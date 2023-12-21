import requests
from core.dataclasses.character import Character, Skills, Skill


class CharacterStats:
    def __init__(self, username):
        self.username = username
        self.character = None

    @property
    def url(self):
        return (
            "https://secure.runescape.com/m=hiscore_oldschool/"
            f"index_lite.ws?player={self.username}"
        )

    @staticmethod
    def calculate_combat_level(
        attack: int,
        strength: int,
        defence: int,
        hitpoints: int,
        prayer: int,
        ranged: int,
        magic: int,
    ) -> int:
        """
        Calculate the combat level of a character based on their skills.

        Parameters
        ----------
        attack : int
            Attack level.
        strength : int
            Strength level.
        defence : int
            Defence level.
        hitpoints : int
            Hitpoints level.
        prayer : int
            Prayer level.
        ranged : int
            Ranged level.
        magic : int
            Magic level.

        Returns
        -------
        int
            The combat level.
        """
        base = 0.25 * (defence + hitpoints + (prayer // 2))
        melee = 0.325 * (attack + strength)
        ranged = 0.325 * (ranged * 1.5)
        magic = 0.325 * (magic * 1.5)

        return int(base + max(melee, ranged, magic))

    def parse(self, text: str) -> Character:
        """
        Parse the text from the hiscores page into a Character object.
        """
        info = {}
        skill_stats = text.split("\n")

        # First row is total level
        total_level_stats = skill_stats.pop(0).split(",")
        total_rank = int(total_level_stats[0])
        total_level = int(total_level_stats[1])
        total_experience = int(total_level_stats[2])

        skills = list(Skills.__annotations__)

        # Skills are in the same order as the Skills class
        # Other rows are minigames, boss kills, etc. that we don't care about
        skill_stats = skill_stats[: len(skills)]
        for skill_name, stats in zip(skills, skill_stats):
            rank, level, experience = stats.split(",")
            info[skill_name] = Skill(
                rank=int(rank), experience=int(experience), level=int(level)
            )
        skills = Skills(**info)
        combat_level = self.calculate_combat_level(
            attack=skills.attack.level,
            strength=skills.strength.level,
            defence=skills.defence.level,
            hitpoints=skills.hitpoints.level,
            prayer=skills.prayer.level,
            ranged=skills.ranged.level,
            magic=skills.magic.level,
        )
        return Character(
            username=self.username,
            skills=skills,
            total_level=total_level,
            total_experience=total_experience,
            total_rank=total_rank,
            combat_level=combat_level,
        )

    def get_character_stats(self) -> Character:
        response = requests.get(self.url)
        if response.status_code == 404:
            raise ValueError(f"User {self.username} does not exist.")
        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code} when scraping {self.url}")
        return self.parse(response.text)

    def collect(self) -> None:
        """
        Collect the character stats and store them in the character attribute.
        """
        self.character = self.get_character_stats()

    def display(self) -> None:
        """
        Display the character stats in a nice format.
        """
        print(self.character)
