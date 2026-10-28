"""
Costanti e Enum del gioco Penumbra
v1.3 – massima compatibilità con qualsiasi versione di map_board.py
"""

from enum import Enum, auto
from typing import Tuple, List, Any
from dataclasses import dataclass

# ============================================================
# COORDINATE ESAGONALI
# ============================================================

HEX_DIRECTIONS = [
    (+1,  0),  # E
    (+1, -1),  # NE
    ( 0, -1),  # NW
    (-1,  0),  # W
    (-1, +1),  # SW
    ( 0, +1),  # SE
]

HEX_RADIUS = 5
PLAYABLE_RADIUS = 4


@dataclass(frozen=True)
class HexPos:
    """Coordinate assiali di un esagono."""
    q: int
    r: int

    def __str__(self) -> str:
        return f"({self.q},{self.r})"

    def neighbors(self) -> List["HexPos"]:
        return [HexPos(self.q + dq, self.r + dr) for dq, dr in HEX_DIRECTIONS]


def hex_key(q: int, r: int) -> Tuple[int, int]:
    """Restituisce una chiave immutabile per usare (q,r) come chiave di dizionario."""
    return (q, r)


def hex_neighbors(q: int, r: int) -> List[Tuple[int, int]]:
    """Restituisce le 6 celle vicine in coordinate (q, r)."""
    return [(q + dq, r + dr) for dq, dr in HEX_DIRECTIONS]


def hex_distance(q1: int, r1: int, q2: int, r2: int) -> int:
    """Distanza esagonale tra due celle."""
    s1 = -q1 - r1
    s2 = -q2 - r2
    return max(abs(q1 - q2), abs(r1 - r2), abs(s1 - s2))


def hex_in_radius(radius: int) -> List[Tuple[int, int]]:
    """Restituisce tutte le celle entro un certo raggio (incluso il centro)."""
    result = []
    for q in range(-radius, radius + 1):
        r1 = max(-radius, -q - radius)
        r2 = min(radius, -q + radius)
        for r in range(r1, r2 + 1):
            result.append((q, r))
    return result


def all_hexes(radius: int = HEX_RADIUS) -> List[Tuple[int, int]]:
    """Alias di hex_in_radius."""
    return hex_in_radius(radius)


def is_hex_within_radius(q: int, r: int, radius: int) -> bool:
    """True se la cella (q,r) è entro il raggio indicato."""
    return hex_distance(q, r, 0, 0) <= radius


# ============================================================
# VECCHIO SISTEMA 5×5 (ancora in uso)
# ============================================================
GRID_SIZE = 5
COORD_LETTERS = "ABCDE"
COORD_NUMBERS = "12345"

def pos_to_coord(row: int, col: int) -> str:
    return f"{COORD_LETTERS[col]}{COORD_NUMBERS[row]}"

def coord_to_pos(coord: str) -> Tuple[int, int]:
    col = COORD_LETTERS.index(coord[0].upper())
    row = COORD_NUMBERS.index(coord[1])
    return row, col

# ============================================================
# ENUM
# ============================================================

class Color(Enum):
    WHITE = "Bianco"
    BLUE = "Blu"
    RED = "Rosso"
    BLACK = "Nero"
    GREEN = "Verde"
    YELLOW = "Giallo"
    GRAY = "Grigio"

class CardType(Enum):
    MONSTER = "Mostro"
    TRAP = "Trappola"
    CURSE = "Maledizione"
    BOSS = "Boss"
    ELDRAZI = "Mostrissimo"
    FRAGMENT = "Frammento"
    NEUTRAL = "Neutrale"

class TileType(Enum):
    EMPTY = "Vuoto"
    TEMPLE_P1 = "Tempio1"
    TEMPLE_P2 = "Tempio2"
    TEMPLE_1 = "Tempio1"
    TEMPLE_2 = "Tempio2"
    TEMPLE_3 = "Tempio3"
    TEMPLE_4 = "Tempio4"
    ALTAR = "Altare"
    BUFF = "Buff"
    EVENT = "Evento"
    WALL = "Muro"
    PORTAL_WHITE = "PortaleBianco"
    PORTAL_BLACK = "PortaleNero"
    PORTAL_GRAY = "PortaleGrigio"
    PORTAL_UNSTABLE = "PortaleInstabile"
    RITUAL = "CerchioRituale"
    SWAMP = "Palude"
    TOWER = "TorreLancio"
    SANCTUARY = "SantuarioVita"
    FISSURE = "Fenditura"
    ILLUSION_WALL = "MuroIllusione"
    SHADOW_REFUGE = "RifugioOmbroso"
    SPIKE_PIT = "FossaSpine"
    MANA_STEAL = "RunaFurto"
    NEUTRAL_TERRAIN = "TerrenoNeutrale"
    MAGMA = "Magma"
    FRAME = "Cornice"
    TERRAIN = "Terreno"

class Phase(Enum):
    DRAFT = auto()
    SETUP = auto()
    TURN_START = auto()
    MAIN = auto()
    COMBAT = auto()
    END_TURN = auto()
    GAME_OVER = auto()

class Direction(Enum):
    N  = (-1, 0)
    S  = (1, 0)
    E  = (0, 1)
    W  = (0, -1)
    NE = (-1, 1)
    NW = (-1, -1)
    SE = (1, 1)
    SW = (1, -1)

# Mana / Frammenti
MANA_CAP = 6
STARTING_MANA = 1
FRAGMENT_COSTS = [0, 3, 6]

# Coordinate speciali legacy
ALTAR_POS = (2, 2)
TEMPLE_P1_POSITIONS = [(4, 1), (4, 2), (4, 3)]
TEMPLE_P2_POSITIONS = [(0, 1), (0, 2), (0, 3)]

ANSI = {
    "reset": "\033[0m", "bold": "\033[1m",
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
    "white": "\033[97m", "gray": "\033[90m",
}
