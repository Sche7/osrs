from pydantic import BaseModel


class Skill(BaseModel):
    id: int
    name: str
    rank: int
    level: int
    xp: int


class Activity(BaseModel):
    id: int
    name: str
    rank: int
    score: int


class Player(BaseModel):
    name: str
    skills: list[Skill]
    activities: list[Activity]

    def display_skills(self) -> str:
        output = f"{self.name.title()}\n"
        combat_skill = self.skills[0]
        output += f"\tCombat level: {combat_skill.level:,d}\n"
        output += f"\tTotal rank: {combat_skill.rank:,d}\n"
        output += f"\tTotal experience: {combat_skill.xp:,d}\n"
        output += "\tSkills:\n"
        for s in self.skills[1:]:
            output += f"\t\t{s.name}: {s.level}\n"
        return output
