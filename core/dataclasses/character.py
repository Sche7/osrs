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

    def eval_rank(self, rank: int) -> str:
        """
        Returns
        -------
        str
            The rank formatted with commas.
        """
        if rank == -1:
            return "Unranked"
        else:
            return f"{rank:,d}"

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            A string representation of the character.
        """
        output = ""
        output += f"Username: {self.username}\n"
        output += f"\tCombat level: {self.combat_level:,d}\n"
        output += f"\tTotal level: {self.total_level:,d}\n"
        output += f"\tTotal experience: {self.total_experience:,d}\n"
        output += f"\tTotal rank: {self.eval_rank(self.total_rank)}\n"
        output += "\n"
        output += "\tSkills:\n"
        for skill_name, skill in self.skills.__dict__.items():
            output += f"\t\t{skill_name}: {skill.level}\n"
        return output
