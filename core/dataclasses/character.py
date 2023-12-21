from dataclasses import dataclass


@dataclass
class Skill:
    level: int = 1
    experience: float = 0
    rank: int = -1  # -1 means unranked


@dataclass
class Skills:
    attack: Skill = Skill()
    defence: Skill = Skill()
    strength: Skill = Skill()
    hitpoints: Skill = Skill(0, 10)  # Hitpoints starts at level 10
    ranged: Skill = Skill()
    prayer: Skill = Skill()
    magic: Skill = Skill()
    cooking: Skill = Skill()
    woodcutting: Skill = Skill()
    fletching: Skill = Skill()
    fishing: Skill = Skill()
    firemaking: Skill = Skill()
    crafting: Skill = Skill()
    smithing: Skill = Skill()
    mining: Skill = Skill()
    herblore: Skill = Skill()
    agility: Skill = Skill()
    thieving: Skill = Skill()
    slayer: Skill = Skill()
    farming: Skill = Skill()
    runecrafting: Skill = Skill()
    hunter: Skill = Skill()
    construction: Skill = Skill()


@dataclass
class Character:
    username: str
    combat_level: int = 3
    total_level: int = 32
    total_experience: int = 0
    total_rank: int = -1  # -1 means unranked
    skills: Skills = Skills()
