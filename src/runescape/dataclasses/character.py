import datetime
from dataclasses import dataclass

DATETIME_FORMAT = "%b %d %Y %H:%M:%S"


@dataclass
class Skill:
    level: int = -1
    experience: float = 0
    rank: int = -1  # -1 means unranked


@dataclass
class Skills:
    attack: Skill = Skill()
    defence: Skill = Skill()
    strength: Skill = Skill()
    hitpoints: Skill = Skill(level=0, experience=10)  # Hitpoints starts at level 10
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

    def __sub__(self, other: "Skills") -> "Skills":
        """
        Subtract the levels of two Skills objects.
        """
        return Skills(
            attack=Skill(
                level=self.attack.level - other.attack.level,
                experience=self.attack.experience - other.attack.experience,
                rank=min(self.attack.rank, other.attack.rank),
            ),
            defence=Skill(
                level=self.defence.level - other.defence.level,
                experience=self.defence.experience - other.defence.experience,
                rank=min(self.defence.rank, other.defence.rank),
            ),
            strength=Skill(
                level=self.strength.level - other.strength.level,
                experience=self.strength.experience - other.strength.experience,
                rank=min(self.strength.rank, other.strength.rank),
            ),
            hitpoints=Skill(
                level=self.hitpoints.level - other.hitpoints.level,
                experience=self.hitpoints.experience - other.hitpoints.experience,
                rank=min(self.hitpoints.rank, other.hitpoints.rank),
            ),
            ranged=Skill(
                level=self.ranged.level - other.ranged.level,
                experience=self.ranged.experience - other.ranged.experience,
                rank=min(self.ranged.rank, other.ranged.rank),
            ),
            prayer=Skill(
                level=self.prayer.level - other.prayer.level,
                experience=self.prayer.experience - other.prayer.experience,
                rank=min(self.prayer.rank, other.prayer.rank),
            ),
            magic=Skill(
                level=self.magic.level - other.magic.level,
                experience=self.magic.experience - other.magic.experience,
                rank=min(self.magic.rank, other.magic.rank),
            ),
            cooking=Skill(
                level=self.cooking.level - other.cooking.level,
                experience=self.cooking.experience - other.cooking.experience,
                rank=min(self.cooking.rank, other.cooking.rank),
            ),
            woodcutting=Skill(
                level=self.woodcutting.level - other.woodcutting.level,
                experience=self.woodcutting.experience - other.woodcutting.experience,
                rank=min(self.woodcutting.rank, other.woodcutting.rank),
            ),
            fletching=Skill(
                level=self.fletching.level - other.fletching.level,
                experience=self.fletching.experience - other.fletching.experience,
                rank=min(self.fletching.rank, other.fletching.rank),
            ),
            fishing=Skill(
                level=self.fishing.level - other.fishing.level,
                experience=self.fishing.experience - other.fishing.experience,
                rank=min(self.fishing.rank, other.fishing.rank),
            ),
            firemaking=Skill(
                level=self.firemaking.level - other.firemaking.level,
                experience=self.firemaking.experience - other.firemaking.experience,
                rank=min(self.firemaking.rank, other.firemaking.rank),
            ),
            crafting=Skill(
                level=self.crafting.level - other.crafting.level,
                experience=self.crafting.experience - other.crafting.experience,
                rank=min(self.crafting.rank, other.crafting.rank),
            ),
            smithing=Skill(
                level=self.smithing.level - other.smithing.level,
                experience=self.smithing.experience - other.smithing.experience,
                rank=min(self.smithing.rank, other.smithing.rank),
            ),
            mining=Skill(
                level=self.mining.level - other.mining.level,
                experience=self.mining.experience - other.mining.experience,
                rank=min(self.mining.rank, other.mining.rank),
            ),
            herblore=Skill(
                level=self.herblore.level - other.herblore.level,
                experience=self.herblore.experience - other.herblore.experience,
                rank=min(self.herblore.rank, other.herblore.rank),
            ),
            agility=Skill(
                level=self.agility.level - other.agility.level,
                experience=self.agility.experience - other.agility.experience,
                rank=min(self.agility.rank, other.agility.rank),
            ),
            thieving=Skill(
                level=self.thieving.level - other.thieving.level,
                experience=self.thieving.experience - other.thieving.experience,
                rank=min(self.thieving.rank, other.thieving.rank),
            ),
            slayer=Skill(
                level=self.slayer.level - other.slayer.level,
                experience=self.slayer.experience - other.slayer.experience,
                rank=min(self.slayer.rank, other.slayer.rank),
            ),
            farming=Skill(
                level=self.farming.level - other.farming.level,
                experience=self.farming.experience - other.farming.experience,
                rank=min(self.farming.rank, other.farming.rank),
            ),
            runecrafting=Skill(
                level=self.runecrafting.level - other.runecrafting.level,
                experience=self.runecrafting.experience - other.runecrafting.experience,
                rank=min(self.runecrafting.rank, other.runecrafting.rank),
            ),
            hunter=Skill(
                level=self.hunter.level - other.hunter.level,
                experience=self.hunter.experience - other.hunter.experience,
                rank=min(self.hunter.rank, other.hunter.rank),
            ),
            construction=Skill(
                level=self.construction.level - other.construction.level,
                experience=self.construction.experience - other.construction.experience,
                rank=min(self.construction.rank, other.construction.rank),
            ),
        )


@dataclass
class Character:
    username: str
    combat_level: int = 3
    total_level: int = 32
    total_experience: int = 0
    total_rank: int = -1  # -1 means unranked
    skills: Skills = Skills()
    date: str = datetime.datetime.now().strftime(DATETIME_FORMAT)

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
