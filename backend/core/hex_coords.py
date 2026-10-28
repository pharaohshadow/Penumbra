"""
Sistema di coordinate esagonali (axial coordinates).
Usato dalla nuova mappa Penumbra a partire da v1.0.
"""

from __future__ import annotations
from typing import Tuple, List, Iterable
from dataclasses import dataclass


# Direzioni esagonali (axial): E, NE, NW, W, SW, SE
HEX_DIRECTIONS = [
    (+1,  0),  # E
    (+1, -1),  # NE
    ( 0, -1),  # NW
    (-1,  0),  # W
    (-1, +1),  # SW
    ( 0, +1),  # SE
]


@dataclass(frozen=True)
class Hex:
    """Coordinate assiali di un esagono."""
    q: int
    r: int

    def __post_init__(self):
        # s = -q - r (utile per debug / cube conversion)
        pass

    @property
    def s(self) -> int:
        return -self.q - self.r

    def neighbor(self, direction_index: int) -> "Hex":
        dq, dr = HEX_DIRECTIONS[direction_index % 6]
        return Hex(self.q + dq, self.r + dr)

    def neighbors(self) -> List["Hex"]:
        return [self.neighbor(i) for i in range(6)]

    def distance(self, other: "Hex") -> int:
        """Distanza esagonale (cube distance)."""
        return max(
            abs(self.q - other.q),
            abs(self.r - other.r),
            abs(self.s - other.s),
        )

    def __add__(self, other: "Hex") -> "Hex":
        return Hex(self.q + other.q, self.r + other.r)

    def __sub__(self, other: "Hex") -> "Hex":
        return Hex(self.q - other.q, self.r - other.r)

    def __str__(self) -> str:
        return f"({self.q},{self.r})"

    def __repr__(self) -> str:
        return f"Hex(q={self.q}, r={self.r})"


def hex_from_tuple(t: Tuple[int, int]) -> Hex:
    return Hex(t[0], t[1])


def all_hexes_in_radius(radius: int) -> List[Hex]:
    """Restituisce tutti gli esagoni entro un certo raggio (incluso)."""
    result = []
    for q in range(-radius, radius + 1):
        r1 = max(-radius, -q - radius)
        r2 = min(radius, -q + radius)
        for r in range(r1, r2 + 1):
            result.append(Hex(q, r))
    return result


def is_within_radius(h: Hex, radius: int) -> bool:
    return h.distance(Hex(0, 0)) <= radius
