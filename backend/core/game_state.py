"""
GameState - stato completo della partita e logica di alto livello
"""

from __future__ import annotations
import random
from typing import List, Optional, Tuple, Dict
from .map_board import Board
from .player import Player
from .unit import Unit
from .card import Card, get_card_db
from .constants import (
    Phase, TileType, Direction, MANA_CAP, ALTAR_POS,
    pos_to_coord, coord_to_pos, Color
)


class GameState:
    def __init__(self, human_name: str = "Hero", ai_name: str = "AI Overlord"):
        self.board = Board()
        self.players = [
            Player(0, human_name, is_ai=False),
            Player(1, ai_name, is_ai=True),
        ]
        self.turn = 1
        self.current_player_id = 0  # inizia l'umano
        self.phase = Phase.DRAFT
        self.log: List[str] = []
        self.main_quest: Optional[str] = None
        self.eldrazi_pool: List[Card] = []
        self.event_deck: List[str] = []  # nomi tessere evento
        self.winner: Optional[int] = None
        self._init_eldrazi_pool()
        self._init_event_deck()

    def log_msg(self, msg: str):
        self.log.append(f"[T{self.turn}] {msg}")
        print(msg)

    # ------------------------------------------------------------------
    # Setup iniziale
    # ------------------------------------------------------------------
    def _init_eldrazi_pool(self):
        db = get_card_db()
        pool = list(db.eldrazi)
        random.shuffle(pool)
        self.eldrazi_pool = pool[:3]  # sempre 3 visibili
        self._eldrazi_remaining = pool[3:]

    def _init_event_deck(self):
        # Tessere base dal GDD
        self.event_deck = [
            "PortaleGrigio", "PortaleInstabile",
            "Palude", "TorreLancio", "SantuarioVita", "Fenditura",
            "MuroIllusione", "RifugioOmbroso",
            "FossaSpine", "RunaFurto",
            "MainQuest_Dominio", "MainQuest_Superiorita",
        ]
        random.shuffle(self.event_deck)

    def start_draft(self):
        """Prepara le 3 bustine e avvia lo snake draft (implementazione base)."""
        self.phase = Phase.DRAFT
        db = get_card_db()
        draftable = db.get_draftable()
        random.shuffle(draftable)

        # 3 bustine da 3 carte
        packs = [draftable[i*3:(i+1)*3] for i in range(3)]
        self._draft_packs = packs
        self._draft_picks: Dict[int, List[Card]] = {0: [], 1: []}
        self.log_msg("=== FASE DI DRAFT ===")
        self.log_msg("3 bustine pronte. Inizia lo snake draft.")

    def get_current_pack(self) -> List[Card]:
        if not hasattr(self, "_draft_packs") or not self._draft_packs:
            return []
        return self._draft_packs[0]

    def draft_pick(self, player_id: int, card_index: int) -> bool:
        """Il giocatore sceglie una carta dalla bustina corrente."""
        pack = self.get_current_pack()
        if not pack or card_index < 0 or card_index >= len(pack):
            return False
        card = pack.pop(card_index)
        self._draft_picks[player_id].append(card)
        self.players[player_id].colors.add(card.color)
        self.log_msg(f"P{player_id} ha scelto: {card}")

        # Se la bustina è vuota, passa alla prossima
        if not pack:
            self._draft_packs.pop(0)
            if self._draft_packs:
                self.log_msg(f"Nuova bustina rivelata ({len(self._draft_packs[0])} carte)")
            else:
                self._finish_draft()
        return True

    def _finish_draft(self):
        db = get_card_db()
        for pid in (0, 1):
            picks = self._draft_picks[pid]
            # Aggiungi un Boss garantito del colore più presente (o random)
            color_count = {}
            for c in picks:
                color_count[c.color] = color_count.get(c.color, 0) + 1
            main_color = max(color_count, key=color_count.get) if color_count else list(Color)[0]
            bosses_of_color = [b for b in db.bosses if b.color == main_color]
            if not bosses_of_color:
                bosses_of_color = db.bosses
            boss = random.choice(bosses_of_color)
            picks.append(boss)
            self.players[pid].hand = picks
            self.log_msg(f"P{pid} mano finale ({len(picks)} carte) + Boss: {boss.name}")
        self.phase = Phase.SETUP
        self.log_msg("Draft completato. Preparazione campo...")

    # ------------------------------------------------------------------
    # Turno
    # ------------------------------------------------------------------
    def start_turn(self):
        p = self.players[self.current_player_id]
        self.phase = Phase.TURN_START
        self.log_msg(f"=== Turno {self.turn} - {p.name} ===")

        # Progressione mana (regola GDD)
        if self.turn == 1:
            pass  # già 1/1
        else:
            # Alternata: al proprio turno si aumenta
            if self.turn >= 2:
                p.increase_mana_max(2 if self.turn > 2 else 1)
            p.refresh_mana()

        # Spawn gratuito 1/1
        self._spawn_free_1_1(p)

        # Mostro Neutrale
        self._spawn_neutral()

        # Effetti a inizio turno (Santuario, Fenditura, Growth, ecc.)
        self._apply_start_of_turn_effects(p)

        # Verifica Main Quest
        if self.main_quest:
            self._check_main_quest(p)

        self.phase = Phase.MAIN

    def _apply_start_of_turn_effects(self, player: Player):
        for unit in list(self.board.get_units_of_player(player.id)):
            tile = self.board.get_tile(unit.row, unit.col)
            if not tile:
                continue
            if tile.tile_type == TileType.SANCTUARY or tile.permanent_effect == "sanctuary":
                unit.heal(1)
                self.log_msg(f"  Santuario: {unit.card.name} +1 HP")
            if tile.tile_type == TileType.FISSURE or tile.permanent_effect == "fissure":
                unit.take_damage(1)
                self.log_msg(f"  Fenditura: {unit.card.name} subisce 1 danno")
                if not unit.is_alive:
                    self._destroy_unit(unit)
            if "Growth" in (unit.card.keywords or []):
                unit.current_hp += 1
                self.log_msg(f"  Crescita: {unit.card.name} +1 HP (ora {unit.current_hp})")
            if "Regenerate" in (unit.card.keywords or []):
                unit.heal(1)
                self.log_msg(f"  Rigenerazione: {unit.card.name} +1 HP")
            # Altare C3 – Evoluzione (GDD): inizia il turno sul centro
            if (unit.row, unit.col) == ALTAR_POS:
                if "evolved" not in unit.statuses:
                    unit.statuses.add("evolved")
                    unit.current_atk += 1
                    unit.heal(1)
                    self.log_msg(
                        f"  ✦ Altare C3: {unit.card.name} evolve! +1 ATK permanente, +1 HP "
                        f"(ora {unit.current_atk}/{unit.current_hp})"
                    )
                else:
                    unit.heal(1)
                    self.log_msg(f"  ✦ Altare C3: {unit.card.name} già evoluta, +1 HP")

    def _spawn_free_1_1(self, player: Player):
        from .card import Card
        from .constants import CardType, Color
        free_card = Card(
            id=9000 + self.turn,
            name="Soldato 1/1",
            cost=0,
            card_type=CardType.MONSTER,
            color=Color.GRAY,
            atk=1, hp=1,
            text="Creatura gratuita di spawn."
        )
        # Cerca casella libera nella zona tempio
        temple_positions = (
            [(4, 1), (4, 2), (4, 3)] if player.id == 0
            else [(0, 1), (0, 2), (0, 3)]
        )
        for r, c in temple_positions:
            if self.board.get_unit_at(r, c) is None and self.board.is_walkable(r, c):
                unit = Unit(free_card, player.id, r, c, 1, 1)
                self.board.place_unit(unit)
                self.log_msg(f"{player.name} spawna Soldato 1/1 su {unit.coord}")
                return
        self.log_msg(f"{player.name}: zona spawn occupata, spawn 1/1 fallito (fuoco amico possibile in futuro)")

    def _spawn_neutral(self):
        # Trova casella libera
        free = [(r, c) for r in range(5) for c in range(5)
                if self.board.get_unit_at(r, c) is None and self.board.is_walkable(r, c)]
        if not free:
            return
        r, c = random.choice(free)
        x = max(0, self.turn // 2)
        atk = x
        hp = max(1, x)
        from .card import Card
        from .constants import CardType, Color
        neut = Card(id=8000 + self.turn, name=f"Neutrale {atk}/{hp}", cost=0,
                    card_type=CardType.NEUTRAL, color=Color.GRAY, atk=atk, hp=hp)
        unit = Unit(neut, -1, r, c, hp, atk)  # owner -1 = neutrale
        self.board.place_unit(unit)
        self.log_msg(f"Mostro Neutrale {atk}/{hp} appare su {unit.coord}")

    def end_turn(self):
        p = self.players[self.current_player_id]
        # Controllo sconfitta (nessun frammento)
        if p.crown_unit is None or not p.crown_unit.is_alive:
            # Ha ancora frammenti da piazzare?
            if p.fragments_remaining > 0 and p.can_afford(p.next_fragment_cost() or 999):
                self.log_msg(f"{p.name} deve piazzare un nuovo Frammento prima di fine turno!")
                # In prototipo forziamo la sconfitta se non lo fa
            else:
                p.has_lost = True
                self.winner = 1 - p.id
                self.phase = Phase.GAME_OVER
                self.log_msg(f"*** {p.name} ha perso! Nessun Frammento in campo. ***")
                return

        # Passa al giocatore successivo
        self.current_player_id = 1 - self.current_player_id
        if self.current_player_id == 0:
            self.turn += 1
        self.start_turn()

    # ------------------------------------------------------------------
    # Movimento e Combattimento (core)
    # ------------------------------------------------------------------
    def try_move(self, unit: Unit, target_row: int, target_col: int) -> bool:
        if unit.owner_id != self.current_player_id:
            return False
        if unit.moved_this_turn and not unit.has_keyword("DoubleMove"):
            return False
        # Solo diagonale di 1
        dr = abs(target_row - unit.row)
        dc = abs(target_col - unit.col)
        if not (dr == 1 and dc == 1):
            self.log_msg("Movimento non diagonale di 1 passo.")
            return False
        if not self.players[unit.owner_id].can_afford(1):
            self.log_msg("Mana insufficiente.")
            return False

        target_unit = self.board.get_unit_at(target_row, target_col)
        if target_unit is None:
            # Movimento libero
            if self.board.move_unit(unit, target_row, target_col):
                self.players[unit.owner_id].spend_mana(1)
                unit.moved_this_turn = True
                self.log_msg(f"{unit} si muove su {pos_to_coord(target_row, target_col)}")
                self._on_enter_tile(unit)
                return True
            return False
        else:
            # Combattimento
            return self._resolve_combat(unit, target_unit)

    def _resolve_combat(self, attacker: Unit, defender: Unit) -> bool:
        self.log_msg(f"COMBATTIMENTO: {attacker} → {defender}")
        self.players[attacker.owner_id].spend_mana(1)

        # 1. First Strike attaccante
        dmg = attacker.current_atk
        actual = defender.take_damage(dmg, attacker)
        self.log_msg(f"  First Strike: {actual} danni a {defender.card.name} (HP rimasti: {defender.current_hp})")

        if not defender.is_alive:
            self.log_msg(f"  {defender.card.name} eliminato! {attacker} conquista la casella.")
            self._destroy_unit(defender)
            self.board.move_unit(attacker, defender.row, defender.col)
            attacker.moved_this_turn = True
            return True

        # 2. Contrattacco
        dmg2 = defender.current_atk
        actual2 = attacker.take_damage(dmg2, defender)
        self.log_msg(f"  Contrattacco: {actual2} danni a {attacker.card.name} (HP rimasti: {attacker.current_hp})")

        if not attacker.is_alive:
            self.log_msg(f"  {attacker.card.name} eliminato nel contrattacco!")
            self._destroy_unit(attacker)
            return True

        # 3. Rimbalzo
        self.log_msg(f"  Entrambi sopravvivono → Rimbalzo di {attacker.card.name}")
        # L'attaccante resta dove era (non si muove)
        attacker.moved_this_turn = True
        return True

    def _destroy_unit(self, unit: Unit):
        if unit.has_fragment:
            owner = self.players[unit.owner_id]
            owner.lose_fragment()
            self.log_msg(f"  ⚠ Frammento di {owner.name} perso!")
        self.board.remove_unit(unit)

    def _on_enter_tile(self, unit: Unit):
        tile = self.board.get_tile(unit.row, unit.col)
        if not tile:
            return

        # Attivazione trappola nascosta
        if tile.trap_card_id is not None:
            db = get_card_db()
            trap = db.get(tile.trap_card_id)
            if trap:
                self.log_msg(f"  ⚠ Trappola attivata: {trap.name}!")
                self._resolve_trap_effect(trap, unit, tile)
            tile.trap_card_id = None  # consumata

        # Esplorazione tessera Evento
        if not tile.explored and tile.tile_type == TileType.EVENT:
            tile.explored = True
            if self.event_deck:
                event = self.event_deck.pop(0)
                self.log_msg(f"  Esplorazione! Tessera rivelata: {event}")
                self._apply_event_tile(event, unit, tile)
                if event.startswith("MainQuest") and self.main_quest is None:
                    self.main_quest = event
                    self.log_msg(f"  ★ MAIN QUEST rivelata: {event}")

        # Portali: entrata → uscita su casella adiacente libera del portale collegato
        if tile.is_portal:
            self._resolve_portal(unit, tile)

        # Effetti permanenti del terreno
        if tile.permanent_effect == "swamp" or tile.tile_type == TileType.SWAMP:
            self.log_msg(f"  Palude: +1 mana extra per entrare/uscire (già pagato movimento).")
        if tile.tile_type == TileType.MAGMA or (tile.permanent_effect or "").startswith("magma"):
            dmg = 2
            unit.take_damage(dmg)
            self.log_msg(f"  Magma: {unit.card.name} subisce {dmg} danni (HP: {unit.current_hp})")
            if not unit.is_alive:
                self._destroy_unit(unit)
        if tile.tile_type == TileType.SPIKE_PIT:
            unit.take_damage(1)
            self.log_msg(f"  Fossa di Spine: 1 danno (HP: {unit.current_hp})")
            if not unit.is_alive:
                self._destroy_unit(unit)

    def _apply_event_tile(self, event: str, unit: Unit, tile) -> None:
        """Applica l'effetto della tessera rivelata e aggiorna il tipo della casella."""
        mapping = {
            "PortaleGrigio": TileType.PORTAL_GRAY,
            "PortaleInstabile": TileType.PORTAL_UNSTABLE,
            "Palude": TileType.SWAMP,
            "TorreLancio": TileType.TOWER,
            "SantuarioVita": TileType.SANCTUARY,
            "Fenditura": TileType.FISSURE,
            "MuroIllusione": TileType.ILLUSION_WALL,
            "RifugioOmbroso": TileType.SHADOW_REFUGE,
            "FossaSpine": TileType.SPIKE_PIT,
            "RunaFurto": TileType.MANA_STEAL,
        }
        if event in mapping:
            tile.tile_type = mapping[event]
            if event == "MuroIllusione":
                tile.wall_hp = unit.current_atk + 1
                self.log_msg(f"  Muro d'Illusione eretto (HP {tile.wall_hp})")
            if event == "FossaSpine":
                unit.take_damage(2)
                self.log_msg(f"  Fossa di Spine: 2 danni all'esploratore (HP: {unit.current_hp})")
                if not unit.is_alive:
                    self._destroy_unit(unit)
            if event == "RunaFurto":
                opp = self.players[1 - unit.owner_id]
                stolen = min(1, opp.mana)
                opp.mana -= stolen
                self.players[unit.owner_id].mana += stolen
                self.log_msg(f"  Runa del Furto: rubati {stolen} mana all'avversario")
                tile.tile_type = TileType.NEUTRAL_TERRAIN
            if event == "SantuarioVita":
                tile.permanent_effect = "sanctuary"
            if event == "Fenditura":
                tile.permanent_effect = "fissure"

    def _resolve_trap_effect(self, trap: Card, victim: Unit, tile) -> None:
        """Effetti base delle trappole più comuni."""
        name = trap.name.lower()
        if "spine" in name or "fossa" in name:
            victim.take_damage(2)
            self.log_msg(f"    → 2 danni a {victim.card.name}")
        elif "mina" in name or "esplosiva" in name:
            victim.take_damage(1)
            self.log_msg(f"    → 1 danno a {victim.card.name}")
        elif "incendiaria" in name:
            # area 3x3 semplificata: danno al victim + adiacenti
            victim.take_damage(2)
            self.log_msg(f"    → 2 danni area a {victim.card.name}")
        elif "eter" in name or "mana" in name:
            owner = self.players[victim.owner_id] if victim.owner_id in (0, 1) else None
            if owner:
                owner.mana = max(0, owner.mana - 1)
                self.log_msg(f"    → -1 mana a {owner.name}")
        elif "luminosa" in name or "blocca" in name:
            victim.statuses.add("stun")
            self.log_msg(f"    → {victim.card.name} bloccata per 1 turno")
        else:
            victim.take_damage(1)
            self.log_msg(f"    → effetto generico: 1 danno")

        if not victim.is_alive:
            self._destroy_unit(victim)


    def _resolve_portal(self, unit: Unit, tile) -> None:
        """Teletrasporto: non si sosta sul portale; atterra su adiacente libera del portale di uscita."""
        from .constants import TileType
        portals = []
        for r in range(5):
            for c in range(5):
                t = self.board.get_tile(r, c)
                if t and t.is_portal and (r, c) != (unit.row, unit.col):
                    portals.append((r, c, t))
        if not portals:
            self.log_msg("  Portale senza uscita attiva.")
            return
        # Preferisci colore opposto bianco/nero, altrimenti primo disponibile
        exit_pos = None
        if tile.tile_type == TileType.PORTAL_WHITE:
            for r, c, t in portals:
                if t.tile_type == TileType.PORTAL_BLACK:
                    exit_pos = (r, c)
                    break
        elif tile.tile_type == TileType.PORTAL_BLACK:
            for r, c, t in portals:
                if t.tile_type == TileType.PORTAL_WHITE:
                    exit_pos = (r, c)
                    break
        if exit_pos is None:
            r, c, _ = portals[0]
            exit_pos = (r, c)
        # Casella adiacente libera (ortogonale o diagonale) attorno all'uscita
        er, ec = exit_pos
        candidates = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = er + dr, ec + dc
                if self.board.is_valid_pos(nr, nc) and self.board.is_walkable(nr, nc):
                    if self.board.get_unit_at(nr, nc) is None:
                        candidates.append((nr, nc))
        if not candidates:
            self.log_msg("  Portale: nessuna casella libera in uscita.")
            return
        nr, nc = candidates[0]
        self.board.move_unit(unit, nr, nc)
        self.log_msg(f"  ✈ Teletrasporto → {unit.coord}")

    def _check_main_quest(self, player: Player):
        if not self.main_quest:
            return
        if self.main_quest == "MainQuest_Dominio":
            # Controlla almeno 2 caselle Buff + Altare
            my_units = self.board.get_units_of_player(player.id)
            buff_count = 0
            has_altar = False
            for u in my_units:
                tile = self.board.get_tile(u.row, u.col)
                if not tile:
                    continue
                if tile.tile_type == TileType.BUFF:
                    buff_count += 1
                if tile.tile_type == TileType.ALTAR:
                    has_altar = True
            if buff_count >= 2 and has_altar:
                self.winner = player.id
                self.phase = Phase.GAME_OVER
                self.log_msg(f"*** {player.name} vince per Dominio del Territorio! ***")
        elif self.main_quest == "MainQuest_Superiorita":
            my_units = len(self.board.get_units_of_player(player.id))
            opp_units = len(self.board.get_units_of_player(1 - player.id))
            if my_units >= opp_units + 3:
                self.winner = player.id
                self.phase = Phase.GAME_OVER
                self.log_msg(f"*** {player.name} vince per Superiorità Numerica! ***")

    # ------------------------------------------------------------------
    # Gioco carte (Evocazione / Trappole / Maledizioni)
    # ------------------------------------------------------------------
    def play_card(self, player_id: int, hand_index: int, target_coord: Optional[str] = None) -> bool:
        """
        Gioca una carta dalla mano.
        - Mostro / Boss → solo nella propria zona Tempio
        - Trappola → su una casella (nasconde la trappola)
        - Maledizione → effetto istantaneo (target opzionale)
        """
        if player_id != self.current_player_id:
            self.log_msg("Non è il tuo turno.")
            return False
        p = self.players[player_id]
        if hand_index < 0 or hand_index >= len(p.hand):
            self.log_msg("Indice mano non valido.")
            return False

        card = p.hand[hand_index]
        if not p.can_afford(card.cost):
            self.log_msg(f"Mana insufficiente (serve {card.cost}, hai {p.mana}).")
            return False

        from .constants import CardType

        if card.card_type in (CardType.MONSTER, CardType.BOSS):
            return self._summon_monster(p, hand_index, card, target_coord)
        elif card.card_type == CardType.TRAP:
            return self._play_trap(p, hand_index, card, target_coord)
        elif card.card_type == CardType.CURSE:
            return self._play_curse(p, hand_index, card, target_coord)
        else:
            self.log_msg(f"Tipo carta non gestito: {card.card_type}")
            return False

    def _summon_monster(self, player: Player, hand_index: int, card: Card, target_coord: Optional[str]) -> bool:
        """Evoca solo nella propria zona Tempio."""
        temple_positions = (
            [(4, 1), (4, 2), (4, 3)] if player.id == 0
            else [(0, 1), (0, 2), (0, 3)]
        )
        # Se target specificato, deve essere nella zona
        if target_coord:
            try:
                r, c = coord_to_pos(target_coord)
            except Exception:
                self.log_msg("Coordinata non valida.")
                return False
            if (r, c) not in temple_positions:
                self.log_msg("Puoi evocare solo nella tua zona Tempio.")
                return False
        else:
            # Prima casella libera della zona
            found = None
            for r, c in temple_positions:
                if self.board.get_unit_at(r, c) is None and self.board.is_walkable(r, c):
                    found = (r, c)
                    break
            if not found:
                self.log_msg("Nessuna casella libera nella zona Tempio.")
                return False
            r, c = found

        if self.board.get_unit_at(r, c) is not None:
            self.log_msg("Casella già occupata (fuoco amico / sovrapposizione non ancora gestita in evocazione).")
            return False

        player.spend_mana(card.cost)
        unit = Unit(card, player.id, r, c, card.hp, card.atk)
        has_charge = "Charge" in (card.keywords or [])
        has_sickness = "SummoningSickness" in (card.keywords or [])
        if has_sickness or not has_charge:
            unit.summoning_sickness = True
            unit.can_attack_this_turn = False
        self.board.place_unit(unit)
        player.hand.pop(hand_index)
        self.log_msg(f"{player.name} evoca {card.name} ({card.atk}/{card.hp}) su {unit.coord}")
        return True

    def _play_trap(self, player: Player, hand_index: int, card: Card, target_coord: Optional[str]) -> bool:
        if not target_coord:
            self.log_msg("Devi specificare la casella per la Trappola.")
            return False
        try:
            r, c = coord_to_pos(target_coord)
        except Exception:
            self.log_msg("Coordinata non valida.")
            return False
        tile = self.board.get_tile(r, c)
        if not tile or not tile.is_walkable:
            self.log_msg("Casella non valida per Trappola.")
            return False
        if tile.trap_card_id is not None:
            self.log_msg("C'è già una Trappola su questa casella.")
            return False

        player.spend_mana(card.cost)
        tile.trap_card_id = card.id
        player.hand.pop(hand_index)
        self.log_msg(f"{player.name} piazza Trappola '{card.name}' su {target_coord} (nascosta)")
        return True

    def _play_curse(self, player: Player, hand_index: int, card: Card, target_coord: Optional[str]) -> bool:
        """Maledizioni istantanee con effetti base."""
        player.spend_mana(card.cost)
        player.hand.pop(hand_index)
        target_info = f" su {target_coord}" if target_coord else ""
        self.log_msg(f"{player.name} gioca Maledizione '{card.name}'{target_info}")

        name = card.name.lower()
        target_unit = None
        if target_coord:
            try:
                r, c = coord_to_pos(target_coord)
                target_unit = self.board.get_unit_at(r, c)
            except Exception:
                pass

        # Effetti semplici basati sul nome (espandibile)
        if "raggio solare" in name or "cura" in name or "linfa" in name:
            if target_unit and target_unit.owner_id == player.id:
                target_unit.heal(1)
                self.log_msg(f"  → {target_unit.card.name} cura 1 HP")
        elif "spark" in name or "dardo" in name or "giudizio" in name:
            if target_unit and target_unit.owner_id != player.id:
                dmg = 2 if "dardo" in name or "giudizio" in name else 1
                target_unit.take_damage(dmg)
                self.log_msg(f"  → {dmg} danni a {target_unit.card.name}")
                if not target_unit.is_alive:
                    self._destroy_unit(target_unit)
        elif "preghiera" in name:
            player.mana += 1
            self.log_msg(f"  → +1 mana temporaneo")
        elif "scudo" in name or "fede" in name:
            if target_unit and target_unit.owner_id == player.id:
                target_unit.statuses.add("shield:2")
                self.log_msg(f"  → Scudo 2 su {target_unit.card.name}")
        elif "flash" in name:
            if target_unit and target_unit.owner_id != player.id:
                target_unit.current_atk = max(0, target_unit.current_atk - 1)
                self.log_msg(f"  → ATK di {target_unit.card.name} ridotto a {target_unit.current_atk}")
        else:
            self.log_msg(f"  → effetto generico applicato")
        return True

    def summon_eldrazi(self, player_id: int, eldrazi_index: int, sacrifice_coords: List[str]) -> bool:
        """
        Evoca un Mostrissimo dal pool comune.
        - Costo: 0 mana ma N sacrifici (sacrifice_cost della carta)
        - Almeno una creatura sacrificata deve stare su Cerchio Rituale
        - Il Mostrissimo appare esattamente su quella casella Rituale
        """
        if player_id != self.current_player_id:
            return False
        p = self.players[player_id]
        if eldrazi_index < 0 or eldrazi_index >= len(self.eldrazi_pool):
            self.log_msg("Indice Mostrissimo non valido.")
            return False

        card = self.eldrazi_pool[eldrazi_index]
        needed = card.sacrifice_cost
        if len(sacrifice_coords) < needed:
            self.log_msg(f"Servono {needed} sacrifici, ne hai indicati {len(sacrifice_coords)}.")
            return False

        # Risolvi le unità da sacrificare
        to_sacrifice: List[Unit] = []
        ritual_pos = None
        for coord in sacrifice_coords[:needed]:
            try:
                r, c = coord_to_pos(coord.upper())
            except Exception:
                self.log_msg(f"Coordinata non valida: {coord}")
                return False
            u = self.board.get_unit_at(r, c)
            if not u or u.owner_id != player_id:
                self.log_msg(f"Nessuna tua creatura su {coord}")
                return False
            to_sacrifice.append(u)
            tile = self.board.get_tile(r, c)
            if tile and tile.is_ritual:
                ritual_pos = (r, c)

        if ritual_pos is None:
            self.log_msg("Almeno una creatura sacrificata deve stare su un Cerchio Rituale.")
            return False

        # Esegui i sacrifici
        for u in to_sacrifice:
            self.log_msg(f"  Sacrificio: {u.card.name} su {u.coord}")
            self._destroy_unit(u)

        # Evoca il Mostrissimo sulla casella del Rituale
        r, c = ritual_pos
        unit = Unit(card, player_id, r, c, card.hp, card.atk)
        self.board.place_unit(unit)
        self.log_msg(f"{p.name} evoca MOSTRISSIMO {card.name} ({card.atk}/{card.hp}) su {unit.coord}!")

        # Rimpiazza nel pool
        self.eldrazi_pool.pop(eldrazi_index)
        if self._eldrazi_remaining:
            new_one = self._eldrazi_remaining.pop(0)
            self.eldrazi_pool.append(new_one)
            self.log_msg(f"  Nuovo Mostrissimo rivelato: {new_one.name}")
        return True

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def print_state(self):
        print("\n" + "=" * 50)
        print(self.board.print_board())
        print("-" * 50)
        for p in self.players:
            print(p)
            if p.crown_unit:
                print(f"  Corona su: {p.crown_unit}")
            if p.hand:
                print(f"  Mano: {', '.join(str(c) for c in p.hand[:5])}{'...' if len(p.hand)>5 else ''}")
        print(f"Turno: {self.turn} | Giocatore corrente: {self.players[self.current_player_id].name}")
        print(f"Fase: {self.phase.name} | Main Quest: {self.main_quest}")
        if self.eldrazi_pool:
            print("Mostrissimi disponibili:")
            for i, e in enumerate(self.eldrazi_pool):
                print(f"  [{i}] {e.name} ({e.atk}/{e.hp}) - Sacrifici: {e.sacrifice_cost}")
        print("=" * 50 + "\n")
