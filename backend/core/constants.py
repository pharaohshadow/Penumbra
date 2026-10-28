"""
Costanti globali – Penumbra v33 (mappa esagonale pointy-top)
"""
from __future__ import annotations
from enum import Enum
from typing import Tuple, List, Dict, Optional

# --- Hex grid (axial q, r) pointy-top ---
HEX_RADIUS = 3  # ~37 esagoni (vicino/sopra alla vecchia zona 5×5)

# 6 direzioni axial pointy-top
HEX_DIRS = [
    (+1,  0),  # E
    (+1, -1),  # NE
    ( 0, -1),  # NW
    (-1,  0),  # W
    (-1, +1),  # SW
    ( 0, +1),  # SE
]

HexPos = Tuple[int, int]  # (q, r)


def hex_s(q: int, r: int) -> int:
    return -q - r


def hex_distance(a: HexPos, b: HexPos) -> int:
    aq, ar = a
    bq, br = b
    return (abs(aq - bq) + abs(ar - br) + abs(hex_s(aq, ar) - hex_s(bq, br))) // 2


def hex_neighbors(q: int, r: int) -> List[HexPos]:
    return [(q + dq, r + dr) for dq, dr in HEX_DIRS]


def hex_in_radius(q: int, r: int, radius: int = HEX_RADIUS) -> bool:
    return hex_distance((0, 0), (q, r)) <= radius


def all_hexes(radius: int = HEX_RADIUS) -> List[HexPos]:
    cells = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            if hex_in_radius(q, r, radius):
                cells.append((q, r))
    return cells


# Pixel layout pointy-top (per UI)
def hex_to_pixel(q: int, r: int, size: float = 28.0) -> Tuple[float, float]:
    x = size * (3 ** 0.5) * (q + r / 2.0)
    y = size * (3 / 2.0) * r
    return x, y


# Compatibilità legacy (alcuni import usano ancora questi nomi)
GRID_SIZE = HEX_RADIUS * 2 + 1  # 7
COORD_LETTERS = "ABCDEFG"
COORD_NUMBERS = "0123456"


def pos_to_coord(row: int, col: int) -> str:
    """Legacy – preferire hex_key."""
    if 0 <= row < len(COORD_NUMBERS) and 0 <= col < len(COORD_LETTERS):
        return f"{COORD_LETTERS[col]}{COORD_NUMBERS[row]}"
    return f"{col},{row}"


def coord_to_pos(coord: str) -> Tuple[int, int]:
    """Accetta 'A3' legacy oppure 'q,r' axial."""
    coord = coord.strip()
    if "," in coord:
        q, r = coord.split(",", 1)
        return int(q), int(r)
    if len(coord) >= 2 and coord[0].upper() in COORD_LETTERS:
        col = COORD_LETTERS.index(coord[0].upper())
        row = COORD_NUMBERS.index(coord[1])
        return row, col
    raise ValueError(f"Coordinata non valida: {coord}")


def hex_key(q: int, r: int) -> str:
    return f"{q},{r}"


def parse_hex_key(key: str) -> HexPos:
    q, r = key.split(",", 1)
    return int(q), int(r)


class Color(Enum):
    WHITE = "Bianco"
    BLUE = "Blu"
    BLACK = "Nero"
    RED = "Rosso"
    GREEN = "Verde"
    YELLOW = "Giallo"
    GRAY = "Grigio"


class CardType(Enum):
    MONSTER = "Mostro"
    BOSS = "Boss"
    CURSE = "Maledizione"
    TRAP = "Trappola"
    ELDRAZI = "Mostrissimo"
    NEUTRAL = "Neutrale"
    FRAGMENT = "Frammento"


class TileType(Enum):
    EMPTY = "Terreno"          # terreno base
    TEMPLE_P1 = "Tempio1"      # basso (sud)
    TEMPLE_P2 = "Tempio2"      # alto (nord)
    TEMPLE_P3 = "Tempio3"      # sinistra (ovest) – futuro
    TEMPLE_P4 = "Tempio4"      # destra (est) – futuro
    ALTAR = "Altare"
    FRAME = "Cornice"          # non usato in hex
    ILLUSION_WALL = "MuroIllusione"
    NEUTRAL_TERRAIN = "TerrenoNeutrale"


class Phase(Enum):
    DRAFT = "DRAFT"
    SETUP = "SETUP"
    TURN_START = "TURN_START"
    MAIN = "MAIN"
    GAME_OVER = "GAME_OVER"


class Direction(Enum):
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"


MANA_CAP = 10
FRAGMENT_COSTS = [0, 3, 6]

# Posizioni axial (q, r) – radius 3
ALTAR_POS: HexPos = (0, 0)
TEMPLE_P1_POS: HexPos = (0, 3)    # sud – giocatore 0
TEMPLE_P2_POS: HexPos = (0, -3)   # nord – giocatore 1
TEMPLE_P3_POS: HexPos = (-3, 0)   # ovest – futuro
TEMPLE_P4_POS: HexPos = (3, -3)   # est – futuro

TEMPLE_P1_POSITIONS = [TEMPLE_P1_POS]
TEMPLE_P2_POSITIONS = [TEMPLE_P2_POS]

# Nomi flavor (ambiente) – assegnati alle caselle terreno
FLAVOR_NAMES = [
    "Palude", "Montagna", "Fiume", "Bosco", "Collina", "Rovine",
    "Brughiera", "Gola", "Lago", "Sentiero", "Cripta", "Radura",
    "Crepaccio", "Torrente", "Ciglio", "Nebbia", "Alture", "Bassura",
    "Catacombe", "Sorgente", "Rupe", "Valle", "Ponte", "Arena",
    "Ossario", "Giardino", "Forgia", "Osservatorio", "Reliquiario",
    "Anfratto", "Duna", "Marea",
]
