"""
Caricamento e validazione della mappa esagonale da map.json.
Introdotto in v1.0.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from .hex_coords import Hex


# Mapping dei tipi presenti in map.json → nomi interni
TYPE_MAP = {
    "frame": "frame",
    "terrain": "terrain",
    "altar": "altar",
    "temple1": "temple1",
    "temple2": "temple2",
    "temple3": "temple3",
    "temple4": "temple4",
}


class MapData:
    def __init__(self):
        self.version: int = 1
        self.radius: int = 5
        self.playable_radius: int = 4
        self.cells: Dict[Hex, str] = {}          # Hex → tipo (frame, terrain, altar, templeX)
        self.walls: Set[Tuple[Hex, Hex]] = set() # muri come coppie ordinate di Hex
        self.temples: Dict[str, Hex] = {}        # "temple1" → Hex
        self.altar: Optional[Hex] = None

    def is_walkable(self, h: Hex) -> bool:
        t = self.cells.get(h)
        if t is None or t == "frame":
            return False
        return True

    def has_wall_between(self, a: Hex, b: Hex) -> bool:
        """True se esiste un muro tra a e b (ordine indipendente)."""
        pair = tuple(sorted([a, b], key=lambda x: (x.q, x.r)))
        return pair in self.walls

    def get_neighbors(self, h: Hex) -> List[Hex]:
        """Vicini walkable e senza muro in mezzo."""
        result = []
        for n in h.neighbors():
            if self.is_walkable(n) and not self.has_wall_between(h, n):
                result.append(n)
        return result


def load_map(json_path: Optional[str | Path] = None) -> MapData:
    """
    Carica map.json e restituisce un oggetto MapData pronto all'uso.
    Se json_path è None, cerca backend/data/map.json rispetto a questo file.
    """
    if json_path is None:
        # percorso relativo a questo modulo
        base = Path(__file__).resolve().parent.parent  # backend/
        json_path = base / "data" / "map.json"
    else:
        json_path = Path(json_path)

    if not json_path.exists():
        raise FileNotFoundError(f"map.json non trovato: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    md = MapData()
    md.version = raw.get("version", 1)
    md.radius = raw.get("radius", 5)
    md.playable_radius = raw.get("playable_radius", 4)

    # Celle
    for cell in raw.get("cells", []):
        q = cell["q"]
        r = cell["r"]
        t = cell.get("type", "terrain")
        h = Hex(q, r)
        md.cells[h] = t
        if t.startswith("temple"):
            md.temples[t] = h
        if t == "altar":
            md.altar = h

    # Muri (normalizzati come tupla ordinata)
    for w in raw.get("walls", []):
        a = Hex(w["a"][0], w["a"][1])
        b = Hex(w["b"][0], w["b"][1])
        pair = tuple(sorted([a, b], key=lambda x: (x.q, x.r)))
        md.walls.add(pair)

    return md


def validate_map(md: MapData) -> List[str]:
    """Restituisce una lista di errori (vuota se tutto ok)."""
    errors = []
    if md.altar is None:
        errors.append("Manca l'altare centrale")
    if len(md.temples) < 2:
        errors.append(f"Templi trovati: {list(md.temples.keys())} (ne servono almeno 2)")
    if not md.cells:
        errors.append("Nessuna cella caricata")
    return errors
