from core.dataclasses.character import Skills, Skill
from core.scraper.runescape import RunescapeScraper


def test_calculate_combat_level():
    scraper = RunescapeScraper("Test")

    # Set skills to the stats of a level 47 combat
    combat_skills = {
        "attack": 40,
        "strength": 40,
        "defence": 36,
        "hitpoints": 38,
        "prayer": 26,
        "ranged": 26,
        "magic": 32,
    }

    # Convert the dict to a Skills object
    _skills = {}
    for skill_name, level in combat_skills.items():
        _skills[skill_name] = Skill(level=level)
    skills = Skills(**_skills)
    assert scraper.calculate_combat_level(skills) == 47
