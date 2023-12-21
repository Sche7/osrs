from core.dataclasses.skills import Skills
from dataclasses import dataclass


@dataclass
class Character:
    username: str
    skills: Skills = Skills()
    combat_level: int = 3
    total_level: int = 32
    quest_points: int = 0
