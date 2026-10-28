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
    Phase, TileType, Direction, MANA_CAP, ALTAR_POS, Color,
    pos_to_coord, coord_to_pos, GRID_SIZE, TEMPLE_P1_POS, TEMPLE_P2_POS,
    PLAYABLE_ROWS, PLAYABLE_COLS
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
    # Fog of War (v28.3)
    # Visibilità: raggio Chebyshev 2 da qualsiasi creatura del giocatore
    # o dal suo Tempio. Unità/caselle fuori fog non sono bersagliabili.
    # ------------------------------------------------------------------
    def vision_sources(self, player_id: int):
        """Posizioni che generano visione per il giocatore."""
        from .constants import TEMPLE_P1_POS, TEMPLE_P2_POS
        sources = []
        temple = TEMPLE_P1_POS if player_id == 0 else TEMPLE_P2_POS
        sources.append(temple)
        for u in self.board.get_units_of_player(player_id):
            if u.is_alive:
                sources.append((u.row, u.col))
        return sources

    def is_visible_to(self, player_id: int, row: int, col: int, radius: int = 2) -> bool:
        """True se (row,col) è entro `radius` (Chebyshev) da una fonte di visione."""
        for sr, sc in self.vision_sources(player_id):
            if max(abs(sr - row), abs(sc - col)) <= radius:
                return True
        return False

    def visible_coords(self, player_id: int, radius: int = 2):
        """Set di (r,c) visibili al giocatore."""
        from .constants import GRID_SIZE
        vis = set()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.is_visible_to(player_id, r, c, radius):
                    vis.add((r, c))
        return vis

    def can_target_unit(self, viewer_id: int, unit) -> bool:
        """Una magia/abilità a bersaglio può colpire questa unità solo se visibile."""
        if unit is None or not unit.is_alive:
            return False
        # Le proprie unità sono sempre bersagliabili
        if unit.owner_id == viewer_id:
            return True
        return self.is_visible_to(viewer_id, unit.row, unit.col)


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
        """
        Draft a buste sigillate:
        - Sempre 3 buste sul tavolo, ognuna di un colore, 3 carte di quel colore.
        - I giocatori a turno scelgono una busta; ne compare subito una nuova.
        - Ognuno prende 3 buste → 9 carte; a inizio partita si aprono + 1 Boss.
        """
        self.phase = Phase.DRAFT
        self._draft_picks: Dict[int, List[Card]] = {0: [], 1: []}
        self._draft_pack_labels: Dict[int, List[str]] = {0: [], 1: []}
        self._draft_packs_taken: Dict[int, int] = {0: 0, 1: 0}
        self._draft_picker = 0
        self._draft_table: List[dict] = []
        for _ in range(3):
            self._draft_table.append(self._generate_sealed_pack())
        self.log_msg("=== FASE DI DRAFT (buste) ===")
        self.log_msg("3 buste sul tavolo. Scegline una: a inizio partita si aprono (9 carte).")

    def _pack_colors(self) -> List[Color]:
        return [Color.WHITE, Color.BLUE, Color.RED, Color.BLACK, Color.GREEN, Color.YELLOW]

    def _generate_sealed_pack(self) -> dict:
        """Crea una busta: colore + 3 carte random di quel colore (Giallo = mix degli altri 5)."""
        db = get_card_db()
        color = random.choice(self._pack_colors())
        five = [Color.WHITE, Color.BLUE, Color.RED, Color.BLACK, Color.GREEN]
        if color == Color.YELLOW:
            pool = [c for c in db.get_draftable() if c.color in five]
        else:
            pool = [c for c in db.get_draftable(color) if c.color == color]
            if not pool:
                pool = [c for c in db.get_draftable() if c.color in five]
        if not pool:
            pool = list(db.cards.values())[:10]
        cards = []
        for _ in range(3):
            src = random.choice(pool)
            if color == Color.YELLOW and src.color != Color.YELLOW:
                cards.append(db.make_yellow_proxy(src, 80000 + random.randint(1, 90000)))
            else:
                cards.append(src)
        return {"color": color, "cards": cards}

    def get_draft_state(self) -> dict:
        table = getattr(self, "_draft_table", []) or []
        taken = getattr(self, "_draft_packs_taken", {0: 0, 1: 0})
        labels = getattr(self, "_draft_pack_labels", {0: [], 1: []})
        return {
            "active": self.phase == Phase.DRAFT,
            "mode": "sealed_packs",
            "picker": getattr(self, "_draft_picker", 0),
            "packs_needed": 3,
            "packs_taken": {"0": taken.get(0, 0), "1": taken.get(1, 0)},
            "packs": [
                {
                    "index": i,
                    "color": p["color"].value,
                    "size": len(p["cards"]),
                    "label": f"Busta {p['color'].value}",
                }
                for i, p in enumerate(table)
            ],
            # compat UI vecchia
            "pack": [],
            "packs_left": 3 - min(taken.get(0, 0), taken.get(1, 0)),
            "picks": {
                "0": list(labels.get(0, [])),
                "1": list(labels.get(1, [])),
            },
        }

    def draft_pick(self, player_id: int, pack_index: int) -> bool:
        """Il giocatore sceglie una busta dal tavolo (indice 0..2)."""
        if self.phase != Phase.DRAFT:
            return False
        picker = getattr(self, "_draft_picker", 0)
        if player_id != picker:
            self.log_msg(f"Non è il turno di draft di P{player_id} (tocca a P{picker})")
            return False
        table = getattr(self, "_draft_table", [])
        if pack_index < 0 or pack_index >= len(table):
            return False
        pack = table.pop(pack_index)
        # assegna le 3 carte (ancora "chiuse" finché non finisce il draft)
        self._draft_picks[player_id].extend(pack["cards"])
        label = f"Busta {pack['color'].value}"
        self._draft_pack_labels[player_id].append(label)
        self._draft_packs_taken[player_id] = self._draft_packs_taken.get(player_id, 0) + 1
        self.players[player_id].colors.add(pack["color"])
        self.log_msg(f"P{player_id} prende {label} ({self._draft_packs_taken[player_id]}/3)")

        # Sempre 3 buste sul tavolo finché entrambi non hanno 3 buste
        if self._draft_packs_taken.get(0, 0) < 3 or self._draft_packs_taken.get(1, 0) < 3:
            self._draft_table.append(self._generate_sealed_pack())

        if self._draft_packs_taken.get(0, 0) >= 3 and self._draft_packs_taken.get(1, 0) >= 3:
            self._finish_draft()
            return True

        # Alterna giocatore (salta chi ha già 3 buste)
        nxt = 1 - picker
        if self._draft_packs_taken.get(nxt, 0) >= 3:
            nxt = picker
        self._draft_picker = nxt
        self._draft_ai_if_needed()
        return True

    def _draft_ai_if_needed(self):
        """Finché tocca all'IA in DRAFT, sceglie una busta a caso."""
        safety = 0
        while self.phase == Phase.DRAFT and safety < 20:
            safety += 1
            picker = getattr(self, "_draft_picker", 0)
            if not self.players[picker].is_ai:
                break
            if self._draft_packs_taken.get(picker, 0) >= 3:
                break
            table = getattr(self, "_draft_table", [])
            if not table:
                break
            self.draft_pick(picker, random.randrange(len(table)))

    def _finish_draft(self):
        """Apre le buste: 9 carte a testa + Boss del colore dominante."""
        db = get_card_db()
        for pid in (0, 1):
            picks = list(self._draft_picks.get(pid, []))
            color_count = {}
            for c in picks:
                color_count[c.color] = color_count.get(c.color, 0) + 1
            # Giallo non è un colore di Boss dedicato → usa il più frequente tra i 5
            main_color = None
            if color_count:
                ranked = sorted(color_count.items(), key=lambda x: x[1], reverse=True)
                for col, _ in ranked:
                    if col != Color.YELLOW and col != Color.GRAY:
                        main_color = col
                        break
                if main_color is None:
                    main_color = ranked[0][0]
            if main_color is None or main_color in (Color.YELLOW, Color.GRAY):
                main_color = random.choice([Color.WHITE, Color.BLUE, Color.RED, Color.BLACK, Color.GREEN])
            bosses_of_color = [b for b in db.bosses if b.color == main_color]
            if not bosses_of_color:
                bosses_of_color = db.bosses
            boss = random.choice(bosses_of_color)
            picks.append(boss)
            self.players[pid].hand = picks
            self.log_msg(f"P{pid} apre le buste: {len(picks)-1} carte + Boss {boss.name}")
        self.phase = Phase.SETUP
        self.log_msg("Draft completato. Inizio partita.")
        self.current_player_id = 0
        self.turn = 1
        self.start_turn()
        units = self.board.get_units_of_player(0)
        if units:
            self.players[0].place_fragment(units[0])
            self._sync_fragment_card(0)
        # IA: stesso trattamento se ha già unità
        units1 = self.board.get_units_of_player(1)
        if units1 and self.players[1].crown_unit is None:
            self.players[1].place_fragment(units1[0])
            self._sync_fragment_card(1)

    # ------------------------------------------------------------------
    # Turno
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

        # Neutrales rimossi (v28.3)

        # Effetti a inizio turno (Santuario, Fenditura, Growth, ecc.)
        self._apply_start_of_turn_effects(p)
        # Passiva Corona in base ai colori del grimorio
        self._apply_crown_color_passive(p)

        # Verifica Main Quest
        if self.main_quest:
            self._check_main_quest(p)

        self.phase = Phase.MAIN

    def _apply_start_of_turn_effects(self, player: Player):
        for unit in list(self.board.get_units_of_player(player.id)):
            if "stun" in unit.statuses:
                unit.statuses.discard("stun")
                self.log_msg(f"  {unit.card.name} non è più stunnata")
            if "invulnerable" in unit.statuses:
                unit.statuses.discard("invulnerable")
            unit.moved_this_turn = False
            unit.can_attack_this_turn = True
            unit.summoning_sickness = False  # scade a inizio del tuo turno
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

    def _apply_crown_color_passive(self, player: Player):
        """Passiva della Corona: effetto del colore dominante in mano."""
        if not player.crown_unit or not player.crown_unit.is_alive:
            return
        counts = {}
        for c in player.hand:
            counts[c.color] = counts.get(c.color, 0) + 1
        if not counts:
            return
        main = max(counts, key=counts.get)
        crown = player.crown_unit
        self.log_msg(f"  Corona ({main.value}): passiva colore")

        if main == Color.WHITE:
            crown.heal(1)
            self.log_msg(f"    Bianco → Corona cura 1 (HP {crown.current_hp})")
        elif main == Color.BLUE:
            if player.mana < player.mana_max:
                player.mana += 1
                self.log_msg(f"    Blu → +1 mana (ora {player.mana})")
            else:
                self.log_msg("    Blu → mana già al massimo")
        elif main == Color.RED:
            if "corona_rage" not in crown.statuses:
                crown.current_atk += 1
                crown.statuses.add("corona_rage")
                self.log_msg(f"    Rosso → Corona +1 ATK (ora {crown.current_atk})")
            else:
                self.log_msg("    Rosso → rabbia già attiva")
        elif main == Color.BLACK:
            enemies = [u for u in self.board.get_units_of_player(1 - player.id) if u.is_alive]
            if enemies:
                enemies.sort(key=lambda u: u.current_hp)
                t = enemies[0]
                t.take_damage(1)
                self.log_msg(f"    Nero → 1 danno a {t.card.name} ({t.coord})")
                if not t.is_alive:
                    self._destroy_unit(t)
            else:
                self.log_msg("    Nero → nessun nemico")
        elif main == Color.GREEN:
            allies = [u for u in self.board.get_units_of_player(player.id) if u.is_alive]
            if allies:
                allies.sort(key=lambda u: u.current_hp)
                a = allies[0]
                a.heal(1)
                self.log_msg(f"    Verde → cura 1 a {a.card.name}")
            else:
                self.log_msg("    Verde → nessun alleato")
        elif main == Color.YELLOW:
            # Giallo: ogni turno un effetto a caso tra i 5 colori
            pick = random.choice([
                Color.WHITE, Color.BLUE, Color.RED, Color.BLACK, Color.GREEN
            ])
            self.log_msg(f"    Giallo → effetto casuale ({pick.value})")
            if pick == Color.WHITE:
                crown.heal(1)
                self.log_msg(f"      cura Corona 1 (HP {crown.current_hp})")
            elif pick == Color.BLUE:
                if player.mana < player.mana_max:
                    player.mana += 1
                    self.log_msg(f"      +1 mana (ora {player.mana})")
            elif pick == Color.RED:
                if "corona_rage" not in crown.statuses:
                    crown.current_atk += 1
                    crown.statuses.add("corona_rage")
                    self.log_msg(f"      Corona +1 ATK (ora {crown.current_atk})")
            elif pick == Color.BLACK:
                enemies = [u for u in self.board.get_units_of_player(1 - player.id) if u.is_alive]
                if enemies:
                    enemies.sort(key=lambda u: u.current_hp)
                    t = enemies[0]
                    t.take_damage(1)
                    self.log_msg(f"      1 danno a {t.card.name}")
                    if not t.is_alive:
                        self._destroy_unit(t)
            else:
                allies = [u for u in self.board.get_units_of_player(player.id) if u.is_alive]
                if allies:
                    allies.sort(key=lambda u: u.current_hp)
                    a = allies[0]
                    a.heal(1)
                    self.log_msg(f"      cura 1 a {a.card.name}")
        else:
            self.log_msg(f"    {main.value} → nessun effetto speciale")

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
        # Spawn SOLO sulla casella del Tempio del giocatore (v28)
        temple = TEMPLE_P1_POS if player.id == 0 else TEMPLE_P2_POS
        r, c = temple
        if self.board.get_unit_at(r, c) is None and self.board.is_walkable(r, c):
            unit = Unit(free_card, player.id, r, c, 1, 1)
            self.board.place_unit(unit)
            self.log_msg(f"{player.name} spawna Soldato 1/1 su {unit.coord}")
            return
        self.log_msg(f"{player.name}: Tempio occupato, spawn 1/1 fallito")

    def _spawn_neutral(self):
        # Trova casella libera
        free = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)
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

    def _activate_neutrals(self):
        """Ogni Neutrale si muove di 1 passo (re) verso il bersaglio più vicino e attacca se adiacente."""
        neutrals = [u for u in list(self.board.units.values()) if u.owner_id == -1 and u.is_alive]
        if not neutrals:
            return
        for neu in neutrals:
            # Bersaglio: creatura non neutrale più vicina
            targets = [u for u in self.board.units.values() if u.owner_id != -1 and u.is_alive]
            if not targets:
                continue
            targets.sort(key=lambda t: abs(t.row - neu.row) + abs(t.col - neu.col))
            prey = targets[0]
            # Se già adiacente (re: max 1 in riga e colonna, non stessa casella) → combatti
            if max(abs(prey.row - neu.row), abs(prey.col - neu.col)) == 1:
                self.log_msg(f"Neutrale attacca {prey.card.name} su {prey.coord}")
                # Combattimento semplificato senza spendere mana
                dmg = neu.current_atk
                actual = prey.take_damage(dmg, neu)
                self.log_msg(f"  Neutrale infligge {actual} (HP preda: {prey.current_hp})")
                if not prey.is_alive:
                    self._destroy_unit(prey)
                    self.log_msg(f"  {prey.card.name} eliminato dal Neutrale")
                    continue
                # Contrattacco
                actual2 = neu.take_damage(prey.current_atk, prey)
                self.log_msg(f"  Contrattacco {actual2} (HP neutrale: {neu.current_hp})")
                if not neu.is_alive:
                    self._destroy_unit(neu)
                continue
            # Altrimenti muovi 1 passo (re) verso la preda
            best = None
            best_score = 999
            for nr, nc in self.board.get_adjacent(neu.row, neu.col):
                if self.board.get_unit_at(nr, nc) is not None:
                    continue
                score = abs(nr - prey.row) + abs(nc - prey.col)
                if score < best_score:
                    best_score = score
                    best = (nr, nc)
            if best:
                self.board.move_unit(neu, best[0], best[1])
                self.log_msg(f"Neutrale si muove verso {prey.card.name} → {neu.coord}")
                self._on_enter_tile(neu)

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
        if "stun" in unit.statuses:
            self.log_msg(f"{unit.card.name} è stunnata e non può muoversi.")
            return False
        if unit.moved_this_turn and not unit.has_keyword("DoubleMove"):
            return False
        # Movimento re degli scacchi: 1 passo in qualsiasi delle 8 direzioni
        dr = abs(target_row - unit.row)
        dc = abs(target_col - unit.col)
        if not (max(dr, dc) == 1 and (dr + dc) >= 1):
            self.log_msg("Movimento non valido: serve 1 passo adiacente (come il re degli scacchi).")
            return False
        if not self.players[unit.owner_id].can_afford(1):
            self.log_msg("Mana insufficiente.")
            return False

        target_unit = self.board.get_unit_at(target_row, target_col)
        if target_unit is not None:
            # Non si attaccano gli alleati
            if target_unit.owner_id == unit.owner_id:
                self.log_msg("Non puoi attaccare una creatura alleata.")
                return False
            # Neutrale o nemico: serve poter attaccare
            if unit.summoning_sickness or not unit.can_attack_this_turn:
                self.log_msg(f"{unit.card.name} non può attaccare in questo turno.")
                return False
        if target_unit is None:
            # Muro d'Illusione: attacca il muro invece di entrare
            dest = self.board.get_tile(target_row, target_col)
            if dest and dest.tile_type == TileType.ILLUSION_WALL and dest.wall_hp > 0:
                self.players[unit.owner_id].spend_mana(1)
                unit.moved_this_turn = True
                dest.wall_hp -= unit.current_atk
                self.log_msg(f"{unit.card.name} colpisce Muro d'Illusione (−{unit.current_atk}, HP muro {max(0, dest.wall_hp)})")
                if dest.wall_hp <= 0:
                    dest.tile_type = TileType.EMPTY
                    dest.wall_hp = 0
                    self.log_msg("  Muro d'Illusione distrutto!")
                return True
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
            if owner.id in (0, 1):
                self._sync_fragment_card(owner.id)
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
        if tile.permanent_effect == "tower" or tile.tile_type == TileType.TOWER:
            if "tower_range" not in unit.statuses:
                unit.statuses.add("tower_range")
                unit.current_atk += 1
                self.log_msg(f"  Torre: {unit.card.name} ottiene +1 ATK")
        if tile.permanent_effect == "refuge" or tile.tile_type == TileType.SHADOW_REFUGE:
            unit.statuses.add("shield:1")
            self.log_msg(f"  Rifugio: scudo 1 su {unit.card.name}")
        if tile.tile_type == TileType.PORTAL_UNSTABLE:
            # ogni entrata = salto casuale
            empties = []
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    t = self.board.get_tile(r, c)
                    if t and t.is_walkable and self.board.get_unit_at(r, c) is None:
                        if (r, c) != (unit.row, unit.col):
                            empties.append((r, c))
            if empties:
                import random
                nr, nc = random.choice(empties)
                self.board.move_unit(unit, nr, nc)
                self.log_msg(f"  Portale Instabile → {unit.coord}")

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
        if event.startswith("MainQuest"):
            tile.tile_type = TileType.NEUTRAL_TERRAIN
            tile.permanent_effect = "quest_marker"
            self.log_msg("  Tessera Main Quest rivelata (effetto a inizio turno).")
            return
        if event not in mapping:
            self.log_msg(f"  Evento sconosciuto: {event}")
            return
        tile.tile_type = mapping[event]
        if event == "MuroIllusione":
            tile.wall_hp = max(2, unit.current_atk + 1)
            self.log_msg(f"  Muro d'Illusione (HP {tile.wall_hp}). Blocca il passaggio finché non viene distrutto.")
        elif event == "FossaSpine":
            unit.take_damage(2)
            self.log_msg(f"  Fossa di Spine: 2 danni (HP: {unit.current_hp})")
            if not unit.is_alive:
                self._destroy_unit(unit)
        elif event == "RunaFurto":
            opp = self.players[1 - unit.owner_id] if unit.owner_id in (0, 1) else None
            if opp:
                stolen = min(1, opp.mana)
                opp.mana -= stolen
                self.players[unit.owner_id].mana += stolen
                self.log_msg(f"  Runa del Furto: +{stolen} mana (rubati)")
            tile.tile_type = TileType.NEUTRAL_TERRAIN
        elif event == "SantuarioVita":
            tile.permanent_effect = "sanctuary"
            unit.heal(1)
            self.log_msg(f"  Santuario: {unit.card.name} cura 1 all'esplorazione")
        elif event == "Fenditura":
            tile.permanent_effect = "fissure"
            unit.take_damage(1)
            self.log_msg(f"  Fenditura: 1 danno all'esploratore (HP: {unit.current_hp})")
            if not unit.is_alive:
                self._destroy_unit(unit)
        elif event == "Palude":
            tile.permanent_effect = "swamp"
            self.log_msg("  Palude permanente: movimento qui costa 1 mana extra (già incluso nel passo).")
        elif event == "TorreLancio":
            tile.permanent_effect = "tower"
            unit.statuses.add("tower_range")
            unit.current_atk += 1
            self.log_msg(f"  Torre di Lancio: {unit.card.name} +1 ATK (vantaggio di tiro)")
        elif event == "RifugioOmbroso":
            tile.permanent_effect = "refuge"
            unit.statuses.add("shield:1")
            self.log_msg(f"  Rifugio Ombroso: scudo 1 su {unit.card.name}")
        elif event == "PortaleGrigio":
            self.log_msg("  Portale Grigio: collegato agli altri portali (teletrasporto al passo successivo).")
            self._resolve_portal(unit, tile)
        elif event == "PortaleInstabile":
            self.log_msg("  Portale Instabile: teletrasporto casuale su casella vuota!")
            empties = []
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    t = self.board.get_tile(r, c)
                    if t and t.is_walkable and self.board.get_unit_at(r, c) is None:
                        empties.append((r, c))
            if empties:
                import random
                nr, nc = random.choice(empties)
                self.board.move_unit(unit, nr, nc)
                self.log_msg(f"  → sbuca su {unit.coord}")

    def _resolve_trap_effect(self, trap: Card, victim: Unit, tile) -> None:
        """Effetti base delle trappole più comuni."""
        name = trap.name.lower()
        if "spine" in name or "fossa di spine" in name or "fossa rampicante" in name:
            dmg = 2 if "spine" in name else 1
            victim.take_damage(dmg)
            if "rampicante" in name or "ombre" in name:
                victim.statuses.add("stun")
            self.log_msg(f"    → {dmg} danni" + (" + stun" if "rampicante" in name or "ombre" in name else ""))
        elif "mina" in name or "esplosiva" in name:
            victim.take_damage(1)
            self.log_msg(f"    → 1 danno a {victim.card.name}")
        elif "incendiaria" in name:
            victim.take_damage(2)
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                ou = self.board.get_unit_at(victim.row + dr, victim.col + dc)
                if ou and ou is not victim:
                    ou.take_damage(1)
                    if not ou.is_alive:
                        self._destroy_unit(ou)
            self.log_msg(f"    → 2 danni + area adiacenti")
        elif "eter" in name or "mana" in name or "runa" in name:
            owner = self.players[victim.owner_id] if victim.owner_id in (0, 1) else None
            if owner:
                owner.mana = max(0, owner.mana - 1)
                self.log_msg(f"    → -1 mana a {owner.name}")
        elif "luminosa" in name or "blocca" in name or "liana" in name:
            victim.statuses.add("stun")
            self.log_msg(f"    → {victim.card.name} bloccata 1 turno")
        elif "barriera" in name or "radiosa" in name:
            victim.statuses.add("shield:2")
            self.log_msg(f"    → Barriera: scudo 2 su chi attiva (inesatto ma giocabile)")
        else:
            victim.take_damage(1)
            self.log_msg(f"    → effetto generico: 1 danno")

        if not victim.is_alive:
            self._destroy_unit(victim)


    def _resolve_portal(self, unit: Unit, tile) -> None:
        """Teletrasporto: non si sosta sul portale; atterra su adiacente libera del portale di uscita."""
        from .constants import TileType
        portals = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
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
        elif card.card_type == CardType.FRAGMENT:
            return self._play_fragment(p, hand_index, card, target_coord)
        elif card.card_type == CardType.TRAP:
            return self._play_trap(p, hand_index, card, target_coord)
        elif card.card_type == CardType.CURSE:
            return self._play_curse(p, hand_index, card, target_coord)
        else:
            self.log_msg(f"Tipo carta non gestito: {card.card_type}")
            return False

    def _summon_monster(self, player: Player, hand_index: int, card: Card, target_coord: Optional[str]) -> bool:
        """Evoca solo nella propria zona Tempio."""
        # v28: un solo Tempio per giocatore
        temple_positions = (
            [TEMPLE_P1_POS] if player.id == 0
            else [TEMPLE_P2_POS]
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

    def _play_fragment(self, player: Player, hand_index: int, card: Card, target_coord: Optional[str]) -> bool:
        """Gioca la carta Frammento/Corona dalla mano sulla creatura bersaglio."""
        if not target_coord:
            self.log_msg("Scegli una tua creatura su cui piazzare la Corona.")
            return False
        try:
            r, c = coord_to_pos(target_coord.upper())
        except Exception:
            self.log_msg("Coordinata non valida.")
            return False
        unit = self.board.get_unit_at(r, c)
        if not unit or unit.owner_id != player.id or not unit.is_alive:
            self.log_msg("Nessuna tua creatura su quella casella.")
            return False
        cost = player.next_fragment_cost()
        if cost is None:
            self.log_msg("Nessun Frammento rimanente.")
            return False
        if card.cost != cost:
            # allinea costo carta a quello reale
            card.cost = cost
        if not player.can_afford(cost):
            self.log_msg(f"Mana insufficiente (serve {cost}).")
            return False
        # place_fragment spende già il mana
        ok = player.place_fragment(unit)
        if not ok:
            self.log_msg("Impossibile piazzare il Frammento.")
            return False
        # Rimuovi la carta Frammento giocata (place non tocca la mano)
        if 0 <= hand_index < len(player.hand) and player.hand[hand_index].card_type.value == "Frammento":
            player.hand.pop(hand_index)
        else:
            player.hand = [c for c in player.hand if c.card_type.value != "Frammento"]
        self.log_msg(f"{player.name} piazza la Corona su {unit.card.name} ({unit.coord}) per {cost} mana")
        self._sync_fragment_card(player.id)
        return True


    def _sync_fragment_card(self, player_id: int) -> None:
        """
        Mantiene in mano la carta «Frammento / Corona» con il costo corretto.
        - Se restano frammenti e non c'è già la carta in mano → la aggiunge (costo next).
        - Se non restano frammenti → rimuove eventuali carte Frammento dalla mano.
        - Aggiorna il costo della carta già presente.
        """
        from .card import Card
        from .constants import CardType, Color, FRAGMENT_COSTS
        p = self.players[player_id]
        # Rimuovi eventuali duplicate / vecchie
        p.hand = [c for c in p.hand if c.card_type != CardType.FRAGMENT]
        cost = p.next_fragment_cost()
        if cost is None or p.fragments_remaining <= 0:
            return
        frag = Card(
            id=7000 + player_id * 10 + (3 - p.fragments_remaining),
            name="Frammento / Corona",
            cost=cost,
            card_type=CardType.FRAGMENT,
            color=Color.GRAY,
            atk=0,
            hp=0,
            text=f"Piazza la Corona su una tua creatura. Costo attuale: {cost}.",
        )
        p.hand.append(frag)
        self.log_msg(f"  [Corona] carta in mano (costo {cost}, frammenti restanti {p.fragments_remaining})")

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
        name = card.name.lower()
        target_unit = None
        if target_coord:
            try:
                r, c = coord_to_pos(target_coord)
                target_unit = self.board.get_unit_at(r, c)
            except Exception:
                pass
            # Fog of War: non si può bersagliare un nemico fuori visione
            if target_unit is not None and target_unit.owner_id != player.id:
                if not self.can_target_unit(player.id, target_unit):
                    self.log_msg("Bersaglio nascosto dalla nebbia di guerra.")
                    return False
            # Anche casella vuota fuori visione non è bersagliabile per effetti a zona/casella
            if target_unit is None and target_coord:
                try:
                    r, c = coord_to_pos(target_coord)
                    if not self.is_visible_to(player.id, r, c):
                        self.log_msg("Casella nascosta dalla nebbia di guerra.")
                        return False
                except Exception:
                    pass

        player.spend_mana(card.cost)
        player.hand.pop(hand_index)
        target_info = f" su {target_coord}" if target_coord else ""
        self.log_msg(f"{player.name} gioca Maledizione '{card.name}'{target_info}")

        # Ondata 1: effetti per nome (GDD)
        if any(k in name for k in ("raggio solare", "linfa vitale", "cura")):
            if target_unit and target_unit.owner_id == player.id:
                target_unit.heal(1)
                self.log_msg(f"  → {target_unit.card.name} cura 1 HP")
            else:
                self.log_msg("  → nessun alleato valido")
        elif "benedizione minore" in name:
            if target_unit and target_unit.owner_id == player.id:
                target_unit.statuses.add("maxhp:1")
                target_unit.heal(1)
                self.log_msg(f"  → +1 HP max su {target_unit.card.name}")
        elif "crescita rigogliosa" in name:
            if target_unit and target_unit.owner_id == player.id:
                target_unit.current_atk += 1
                target_unit.statuses.add("maxhp:1")
                target_unit.heal(1)
                self.log_msg(f"  → +1/+1 permanente su {target_unit.card.name}")
        elif "preghiera" in name:
            player.mana += 1
            self.log_msg("  → +1 mana (turno corrente)")
        elif "scudo" in name or "fede" in name or "aegis" in name:
            if target_unit and target_unit.owner_id == player.id:
                val = 2 if "aegis" not in name else 99
                if "aegis" in name:
                    target_unit.statuses.add("invulnerable")
                    self.log_msg(f"  → Invulnerabilità 1 turno su {target_unit.card.name}")
                else:
                    target_unit.statuses.add(f"shield:{val}")
                    self.log_msg(f"  → Scudo {val} su {target_unit.card.name}")
        elif "flash" in name or "tocco della fossa" in name:
            if target_unit and target_unit.owner_id != player.id:
                target_unit.current_atk = max(0, target_unit.current_atk - 1)
                self.log_msg(f"  → ATK di {target_unit.card.name} → {target_unit.current_atk}")
        elif any(k in name for k in ("spark", "dardo", "giudizio divino", "succhiasangue", "drenaggio")):
            if target_unit and target_unit.owner_id != player.id:
                dmg = 1
                if "dardo" in name or "drenaggio" in name:
                    dmg = 2
                if "giudizio" in name:
                    dmg = 2 if target_unit.has_fragment else 1
                actual = target_unit.take_damage(dmg)
                self.log_msg(f"  → {actual} danni a {target_unit.card.name}")
                if "succhiasangue" in name and player.crown_unit:
                    player.crown_unit.heal(1)
                    self.log_msg("  → cura 1 al tuo Comandante")
                if not target_unit.is_alive:
                    self._destroy_unit(target_unit)
            else:
                self.log_msg("  → nessun nemico valido")
        elif "esecuzione" in name:
            if target_unit and target_unit.owner_id != player.id and target_unit.current_hp <= 2:
                self.log_msg(f"  → Esecuzione: {target_unit.card.name} distrutto")
                self._destroy_unit(target_unit)
            else:
                self.log_msg("  → bersaglio non valido (serve nemico con ≤2 HP)")
        elif "congelamento" in name or "mente confusa" in name:
            if target_unit and target_unit.owner_id != player.id:
                target_unit.statuses.add("stun")
                self.log_msg(f"  → {target_unit.card.name} non può agire 1 turno")
        elif "carica frenetica" in name:
            if target_unit and target_unit.owner_id == player.id:
                target_unit.current_atk += 1
                target_unit.take_damage(1)
                self.log_msg(f"  → +1 ATK / -1 HP su {target_unit.card.name}")
                if not target_unit.is_alive:
                    self._destroy_unit(target_unit)
        elif "ondata di furia" in name:
            for u in self.board.get_units_of_player(player.id):
                u.current_atk += 1
            self.log_msg("  → +1 ATK a tutte le tue creature (turno)")
        elif "forza gigantesca" in name:
            if target_unit and target_unit.owner_id == player.id:
                target_unit.current_atk += 3
                target_unit.statuses.add("maxhp:3")
                target_unit.heal(3)
                self.log_msg(f"  → +3/+3 temporaneo-ish su {target_unit.card.name}")
        elif "richiamo selvaggio" in name:
            from .card import Card
            from .constants import CardType, Color
            wolf = Card(id=9126, name="Lupo 2/1", cost=0, card_type=CardType.MONSTER, color=Color.GREEN, atk=2, hp=1)
            temple = [TEMPLE_P1_POS] if player.id == 0 else [TEMPLE_P2_POS]
            placed = False
            for r, c in temple:
                if self.board.get_unit_at(r, c) is None and self.board.is_walkable(r, c):
                    self.board.place_unit(Unit(wolf, player.id, r, c, 1, 2))
                    self.log_msg(f"  → Lupo 2/1 evocato su {pos_to_coord(r, c)}")
                    placed = True
                    break
            if not placed:
                self.log_msg("  → spawn pieno, Richiamo fallito")
        else:
            # fallback utile: danno 1 a nemico o cura 1 alleato se c'è target
            if target_unit:
                if target_unit.owner_id != player.id:
                    target_unit.take_damage(1)
                    self.log_msg(f"  → effetto generico: 1 danno a {target_unit.card.name}")
                    if not target_unit.is_alive:
                        self._destroy_unit(target_unit)
                else:
                    target_unit.heal(1)
                    self.log_msg(f"  → effetto generico: cura 1 a {target_unit.card.name}")
            else:
                self.log_msg("  → effetto generico (nessun target)")
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
