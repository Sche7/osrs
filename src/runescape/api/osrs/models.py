from collections import namedtuple
from enum import Enum
from typing import Literal

Category = namedtuple("category", ["id", "name"])


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
    "u",
    "z",
]


class Categories(Enum):
    MISCELLANEOUS = Category(0, "Miscellaneous")
    AMMO = Category(1, "Ammo")
    ARROWS = Category(2, "Arrows")
    BOLTS = Category(3, "Bolts")
    CONSTRUCTION_MATERIALS = Category(4, "Construction materials")
    CONSTRUCTION_PRODUCTS = Category(5, "Construction products")
    COOKING_INGREDIENTS = Category(6, "Cooking ingredients")
    COSTUMES = Category(7, "Costumes")
    CRAFTING_MATERIALS = Category(8, "Crafting materials")
    FAMILIARS = Category(9, "Familiars")
    FARMING_PRODUCTS = Category(10, "Farming products")
    FLETCHING_MATERIALS = Category(11, "Fletching materials")
    FOOD_AND_DRINK = Category(12, "Food and Drink")
    HERBLORE_MATIERLAS = Category(13, "Herblore materials")
    HUNTING_EQUIPMENT = Category(14, "Hunting equipment")
    HUNTING_PRODUCTS = Category(15, "Hunting Products")
    JEWELLERY = Category(16, "Jewellery")
    MAGE_ARMOUR = Category(17, "Mage armour")
    MAGE_WEAPONS = Category(18, "Mage weapons")
    MELEE_ARMOUR_LOW_LEVEL = Category(19, "Melee armour - low level")
    MELEE_ARMOUR_MID_LEVEL = Category(20, "Melee armour - mid level")
    MELEE_ARMOUR_HIGH_LEVEL = Category(21, "Melee armour - high level")
    MELEE_WEAPONS_LOW_LEVEL = Category(22, "Melee weapons - low level")
    MELEE_WEAPONS_MID_LEVEL = Category(23, "Melee weapons - mid level")
    MELEE_WEAPONS_HIGH_LEVEL = Category(24, "Melee weapons - high level")
    MINING_AND_SMITHING = Category(25, "Mining and Smithing")
    POTIONS = Category(26, "Potions")
    PRAYER_ARMOUR = Category(27, "Prayer armour")
    PRAYER_MATERIALS = Category(28, "Prayer materials")
    RANGE_ARMOUR = Category(29, "Range armour")
    RANGE_WEAPONS = Category(30, "Range weapons")
    RUNECRAFTING = Category(31, "Runecrafting")
    RUNES_SPELLS_TELEPORTS = Category(32, "Runes, Spells and Teleports")
    SEEDS = Category(33, "Seeds")
    SUMMONING_SCROLLS = Category(34, "Summoning scrolls")
    TOOLS_AND_CONTAINERS = Category(35, "Tools and containers")
    WOODCUTTING_PRODUCT = Category(36, "Woodcutting product")
    POCKET_ITEMS = Category(37, "Pocket items")
    STONE_SPIRITS = Category(38, "Stone spirits")
    SALVAGE = Category(39, "Salvage")
    FIREMAKING_PRODUCTS = Category(40, "Firemaking products")
    ARCHAEOLOGY_MATERIALS = Category(41, "Archaeology materials")
    WOOD_SPIRITS = Category(42, "Wood spirits")
    NECROMANCY_ARMOUR = Category(43, "Necromancy armour")
