"""
Tile - singola casella della griglia 5x5
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Any
from .constants import TileType
from .unit import Unit


@dataclass
class Tile:
    row: int
    col: int
    tile_type: TileType = TileType.EMPTY
    explored: bool = False
    # Effetti permanenti / temporanei
    permanent_effect: Optional[str] = None   # es. "swamp", "magma:2", "sanctuary"
    trap_card_id: Optional[int] = None       # se c'è una trappola nascosta
    wall_hp: int = 0                         # per Muro d'Illusione
    owner_id: Optional[int] = None           # per zone di spawn o effetti proprietari

    @property
    def coord(self) -> str:
        from .constants import pos_to_coord
        return pos_to_coord(self.row, self.col)

    @property
    def is_walkable(self) -> bool:
        if self.tile_type == TileType.WALL:
            return False
        if self.tile_type == TileType.ILLUSION_WALL and self.wall_hp > 0:
            return False
        return True

    @property
    def is_portal(self) -> bool:
        return self.tile_type in (
            TileType.PORTAL_WHITE, TileType.PORTAL_BLACK,
            TileType.PORTAL_GRAY, TileType.PORTAL_UNSTABLE
        )

    @property
    def is_ritual(self) -> bool:
        return self.tile_type == TileType.RITUAL or (
            self.tile_type == TileType.BUFF and "ritual" in (self.permanent_effect or "")
        )

    def __str__(self) -> str:
        symbols = {
            TileType.EMPTY: "·",
            TileType.TEMPLE_P1: "T1",
            TileType.TEMPLE_P2: "T2",
            TileType.ALTAR: "A",
            TileType.BUFF: "B",
            TileType.EVENT: "?",
            TileType.WALL: "█",
            TileType.PORTAL_WHITE: "○",
            TileType.PORTAL_BLACK: "●",
            TileType.PORTAL_GRAY: "◎",
            TileType.PORTAL_UNSTABLE: "◉",
            TileType.RITUAL: "✧",
            TileType.SWAMP: "~",
            TileType.MAGMA: "▲",
            TileType.SANCTUARY: "+",
            TileType.FISSURE: "V",
            TileType.ILLUSION_WALL: "▓",
            TileType.SHADOW_REFUGE: "▒",
            TileType.SPIKE_PIT: "‡",
            TileType.MANA_STEAL: "¤",
            TileType.NEUTRAL_TERRAIN: "·",
            TileType.TOWER: "↑",
        }
        return symbols.get(self.tile_type, "?")
