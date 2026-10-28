"""
Tile - singola casella della griglia 7×7
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Any
from .constants import TileType
# from .unit import Unit  # unused


@dataclass
class Tile:
    row: int
    col: int
    tile_type: TileType = TileType.EMPTY
    explored: bool = False
    permanent_effect: Optional[str] = None
    trap_card_id: Optional[int] = None
    wall_hp: int = 0
    owner_id: Optional[int] = None
    has_artifact: bool = False  # artefatto del Signore (v30)

    @property
    def coord(self) -> str:
        from .constants import pos_to_coord
        return pos_to_coord(self.row, self.col)

    @property
    def is_walkable(self) -> bool:
        # Cornice e muri-cella non sono camminabili
        if self.tile_type in (TileType.FRAME, TileType.WALL):
            return False
        if self.tile_type == TileType.ILLUSION_WALL and self.wall_hp > 0:
            return False
        # Templi, Altare, EMPTY, EVENT, PORTAL, BUFF ecc. sono camminabili
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
            TileType.FRAME: " ",
            TileType.TEMPLE_P1: "T1",
            TileType.TEMPLE_P2: "T2",
            TileType.TEMPLE_P3: "T3",
            TileType.TEMPLE_P4: "T4",
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
