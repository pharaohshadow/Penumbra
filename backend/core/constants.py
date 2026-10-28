"""
Costanti e Enum del gioco Penumbra
v1.5 – aggiunto parse_hex_key (fix ImportError che bloccava Render)
"""

from enum import Enum, auto
from typing import Tuple, List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import json

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

# Posizioni speciali (coordinate assiali)
ALTAR_POS: Tuple[int, int] = (0, 0)
TEMPLE_P1_POS: Tuple[int, int] = (-3, 4)   # da map.json temple1
TEMPLE_P2_POS: Tuple[int, int] = (3, -4)   # temple2
TEMPLE_P3_POS: Tuple[int, int] = (-4, 0)   # temple3
TEMPLE_P4_POS: Tuple[int, int] = (4, 0)    # temple4

# Alias legacy (per compatibilità con codice vecchio)
TEMPLE_P1_POSITIONS = [TEMPLE_P1_POS]
TEMPLE_P2_POSITIONS = [TEMPLE_P2_POS]
ALTAR_POS_LEGACY = (2, 2)  # vecchio 5x5


@dataclass(frozen=True)
class HexPos:
    q: int
    r: int

    def __str__(self) -> str:
        return f"({self.q},{self.r})"

    def __le__(self, other: "HexPos") -> bool:
        return (self.q, self.r) <= (other.q, other.r)

    def neighbors(self) -> List["HexPos"]:
        return [HexPos(self.q + dq, self.r + dr) for dq, dr in HEX_DIRECTIONS]


def hex_key(q: int, r: int) -> Tuple[int, int]:
    return (q, r)


def parse_hex_key(key) -> Tuple[int, int]:
    """
    Accetta (q, r), 'q,r', HexPos o oggetto con .q/.r
    e restituisce sempre la tupla (q, r).
    """
    if isinstance(key, tuple) and len(key) == 2:
        return int(key[0]), int(key[1])
    if isinstance(key, str) and "," in key:
        parts = key.split(",", 1)
        return int(parts[0].strip()), int(parts[1].strip())
    if hasattr(key, "q") and hasattr(key, "r"):
        return int(key.q), int(key.r)
    raise ValueError(f"Impossibile interpretare hex key: {key!r}")


def hex_neighbors(q: int, r: int) -> List[Tuple[int, int]]:
    return [(q + dq, r + dr) for dq, dr in HEX_DIRECTIONS]


def hex_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    q1, r1 = a
    q2, r2 = b
    s1 = -q1 - r1
    s2 = -q2 - r2
    return max(abs(q1 - q2), abs(r1 - r2), abs(s1 - s2))


def hex_in_radius(radius: int) -> List[Tuple[int, int]]:
    result = []
    for q in range(-radius, radius + 1):
        r1 = max(-radius, -q - radius)
        r2 = min(radius, -q + radius)
        for r in range(r1, r2 + 1):
            result.append((q, r))
    return result


def all_hexes(radius: int = HEX_RADIUS) -> List[Tuple[int, int]]:
    return hex_in_radius(radius)


# ============================================================
# CARICAMENTO MAPPA UTENTE
# ============================================================

def load_user_map() -> Optional[Dict[str, Any]]:
    """Carica backend/data/map.json se esiste."""
    candidates = [
        Path(__file__).resolve().parent.parent / "data" / "map.json",
        Path("backend/data/map.json"),
        Path("data/map.json"),
    ]
    for p in candidates:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                continue
    return None


# Nomi "flavor" per le caselle di terreno
FLAVOR_NAMES = [
    "Pianura", "Collina", "Bosco", "Lago", "Rovina", "Palude",
    "Cava", "Altura", "Sentiero", "Radura", "Anfratto", "Sorgente",
    "Crocevia", "Osservatorio", "Campo", "Rifugio", "Promontorio",
]


# ============================================================
# VECCHIO SISTEMA 5×5 (ancora referenziato da alcuni moduli)
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
    TEMPLE_P3 = "Tempio3"
    TEMPLE_P4 = "Tempio4"
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

ANSI = {
    "reset": "\033[0m", "bold": "\033[1m",
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
    "white": "\033[97m", "gray": "\033[90m",
}
