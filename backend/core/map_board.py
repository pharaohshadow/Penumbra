"""
Board - griglia 5x5 con layout a meandro/girandola del GDD
"""

from __future__ import annotations
from typing import List, Optional, Tuple, Dict
from .tile import Tile
from .unit import Unit
from .constants import (
    GRID_SIZE, TileType, ALTAR_POS, TEMPLE_P1_POSITIONS, TEMPLE_P2_POSITIONS,
    pos_to_coord, coord_to_pos, Direction
)


class Board:
    def __init__(self):
        self.grid: List[List[Tile]] = [
            [Tile(r, c) for c in range(GRID_SIZE)] for r in range(GRID_SIZE)
        ]
        self.units: Dict[Tuple[int, int], Unit] = {}  # pos -> Unit
        self._setup_fixed_layout()

    def _setup_fixed_layout(self):
        """Layout definitivo descritto nel GDD."""
        # Tempio giocatore 1 (basso - umano) - riga 4
        for r, c in TEMPLE_P1_POSITIONS:
            self.grid[r][c].tile_type = TileType.TEMPLE_P1
            self.grid[r][c].owner_id = 0

        # Tempio giocatore 2 (alto - IA) - riga 0
        for r, c in TEMPLE_P2_POSITIONS:
            self.grid[r][c].tile_type = TileType.TEMPLE_P2
            self.grid[r][c].owner_id = 1

        # Altare centrale C3
        ar, ac = ALTAR_POS
        self.grid[ar][ac].tile_type = TileType.ALTAR
        self.grid[ar][ac].explored = True

        # Angoli Buff + Cerchio Rituale (gialli)
        corners = [(0, 0), (0, 4), (4, 0), (4, 4)]
        for r, c in corners:
            self.grid[r][c].tile_type = TileType.BUFF
            self.grid[r][c].permanent_effect = "ritual"
            self.grid[r][c].explored = True

        # Muri a girandola/meandro (esempio realistico basato sulla descrizione)
        # I muri corrono lungo i bordi tra caselle formando un percorso a chiocciola attorno a C3.
        # Per semplicità di prototipo usiamo muri su caselle intere che bloccano il passaggio.
        # In versione finale i muri saranno "edge walls" (tra caselle).
        wall_positions = [
            (1, 1), (1, 3),
            (2, 0), (2, 4),
            (3, 1), (3, 3),
        ]
        for r, c in wall_positions:
            if self.grid[r][c].tile_type == TileType.EMPTY:
                self.grid[r][c].tile_type = TileType.WALL

        # Eventi / Portali (rosa) - posizioni tipiche non occupate
        event_candidates = [(0, 2), (1, 0), (1, 4), (2, 1), (2, 3), (3, 0), (3, 4), (4, 2)]
        # Mettiamo 2 portali obbligatori + qualche evento
        self.grid[1][0].tile_type = TileType.PORTAL_WHITE
        self.grid[1][0].explored = False
        self.grid[3][4].tile_type = TileType.PORTAL_BLACK
        self.grid[3][4].explored = False
        # Altri eventi da esplorare
        for r, c in [(0, 2), (2, 1), (4, 2)]:
            if self.grid[r][c].tile_type == TileType.EMPTY:
                self.grid[r][c].tile_type = TileType.EVENT
                self.grid[r][c].explored = False

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
        return tile is not None and tile.is_walkable

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
            return False  # occupata → sarà gestito come combattimento dal GameState
        old_pos = (unit.row, unit.col)
        if old_pos in self.units:
            del self.units[old_pos]
        unit.row = new_row
        unit.col = new_col
        self.units[(new_row, new_col)] = unit
        return True

    def get_adjacent(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Caselle raggiungibili con 1 passo come il re degli scacchi (8 direzioni)."""
        result = []
        for d in Direction:
            nr, nc = row + d.value[0], col + d.value[1]
            if self.is_valid_pos(nr, nc) and self.is_walkable(nr, nc):
                result.append((nr, nc))
        return result

    def get_adjacent_diagonal(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Compatibilità: ora equivale a get_adjacent (movimento re)."""
        return self.get_adjacent(row, col)

    def get_units_of_player(self, owner_id: int) -> List[Unit]:
        return [u for u in self.units.values() if u.owner_id == owner_id]

    def print_board(self, show_coords: bool = True) -> str:
        """Rappresentazione ASCII della mappa."""
        lines = []
        header = "    " + "  ".join(f" {c} " for c in "ABCDE")
        lines.append(header)
        lines.append("   +" + "----+" * GRID_SIZE)

        for r in range(GRID_SIZE):
            row_str = f" {r+1} |"
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
