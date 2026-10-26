"""
Player - stato di un giocatore
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Set
from .card import Card
from .unit import Unit
from .constants import FRAGMENT_COSTS, Color


@dataclass
class Player:
    id: int                          # 0 = umano (basso), 1 = IA (alto)
    name: str
    mana: int = 1
    mana_max: int = 1
    hand: List[Card] = field(default_factory=list)
    fragments_remaining: int = 3     # 3 vite
    crown_unit: Optional[Unit] = None
    colors: Set[Color] = field(default_factory=set)  # colori scelti nel draft
    is_ai: bool = False
    has_lost: bool = False

    def can_afford(self, cost: int) -> bool:
        return self.mana >= cost

    def spend_mana(self, amount: int) -> bool:
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def refresh_mana(self):
        self.mana = self.mana_max

    def increase_mana_max(self, amount: int = 2):
        from .constants import MANA_CAP
        self.mana_max = min(self.mana_max + amount, MANA_CAP)

    def next_fragment_cost(self) -> Optional[int]:
        used = 3 - self.fragments_remaining
        if used >= 3:
            return None
        return FRAGMENT_COSTS[used]

    def can_place_fragment(self) -> bool:
        return self.fragments_remaining > 0 and self.next_fragment_cost() is not None

    def place_fragment(self, unit: Unit) -> bool:
        cost = self.next_fragment_cost()
        if cost is None or not self.can_afford(cost):
            return False
        self.spend_mana(cost)
        self.fragments_remaining -= 1
        unit.has_fragment = True
        unit.fragment_index = 3 - self.fragments_remaining - 1
        if self.crown_unit:
            self.crown_unit.has_fragment = False
        self.crown_unit = unit
        return True

    def lose_fragment(self):
        """Chiamato quando la creatura incoronata muore."""
        if self.crown_unit:
            self.crown_unit.has_fragment = False
            self.crown_unit = None

    def check_defeat(self) -> bool:
        """Se a fine turno non ha un frammento in campo → sconfitta."""
        if self.crown_unit is None or not self.crown_unit.is_alive:
            self.has_lost = True
            return True
        return False

    def __str__(self) -> str:
        return (f"{self.name} (P{self.id}) | Mana {self.mana}/{self.mana_max} | "
                f"Frammenti {self.fragments_remaining}/3 | Carte in mano {len(self.hand)}")
