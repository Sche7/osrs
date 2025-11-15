from collections import namedtuple
from enum import Enum
from typing import Literal

Alpha = Literal[
    "#",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "x",
    "y",
    "z",
]


CategoryGroup = namedtuple("CategoryGroup", ["id", "name"])


class Category(Enum):
    MISCELLANEOUS = CategoryGroup(0, "Miscellaneous")
    AMMO = CategoryGroup(1, "Ammo")
    ARROWS = CategoryGroup(2, "Arrows")
    BOLTS = CategoryGroup(3, "Bolts")
    CONSTRUCTION_MATERIALS = CategoryGroup(4, "Construction materials")
    CONSTRUCTION_PRODUCTS = CategoryGroup(5, "Construction products")
    COOKING_INGREDIENTS = CategoryGroup(6, "Cooking ingredients")
    COSTUMES = CategoryGroup(7, "Costumes")
    CRAFTING_MATERIALS = CategoryGroup(8, "Crafting materials")
    FAMILIARS = CategoryGroup(9, "Familiars")
    FARMING_PRODUCTS = CategoryGroup(10, "Farming products")
    FLETCHING_MATERIALS = CategoryGroup(11, "Fletching materials")
    FOOD_AND_DRINK = CategoryGroup(12, "Food and Drink")
    HERBLORE_MATERIALS = CategoryGroup(13, "Herblore materials")
    HUNTING_EQUIPMENT = CategoryGroup(14, "Hunting equipment")
    HUNTING_PRODUCTS = CategoryGroup(15, "Hunting Products")
    JEWELLERY = CategoryGroup(16, "Jewellery")
    MAGE_ARMOUR = CategoryGroup(17, "Mage armour")
    MAGE_WEAPONS = CategoryGroup(18, "Mage weapons")
    MELEE_ARMOUR_LOW_LEVEL = CategoryGroup(19, "Melee armour - low level")
    MELEE_ARMOUR_MID_LEVEL = CategoryGroup(20, "Melee armour - mid level")
    MELEE_ARMOUR_HIGH_LEVEL = CategoryGroup(21, "Melee armour - high level")
    MELEE_WEAPONS_LOW_LEVEL = CategoryGroup(22, "Melee weapons - low level")
    MELEE_WEAPONS_MID_LEVEL = CategoryGroup(23, "Melee weapons - mid level")
    MELEE_WEAPONS_HIGH_LEVEL = CategoryGroup(24, "Melee weapons - high level")
    MINING_AND_SMITHING = CategoryGroup(25, "Mining and Smithing")
    POTIONS = CategoryGroup(26, "Potions")
    PRAYER_ARMOUR = CategoryGroup(27, "Prayer armour")
    PRAYER_MATERIALS = CategoryGroup(28, "Prayer materials")
    RANGE_ARMOUR = CategoryGroup(29, "Range armour")
    RANGE_WEAPONS = CategoryGroup(30, "Range weapons")
    RUNECRAFTING = CategoryGroup(31, "Runecrafting")
    RUNES_SPELLS_TELEPORTS = CategoryGroup(32, "Runes, Spells and Teleports")
    SEEDS = CategoryGroup(33, "Seeds")
    SUMMONING_SCROLLS = CategoryGroup(34, "Summoning scrolls")
    TOOLS_AND_CONTAINERS = CategoryGroup(35, "Tools and containers")
    WOODCUTTING_PRODUCT = CategoryGroup(36, "Woodcutting product")
    POCKET_ITEMS = CategoryGroup(37, "Pocket items")
    STONE_SPIRITS = CategoryGroup(38, "Stone spirits")
    SALVAGE = CategoryGroup(39, "Salvage")
    FIREMAKING_PRODUCTS = CategoryGroup(40, "Firemaking products")
    ARCHAEOLOGY_MATERIALS = CategoryGroup(41, "Archaeology materials")
    WOOD_SPIRITS = CategoryGroup(42, "Wood spirits")
    NECROMANCY_ARMOUR = CategoryGroup(43, "Necromancy armour")
