"""
IA base per il giocatore in alto (P1).
Priorità (in ordine):
1. Piazzare Frammento se manca
2. Attaccare la Corona nemica se raggiungibile
3. Difendere la propria Corona
4. Evocare Mostri economici / giocare carte utili
5. Muovere verso Altare o Buff
6. Tentare Mostrissimo se ha abbastanza creature
7. Passare il turno
"""

from __future__ import annotations
from typing import List, Optional, Tuple
import random

from core.game_state import GameState
from core.unit import Unit
from core.player import Player
from core.constants import ALTAR_POS, coord_to_pos, pos_to_coord, CardType


class BasicAI:
    def __init__(self, game: GameState, player_id: int = 1):
        self.game = game
        self.pid = player_id

    @property
    def player(self) -> Player:
        return self.game.players[self.pid]

    def take_turn(self) -> None:
        """Esegue un intero turno dell'IA (chiamare quando è il suo turno)."""
        g = self.game
        p = self.player
        g.log_msg(f"[IA] {p.name} sta pensando...")

        # 1. Frammento se manca
        if p.crown_unit is None or not p.crown_unit.is_alive:
            self._try_place_fragment()

        # 2. Prova a giocare 1-2 carte (mostri economici / maledizioni semplici)
        self._try_play_cards(max_plays=2)

        # 3. Movimenti / attacchi (fino a 3 azioni o mana esaurito)
        for _ in range(4):
            if p.mana < 1:
                break
            acted = self._try_combat_or_move()
            if not acted:
                break

        # 4. Mostrissimo se possibile
        self._try_eldrazi()

        g.log_msg(f"[IA] {p.name} termina il turno.")
        g.end_turn()

    # ------------------------------------------------------------------
    # Sotto-strategie
    # ------------------------------------------------------------------
    def _try_place_fragment(self) -> bool:
        p = self.player
        cost = p.next_fragment_cost()
        if cost is None or not p.can_afford(cost):
            return False
        units = self.game.board.get_units_of_player(self.pid)
        if not units:
            return False
        # Preferisci l'unità più forte o più arretrata
        units.sort(key=lambda u: (u.current_hp + u.current_atk, -u.row), reverse=True)
        target = units[0]
        ok = p.place_fragment(target)
        if ok:
            self.game.log_msg(f"[IA] Frammento assegnato a {target}")
        return ok

    def _try_play_cards(self, max_plays: int = 2) -> None:
        p = self.player
        plays = 0
        # Copia indici perché la mano cambia
        indices = list(range(len(p.hand)))
        random.shuffle(indices)

        for idx in indices:
            if plays >= max_plays or p.mana < 1:
                break
            if idx >= len(p.hand):
                continue
            card = p.hand[idx]
            if not p.can_afford(card.cost):
                continue

            if card.card_type in (CardType.MONSTER, CardType.BOSS):
                # Evoca solo se ha senso (costo basso o abbiamo poco campo)
                if card.cost <= p.mana and card.cost <= 3:
                    if self.game.play_card(self.pid, idx, None):
                        plays += 1
            elif card.card_type == CardType.CURSE and card.cost <= 2:
                # Target: nemico più debole o corona nemica
                enemy_units = self.game.board.get_units_of_player(1 - self.pid)
                target_coord = None
                if enemy_units:
                    enemy_units.sort(key=lambda u: u.current_hp)
                    target_coord = enemy_units[0].coord
                if self.game.play_card(self.pid, idx, target_coord):
                    plays += 1
            elif card.card_type == CardType.TRAP and card.cost <= 1:
                # Piazza su una casella centrale-ish libera
                free = self._find_trap_spot()
                if free and self.game.play_card(self.pid, idx, free):
                    plays += 1

    def _find_trap_spot(self) -> Optional[str]:
        candidates = [(2, 1), (2, 3), (1, 2), (3, 2), (2, 2)]
        for r, c in candidates:
            tile = self.game.board.get_tile(r, c)
            if tile and tile.is_walkable and self.game.board.get_unit_at(r, c) is None:
                if tile.trap_card_id is None:
                    return pos_to_coord(r, c)
        return None

    def _try_combat_or_move(self) -> bool:
        """Prova un'azione di movimento/attacco. Ritorna True se ha agito."""
        p = self.player
        units = [u for u in self.game.board.get_units_of_player(self.pid)
                 if not u.moved_this_turn and u.is_alive]
        if not units or p.mana < 1:
            return False

        enemy_crown = self.game.players[1 - self.pid].crown_unit
        my_crown = p.crown_unit

        # Priorità: attaccare corona nemica se adiacente (re)
        for u in units:
            if enemy_crown and enemy_crown.is_alive:
                if self._is_adjacent(u, enemy_crown.row, enemy_crown.col):
                    if self.game.try_move(u, enemy_crown.row, enemy_crown.col):
                        return True

        # Attaccare qualsiasi nemico adiacente
        for u in units:
            enemies_near = self._enemies_adjacent(u)
            if enemies_near:
                # Preferisci il più debole
                enemies_near.sort(key=lambda e: e.current_hp)
                target = enemies_near[0]
                if self.game.try_move(u, target.row, target.col):
                    return True

        # Muovere verso Altare o verso corona nemica
        for u in units:
            target = self._choose_move_target(u, enemy_crown)
            if target:
                tr, tc = target
                if self.game.try_move(u, tr, tc):
                    return True

        return False

    def _is_adjacent(self, unit: Unit, row: int, col: int) -> bool:
        """Adiacenza tipo re degli scacchi (8 caselle)."""
        dr = abs(unit.row - row)
        dc = abs(unit.col - col)
        return max(dr, dc) == 1

    def _enemies_adjacent(self, unit: Unit) -> List[Unit]:
        result = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = unit.row + dr, unit.col + dc
                other = self.game.board.get_unit_at(nr, nc)
                if other and other.owner_id == (1 - self.pid) and other.is_alive:
                    result.append(other)
        return result

    def _choose_move_target(self, unit: Unit, enemy_crown: Optional[Unit]) -> Optional[Tuple[int, int]]:
        """Sceglie una casella adiacente libera verso un obiettivo interessante."""
        candidates = self.game.board.get_adjacent(unit.row, unit.col)
        if not candidates:
            return None

        def score(pos: Tuple[int, int]) -> float:
            r, c = pos
            s = 0.0
            # Vicino all'Altare
            ar, ac = ALTAR_POS
            s -= abs(r - ar) + abs(c - ac) * 0.5
            # Verso corona nemica
            if enemy_crown and enemy_crown.is_alive:
                s -= abs(r - enemy_crown.row) + abs(c - enemy_crown.col) * 0.8
            # Preferisci avanzare (verso il basso per P1)
            if self.pid == 1:
                s += r * 0.3  # riga più alta = più in basso sulla mappa stampata? 
                # In coordinate: riga 0 = alto (P2), riga 4 = basso (P1)
                # P1 vuole scendere → aumentare row
            else:
                s -= r * 0.3
            # Evita caselle già occupate (già filtrate da get_adjacent walkable)
            return s

        candidates.sort(key=score, reverse=True)
        return candidates[0] if candidates else None

    def _try_eldrazi(self) -> bool:
        p = self.player
        if not self.game.eldrazi_pool:
            return False
        my_units = self.game.board.get_units_of_player(self.pid)
        if len(my_units) < 2:
            return False

        # Cerca il Mostrissimo più economico che possiamo permetterci
        for idx, card in enumerate(self.game.eldrazi_pool):
            needed = card.sacrifice_cost
            if len(my_units) < needed:
                continue
            # Deve esserci almeno un'unità su Cerchio Rituale
            ritual_units = []
            other_units = []
            for u in my_units:
                tile = self.game.board.get_tile(u.row, u.col)
                if tile and tile.is_ritual:
                    ritual_units.append(u)
                else:
                    other_units.append(u)
            if not ritual_units:
                continue
            # Non sacrificare la Corona se possiamo evitarlo
            sac = []
            sac.append(ritual_units[0])
            candidates = [u for u in other_units if not u.has_fragment] + \
                         [u for u in other_units if u.has_fragment]
            for u in candidates:
                if len(sac) >= needed:
                    break
                if u not in sac:
                    sac.append(u)
            if len(sac) < needed:
                continue
            coords = [u.coord for u in sac]
            if self.game.summon_eldrazi(self.pid, idx, coords):
                return True
        return False
