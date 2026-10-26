"""
Unit - una creatura (o struttura) sul tabellone
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Set
from .card import Card
from .constants import Color


@dataclass
class Unit:
    card: Card
    owner_id: int                  # 0 = umano (basso), 1 = IA (alto)
    row: int
    col: int
    current_hp: int
    current_atk: int
    has_fragment: bool = False     # ha la Corona / Frammento
    fragment_index: int = -1       # 0, 1 o 2
    statuses: Set[str] = field(default_factory=set)  # "shield:2", "stun", "invulnerable", "charge_used", ...
    summoning_sickness: bool = False
    can_attack_this_turn: bool = True
    moved_this_turn: bool = False

    def __post_init__(self):
        if self.current_hp <= 0:
            self.current_hp = self.card.hp
        if self.current_atk <= 0:
            self.current_atk = self.card.atk

    @property
    def pos(self) -> tuple[int, int]:
        return (self.row, self.col)

    @property
    def coord(self) -> str:
        from .constants import pos_to_coord
        return pos_to_coord(self.row, self.col)

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    @property
    def is_creature(self) -> bool:
        return self.card.is_creature()

    def take_damage(self, amount: int, source: Optional[Unit] = None) -> int:
        """Applica danno tenendo conto di scudi e status. Ritorna danno effettivo."""
        if "invulnerable" in self.statuses:
            return 0
        # Riduzione danno generica
        if "ReduceDamage1" in self.card.keywords:
            amount = max(0, amount - 1)
        # Scudo
        for s in list(self.statuses):
            if s.startswith("shield:"):
                shield_val = int(s.split(":")[1])
                absorbed = min(shield_val, amount)
                amount -= absorbed
                new_shield = shield_val - absorbed
                self.statuses.discard(s)
                if new_shield > 0:
                    self.statuses.add(f"shield:{new_shield}")
                break
        self.current_hp -= amount
        return amount

    def heal(self, amount: int):
        self.current_hp = min(self.current_hp + amount, self.card.hp + self._bonus_max_hp())

    def _bonus_max_hp(self) -> int:
        bonus = 0
        for s in self.statuses:
            if s.startswith("maxhp:"):
                bonus += int(s.split(":")[1])
        return bonus

    def has_keyword(self, kw: str) -> bool:
        return kw in self.card.keywords

    def __str__(self) -> str:
        crown = "👑" if self.has_fragment else ""
        return f"{crown}{self.card.name}({self.current_atk}/{self.current_hp})@{self.coord}[P{self.owner_id}]"
