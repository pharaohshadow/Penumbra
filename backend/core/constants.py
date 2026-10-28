"""
Costanti e Enum del gioco Tactical Card Game – griglia 7×7 (v28)
"""

from enum import Enum, auto
from typing import Tuple

# Griglia 7×7 (cornice + zona giocabile 5×5 interna)
GRID_SIZE = 7
COORD_LETTERS = "ABCDEFG"
COORD_NUMBERS = "0123456"

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
    YELLOW = "Giallo"  # Meta: carte random dagli altri 5, bordo giallo in UI
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
    EMPTY = "Vuoto"           # casella giocabile vuota
    FRAME = "Cornice"         # bordo esterno non giocabile
    TEMPLE_P1 = "Tempio1"     # Spawn giocatore 0 (umano) – angolo basso-sinistra
    TEMPLE_P2 = "Tempio2"     # Spawn giocatore 1 (IA) – angolo alto-destra
    TEMPLE_P3 = "Tempio3"     # futuro 4 giocatori
    TEMPLE_P4 = "Tempio4"     # futuro 4 giocatori
    ALTAR = "Altare"          # centro zona MAPPA – Evoluzione
    BUFF = "Buff"             # Cerchio Rituale / angoli gialli
    EVENT = "Evento"          # Rosa (da esplorare)
    WALL = "Muro"             # legacy cell-wall (non più usato come cella)
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
    """Direzioni movimento base (re degli scacchi: 8 caselle adiacenti)"""
    N  = (-1, 0)
    S  = (1, 0)
    E  = (0, 1)
    W  = (0, -1)
    NE = (-1, 1)
    NW = (-1, -1)
    SE = (1, 1)
    SW = (1, -1)

# Mana
MANA_CAP = 6
STARTING_MANA = 1

# Frammenti
FRAGMENT_COSTS = [0, 3, 6]  # Commander Tax

# Coordinate speciali (0-based, griglia 7×7)
# Excel: riga1=alto → row0, colonna1=sinistra → col0
ALTAR_POS = (3, 3)                 # centro zona MAPPA
TEMPLE_P1_POS = (6, 0)             # basso-sinistra (umano)
TEMPLE_P2_POS = (0, 6)             # alto-destra (IA)
TEMPLE_P3_POS = (6, 6)             # basso-destra (futuro)
TEMPLE_P4_POS = (0, 0)             # alto-sinistra (futuro)

# Compatibilità con codice che si aspetta liste
TEMPLE_P1_POSITIONS = [TEMPLE_P1_POS]
TEMPLE_P2_POSITIONS = [TEMPLE_P2_POS]

# Zona giocabile interna (righe/colonne 1..5)
PLAYABLE_ROWS = range(1, 6)
PLAYABLE_COLS = range(1, 6)

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
