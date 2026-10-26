"""
Costanti e Enum del gioco Tactical Card Game 5x5
"""

from enum import Enum, auto
from typing import Tuple

# Griglia
GRID_SIZE = 5
COORD_LETTERS = "ABCDE"
COORD_NUMBERS = "12345"

def pos_to_coord(row: int, col: int) -> str:
    """Converte (row, col) 0-based in coordinata tipo 'C3'"""
    return f"{COORD_LETTERS[col]}{COORD_NUMBERS[row]}"

def coord_to_pos(coord: str) -> Tuple[int, int]:
    """Converte 'C3' in (row, col) 0-based"""
    col = COORD_LETTERS.index(coord[0].upper())
    row = COORD_NUMBERS.index(coord[1])
    return row, col

class Color(Enum):
    WHITE = "Bianco"
    BLUE = "Blu"
    RED = "Rosso"
    BLACK = "Nero"
    GREEN = "Verde"
    GRAY = "Grigio"  # Eldrazzi / Neutrali

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
    TEMPLE_P1 = "Tempio1"      # Spawn giocatore basso (umano)
    TEMPLE_P2 = "Tempio2"      # Spawn giocatore alto (IA)
    ALTAR = "Altare"            # C3 Evoluzione
    BUFF = "Buff"               # Angoli gialli + Cerchio Rituale
    EVENT = "Evento"            # Rosa (da esplorare)
    WALL = "Muro"               # Nero divisore
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

class Phase(Enum):
    DRAFT = auto()
    SETUP = auto()
    TURN_START = auto()
    MAIN = auto()
    COMBAT = auto()
    END_TURN = auto()
    GAME_OVER = auto()

class Direction(Enum):
    """Direzioni diagonali (movimento base)"""
    NE = (-1, 1)   # Nord-Est
    NW = (-1, -1)  # Nord-Ovest
    SE = (1, 1)    # Sud-Est
    SW = (1, -1)   # Sud-Ovest

# Mana
MANA_CAP = 6
STARTING_MANA = 1

# Frammenti
FRAGMENT_COSTS = [0, 3, 6]  # Commander Tax

# Coordinate speciali
ALTAR_POS = (2, 2)  # C3
TEMPLE_P1_POSITIONS = [(4, 1), (4, 2), (4, 3)]  # Zona spawn basso (approssimativa, da rifinire)
TEMPLE_P2_POSITIONS = [(0, 1), (0, 2), (0, 3)]  # Zona spawn alto

# Colori ANSI per console
ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "gray": "\033[90m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
    "bg_magenta": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_white": "\033[47m",
    "bg_gray": "\033[100m",
}
