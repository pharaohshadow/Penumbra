"""
Board - griglia 7×7 con cornice, templi agli angoli e muri edge (v28)
"""

from __future__ import annotations
from typing import List, Optional, Tuple, Dict, Set
from .tile import Tile
from .unit import Unit
from .constants import (
    GRID_SIZE, TileType, ALTAR_POS, TEMPLE_P1_POS, TEMPLE_P2_POS,
    TEMPLE_P3_POS, TEMPLE_P4_POS, PLAYABLE_ROWS, PLAYABLE_COLS,
    pos_to_coord, coord_to_pos, Direction
)


def _edge_key(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Chiave ordinata per un bordo tra due celle adiacenti."""
    return (a, b) if a <= b else (b, a)


class Board:
    def __init__(self):
        self.grid: List[List[Tile]] = [
            [Tile(r, c) for c in range(GRID_SIZE)] for r in range(GRID_SIZE)
        ]
        self.units: Dict[Tuple[int, int], Unit] = {}
        # Muri edge: set di chiavi ((r1,c1),(r2,c2)) ordinate
        self.edge_walls: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
        self._setup_fixed_layout()

    def _setup_fixed_layout(self):
        """Layout 7×7 da map.xlsx dell'utente (v28)."""
        # 1. Tutta la griglia parte come Cornice (non giocabile)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.grid[r][c].tile_type = TileType.FRAME
                self.grid[r][c].explored = True

        # 2. Zona giocabile interna 5×5 (righe 1-5, colonne 1-5) → EMPTY
        for r in PLAYABLE_ROWS:
            for c in PLAYABLE_COLS:
                self.grid[r][c].tile_type = TileType.EMPTY
                self.grid[r][c].explored = False

        # 3. Templi agli angoli
        self.grid[TEMPLE_P1_POS[0]][TEMPLE_P1_POS[1]].tile_type = TileType.TEMPLE_P1
        self.grid[TEMPLE_P1_POS[0]][TEMPLE_P1_POS[1]].owner_id = 0
        self.grid[TEMPLE_P1_POS[0]][TEMPLE_P1_POS[1]].explored = True

        self.grid[TEMPLE_P2_POS[0]][TEMPLE_P2_POS[1]].tile_type = TileType.TEMPLE_P2
        self.grid[TEMPLE_P2_POS[0]][TEMPLE_P2_POS[1]].owner_id = 1
        self.grid[TEMPLE_P2_POS[0]][TEMPLE_P2_POS[1]].explored = True

        # Futuri 4 giocatori (presenti ma non usati)
        self.grid[TEMPLE_P3_POS[0]][TEMPLE_P3_POS[1]].tile_type = TileType.TEMPLE_P3
        self.grid[TEMPLE_P3_POS[0]][TEMPLE_P3_POS[1]].explored = True
        self.grid[TEMPLE_P4_POS[0]][TEMPLE_P4_POS[1]].tile_type = TileType.TEMPLE_P4
        self.grid[TEMPLE_P4_POS[0]][TEMPLE_P4_POS[1]].explored = True

        # 4. Altare al centro della zona MAPPA
        ar, ac = ALTAR_POS
        self.grid[ar][ac].tile_type = TileType.ALTAR
        self.grid[ar][ac].explored = True

        # 5. Muri edge – esattamente i bordi blu dell'xlsx
        # Excel 1-based → 0-based: Excel (row,col) → (row-1, col-1)
        # Bordi rilevati:
        # (2,2) R → tra (1,1)-(1,2)
        # (2,3) B → tra (1,2)-(2,2)
        # (2,4) B → tra (1,3)-(2,3)
        # (3,6) L+T → tra (2,4)-(2,5) e tra (1,5)-(2,5)
        # (4,2) R → tra (3,1)-(3,2)
        # (4,6) L → tra (3,4)-(3,5)
        # (5,2) R → tra (4,1)-(4,2)
        # (6,2) T → tra (4,1)-(5,1)
        # (6,4) T → tra (4,3)-(5,3)
        # (6,5) T → tra (4,4)-(5,4)
        # (6,6) L → tra (5,4)-(5,5)
        edges = [
            ((1, 1), (1, 2)),
            ((1, 2), (2, 2)),
            ((1, 3), (2, 3)),
            ((2, 4), (2, 5)),
            ((1, 5), (2, 5)),
            ((3, 1), (3, 2)),
            ((3, 4), (3, 5)),
            ((4, 1), (4, 2)),
            ((4, 1), (5, 1)),
            ((4, 3), (5, 3)),
            ((4, 4), (5, 4)),
            ((5, 4), (5, 5)),
        ]
        for a, b in edges:
            self.edge_walls.add(_edge_key(a, b))

        # Perimetro zona giocabile (v31): muri tra MAPPA e cornice
        for c in range(1, 6):
            self.edge_walls.add(_edge_key((1, c), (0, c)))  # top
            self.edge_walls.add(_edge_key((5, c), (6, c)))  # bottom
        for r in range(1, 6):
            self.edge_walls.add(_edge_key((r, 1), (r, 0)))  # left
            self.edge_walls.add(_edge_key((r, 5), (r, 6)))  # right
        # Angoli interni playable ↔ frame diagonali non servono (edge walls solo ortogonali)

        # 6. Portali / eventi di base (sulla zona giocabile, posizioni libere)
        # Portale bianco e nero come prima, adattati
        if self.grid[1][1].tile_type == TileType.EMPTY:
            self.grid[1][1].tile_type = TileType.PORTAL_WHITE
            self.grid[1][1].explored = False
        if self.grid[5][5].tile_type == TileType.EMPTY:
            self.grid[5][5].tile_type = TileType.PORTAL_BLACK
            self.grid[5][5].explored = False
        for r, c in [(1, 3), (3, 1), (5, 3)]:
            if self.grid[r][c].tile_type == TileType.EMPTY:
                self.grid[r][c].tile_type = TileType.EVENT
                self.grid[r][c].explored = False

    def has_edge_wall(self, a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        return _edge_key(a, b) in self.edge_walls

    def get_tile(self, row: int, col: int) -> Optional[Tile]:
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return self.grid[row][col]
        return None

    def get_tile_by_coord(self, coord: str) -> Optional[Tile]:
        try:
            r, c = coord_to_pos(coord)
            return self.get_tile(r, c)
        except (ValueError, IndexError):
            return None

    def is_valid_pos(self, row: int, col: int) -> bool:
        return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE

    def is_walkable(self, row: int, col: int) -> bool:
        tile = self.get_tile(row, col)
        if tile is None:
            return False
        return tile.is_walkable

    def get_unit_at(self, row: int, col: int) -> Optional[Unit]:
        return self.units.get((row, col))

    def place_unit(self, unit: Unit) -> bool:
        pos = (unit.row, unit.col)
        if pos in self.units:
            return False
        if not self.is_walkable(unit.row, unit.col):
            return False
        self.units[pos] = unit
        return True

    def remove_unit(self, unit: Unit):
        pos = (unit.row, unit.col)
        if pos in self.units and self.units[pos] is unit:
            del self.units[pos]

    def move_unit(self, unit: Unit, new_row: int, new_col: int) -> bool:
        if not self.is_valid_pos(new_row, new_col):
            return False
        if not self.is_walkable(new_row, new_col):
            return False
        if (new_row, new_col) in self.units:
            return False
        # Blocca se c'è un muro edge tra le due celle (solo per mosse ortogonali)
        old = (unit.row, unit.col)
        new = (new_row, new_col)
        if abs(old[0] - new[0]) + abs(old[1] - new[1]) == 1:  # ortogonale
            if self.has_edge_wall(old, new):
                return False
        # Diagonale: blocca se entrambi i percorsi ortogonali sono murati
        elif abs(old[0] - new[0]) == 1 and abs(old[1] - new[1]) == 1:
            mid1 = (old[0], new[1])
            mid2 = (new[0], old[1])
            if self.has_edge_wall(old, mid1) and self.has_edge_wall(old, mid2):
                return False
            if self.has_edge_wall(mid1, new) and self.has_edge_wall(mid2, new):
                return False
        old_pos = (unit.row, unit.col)
        if old_pos in self.units:
            del self.units[old_pos]
        unit.row = new_row
        unit.col = new_col
        self.units[(new_row, new_col)] = unit
        return True

    def get_adjacent(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Caselle raggiungibili con 1 passo come il re (8 direzioni), rispettando muri edge."""
        result = []
        for d in Direction:
            nr, nc = row + d.value[0], col + d.value[1]
            if not self.is_valid_pos(nr, nc) or not self.is_walkable(nr, nc):
                continue
            # Controllo muro
            if abs(d.value[0]) + abs(d.value[1]) == 1:  # ortogonale
                if self.has_edge_wall((row, col), (nr, nc)):
                    continue
            else:  # diagonale
                mid1 = (row, nc)
                mid2 = (nr, col)
                blocked = (
                    (self.has_edge_wall((row, col), mid1) and self.has_edge_wall((row, col), mid2))
                    or (self.has_edge_wall(mid1, (nr, nc)) and self.has_edge_wall(mid2, (nr, nc)))
                )
                if blocked:
                    continue
            result.append((nr, nc))
        return result

    def get_adjacent_diagonal(self, row: int, col: int) -> List[Tuple[int, int]]:
        return self.get_adjacent(row, col)

    def get_units_of_player(self, owner_id: int) -> List[Unit]:
        return [u for u in self.units.values() if u.owner_id == owner_id]

    def get_edge_walls_for_ui(self) -> List[dict]:
        """Lista di muri per la UI: {from, to, dir}."""
        out = []
        for a, b in self.edge_walls:
            out.append({
                "a": pos_to_coord(*a),
                "b": pos_to_coord(*b),
            })
        return out

    def print_board(self, show_coords: bool = True) -> str:
        lines = []
        header = "    " + "  ".join(f" {c} " for c in COORD_LETTERS)
        lines.append(header)
        lines.append("   +" + "----+" * GRID_SIZE)
        for r in range(GRID_SIZE):
            row_str = f" {COORD_NUMBERS[r]} |"
            for c in range(GRID_SIZE):
                tile = self.grid[r][c]
                unit = self.get_unit_at(r, c)
                if unit:
                    symbol = f"P{unit.owner_id}"
                    if unit.has_fragment:
                        symbol = "👑"
                    cell = f"{symbol:^4}"
                else:
                    cell = f"{str(tile):^4}"
                row_str += cell + "|"
            lines.append(row_str)
            lines.append("   +" + "----+" * GRID_SIZE)
        return "\n".join(lines)


# Import locale per print_board
from .constants import COORD_LETTERS, COORD_NUMBERS
