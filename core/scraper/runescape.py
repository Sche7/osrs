import requests
from bs4 import BeautifulSoup
from core.dataclasses.character import Character, Skills, Skill


class RunescapeScraper:
    def __init__(self, username):
        self.username = username

    @property
    def url(self):
        return (
            "https://secure.runescape.com/m=hiscore_oldschool/"
            f"index_lite.ws?player={self.username}"
        )

    def parse(self, text: str) -> Character:
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

        return Character(
            username=self.username,
            skills=Skills(**info),
            total_level=total_level,
            total_experience=total_experience,
            total_rank=total_rank,
        )

    def get_character_stats(self) -> Character:
        response = requests.get(self.url)
        if response.status_code == 404:
            raise ValueError(f"User {self.username} does not exist.")
        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code} when scraping {self.url}")
        return self.parse(response.text)
