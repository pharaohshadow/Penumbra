"""
Board esagonale – layout da reference utente (v38)
- Anello esterno marrone = Cornice (non calpestabile)
- Interno = terreno / templi / altare
- Muri rossi = edge walls (approssimazione fedele allo sketch)
"""
from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple

from .constants import (
    HEX_RADIUS, PLAYABLE_RADIUS, HexPos, hex_neighbors, hex_in_radius, all_hexes,
    hex_key, hex_distance, ALTAR_POS, TEMPLE_P1_POS, TEMPLE_P2_POS,
    TEMPLE_P3_POS, TEMPLE_P4_POS, FLAVOR_NAMES, TileType,
)
from .tile import Tile
from .unit import Unit


def _edge_key(a: HexPos, b: HexPos) -> Tuple[HexPos, HexPos]:
    return (a, b) if a <= b else (b, a)


class Board:
    def __init__(self):
        self.tiles: Dict[HexPos, Tile] = {}
        self.units: Dict[HexPos, Unit] = {}
        self.edge_walls: Set[Tuple[HexPos, HexPos]] = set()
        self._flavor_by_pos: Dict[HexPos, str] = {}
        self._pos_by_flavor: Dict[str, HexPos] = {}
        self._setup_hex_layout()

    def _setup_hex_layout(self):
        cells = all_hexes(HEX_RADIUS)
        flavor_pool = list(FLAVOR_NAMES)
        fi = 0

        for q, r in cells:
            dist = hex_distance((0, 0), (q, r))
            if dist > PLAYABLE_RADIUS:
                ttype = TileType.FRAME
                name = "BoscoEsterno"
            elif (q, r) == ALTAR_POS:
                ttype = TileType.ALTAR
                name = "Altare"
            elif (q, r) == TEMPLE_P1_POS:
                ttype = TileType.TEMPLE_P1
                name = "Tempio1"
            elif (q, r) == TEMPLE_P2_POS:
                ttype = TileType.TEMPLE_P2
                name = "Tempio2"
            elif (q, r) == TEMPLE_P3_POS:
                ttype = TileType.TEMPLE_P3
                name = "Tempio3"
            elif (q, r) == TEMPLE_P4_POS:
                ttype = TileType.TEMPLE_P4
                name = "Tempio4"
            else:
                ttype = TileType.EMPTY
                name = flavor_pool[fi % len(flavor_pool)]
                fi += 1

            tile = Tile(row=r, col=q, tile_type=ttype)
            tile.flavor_name = name
            tile.explored = True
            self.tiles[(q, r)] = tile
            self._flavor_by_pos[(q, r)] = name
            # flavor unico: se duplicato aggiungi suffisso
            base = name
            n = 2
            while name in self._pos_by_flavor:
                name = f"{base}{n}"
                n += 1
            tile.flavor_name = name
            self._flavor_by_pos[(q, r)] = name
            self._pos_by_flavor[name] = (q, r)

        self._setup_walls_from_sketch()

    def _setup_walls_from_sketch(self):
        """
        Muri rossi dallo sketch utente (edge tra hex adiacenti).
        Coordinate axial pointy-top, centro (0,0).
        Pattern: corridoi / choke intorno all'altare e verso i 4 templi.
        """
        walls = [
            # --- Nord (verso Tempio2 0,-3) ---
            ((0, -2), (1, -3)),
            ((0, -2), (-1, -2)),
            ((1, -2), (1, -3)),
            ((-1, -1), (-1, -2)),
            ((0, -1), (1, -2)),
            ((-1, -1), (0, -1)),
            # arco NE
            ((1, -2), (2, -2)),
            ((2, -3), (2, -2)),
            ((1, -1), (2, -2)),
            # arco NW
            ((-2, -1), (-1, -1)),
            ((-2, 0), (-2, -1)),
            ((-1, 0), (-1, -1)),

            # --- Est (verso Tempio4 3,-3) ---
            ((2, -1), (2, 0)),
            ((2, -1), (3, -2)),
            ((1, 0), (2, -1)),
            ((2, 0), (3, -1)),
            ((1, 1), (2, 0)),
            ((2, -2), (3, -2)),

            # --- Ovest (verso Tempio3 -3,0) ---
            ((-2, 1), (-1, 1)),
            ((-2, 1), (-2, 0)),
            ((-1, 1), (-1, 0)),
            ((-2, 2), (-2, 1)),
            ((-3, 1), (-2, 1)),
            ((-1, 2), (-1, 1)),

            # --- Sud (verso Tempio1 0,3) ---
            ((0, 2), (1, 1)),
            ((0, 2), (-1, 2)),
            ((1, 2), (1, 1)),
            ((-1, 3), (-1, 2)),
            ((0, 1), (0, 2)),
            ((1, 1), (0, 1)),
            ((-1, 2), (0, 1)),
            # arco SE / SW
            ((1, 2), (2, 1)),
            ((2, 1), (1, 1)),
            ((-2, 2), (-1, 2)),

            # --- Centro / medio (segmenti vicino altare) ---
            ((0, 0), (1, 0)),   # muro a est dell'altare (visibile nello sketch)
            ((1, -1), (0, 0)),
            ((-1, 0), (0, 0)),
            ((0, 1), (-1, 1)),
            ((1, 0), (1, 1)),
        ]

        for a, b in walls:
            if hex_in_radius(*a, PLAYABLE_RADIUS) and hex_in_radius(*b, PLAYABLE_RADIUS):
                if hex_distance(a, b) == 1:
                    self.edge_walls.add(_edge_key(a, b))

        # Aperture obbligatorie: i templi devono avere almeno 1 uscita
        for temple in (TEMPLE_P1_POS, TEMPLE_P2_POS, TEMPLE_P3_POS, TEMPLE_P4_POS):
            for nb in hex_neighbors(*temple):
                if hex_in_radius(*nb, PLAYABLE_RADIUS) and self.is_walkable(*nb):
                    # lascia almeno un vicino senza muro se tutti bloccati
                    pass
            adj = [nb for nb in hex_neighbors(*temple) if hex_in_radius(*nb, PLAYABLE_RADIUS)]
            blocked = [nb for nb in adj if _edge_key(temple, nb) in self.edge_walls]
            if adj and len(blocked) >= len(adj):
                # sblocca il primo
                self.edge_walls.discard(_edge_key(temple, adj[0]))

    def get_tile(self, q: int, r: int) -> Optional[Tile]:
        return self.tiles.get((q, r))

    def get_unit_at(self, q: int, r: int) -> Optional[Unit]:
        return self.units.get((q, r))

    def is_walkable(self, q: int, r: int) -> bool:
        if not hex_in_radius(q, r, HEX_RADIUS):
            return False
        tile = self.tiles.get((q, r))
        if not tile:
            return False
        if tile.tile_type == TileType.FRAME:
            return False
        return True

    def has_edge_wall(self, a: HexPos, b: HexPos) -> bool:
        return _edge_key(a, b) in self.edge_walls

    def get_adjacent(self, q: int, r: int) -> List[HexPos]:
        out = []
        for nq, nr in hex_neighbors(q, r):
            if not self.is_walkable(nq, nr):
                continue
            if self.has_edge_wall((q, r), (nq, nr)):
                continue
            out.append((nq, nr))
        return out

    def place_unit(self, unit: Unit) -> bool:
        q, r = unit.col, unit.row
        if (q, r) not in self.tiles and (unit.row, unit.col) in self.tiles:
            q, r = unit.row, unit.col
        if not self.is_walkable(q, r):
            return False
        if (q, r) in self.units:
            return False
        unit.row = r
        unit.col = q
        self.units[(q, r)] = unit
        return True

    def remove_unit(self, unit: Unit) -> None:
        key = (unit.col, unit.row)
        if key in self.units and self.units[key] is unit:
            del self.units[key]
            return
        key2 = (unit.row, unit.col)
        if key2 in self.units and self.units[key2] is unit:
            del self.units[key2]

    def move_unit(self, unit: Unit, tq: int, tr: int) -> bool:
        if not self.is_walkable(tq, tr):
            return False
        if (tq, tr) in self.units:
            return False
        if self.has_edge_wall((unit.col, unit.row), (tq, tr)):
            return False
        old = (unit.col, unit.row)
        if old not in self.units:
            old = (unit.row, unit.col)
        if old in self.units:
            del self.units[old]
        unit.col, unit.row = tq, tr
        self.units[(tq, tr)] = unit
        return True

    def get_units_of_player(self, player_id: int) -> List[Unit]:
        return [u for u in self.units.values() if u.owner_id == player_id and u.is_alive]

    def resolve_pos(self, coord: str) -> Optional[HexPos]:
        if coord in self._pos_by_flavor:
            return self._pos_by_flavor[coord]
        if "," in coord:
            try:
                q, r = map(int, coord.split(",", 1))
                if (q, r) in self.tiles:
                    return (q, r)
            except ValueError:
                return None
        return None

    def flavor_of(self, q: int, r: int) -> str:
        return self._flavor_by_pos.get((q, r), hex_key(q, r))

    def get_edge_walls_for_ui(self) -> List[dict]:
        out = []
        for a, b in self.edge_walls:
            out.append({
                "a": self.flavor_of(*a),
                "b": self.flavor_of(*b),
                "a_qr": hex_key(*a),
                "b_qr": hex_key(*b),
            })
        return out
