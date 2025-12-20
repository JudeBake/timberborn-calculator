from enum import Enum


class DifficultyLevel(Enum):
    EASY = 'easy'
    NORMAL = 'normal'
    HARD = 'hard'


class ConsumptionType(Enum):
    FOOD = 'food'
    WATER = 'water'


class CropName(Enum):
    BERRY_BUSH = 'Berry Bush'
    DANDELION_BUSH = 'Dandelion Bush'
    CARROT_CROP = 'Carrot Crop'
    SUNFLOWER_CROP = 'Sunflower Crop'
    POTATO_CROP = 'Potato Crop'
    WHEAT_CROP = 'Wheat Crop'
    CATTAIL_CROP = 'Cattail Crop'
    SPADDERDOCK_CROP = 'Spadderdock Crop'
    COFFEE_BUSH = 'Coffee Bush'
    KOHLRABI_CROP = 'Kohlrabi Crop'
    CASSAVA_CROP = 'Cassava Crop'
    SOYBEAN_CROP = 'Soybean Crop'
    CANOLA_CROP = 'Canola Crop'
    CORN_CROP = 'Corn Crop'
    EGGPLANT_CROP = 'Eggplant Crop'


class TreeName(Enum):
    BIRCH = 'Birch'
    PINE = 'Pine'
    MAPLE = 'Maple'
    CHESTNUT_TREE = 'Chestnut Tree'
    OAK = 'Oak'
    MANGROVE_TREE = 'Mangrove Tree'


class HarvestName(Enum):
    BERRIES = 'Berries'
    DANDELIONS = 'Dandelions'
    CARROTS = 'Carrots'
    SUNFLOWER_SEEDS = 'Sunflower Seeds'
    POTATOES = 'Potatoes'
    WHEAT = 'Wheat'
    CATTAIL_ROOTS = 'Cattail Roots'
    SPADDERDOCKS = 'Spadderdocks'
    COFFEE_BEANS = 'Coffee Beans'
    KOHLRABIES = 'Kohlrabies'
    CASSAVAS = 'Cassavas'
    SOYBEANS = 'Soybeans'
    CANOLA_SEEDS = 'Canola Seeds'
    CORN = 'Corn'
    EGGPLANTS = 'Eggplants'
    PINE_RESIN = 'Pine Resin'
    MAPLE_SYRUP = 'Maple Syrup'
    CHESTNUTS = 'Chestnuts'
    MANGROVE_FRUITS = 'Mangrove Fruits'


class WaterBuildingName(Enum):
    WATER_PUMP = 'Water Pump'
    LARGE_WATER_PUMP = 'Large Water Pump'
    BADWATER_PUMP = 'Badwater Pump'
    DEEP_WATER_PUMP = 'Deep Water Pump'
    DEEP_BADWATER_PUMP = 'Deep Badwater Pump'


class FoodProcessingBuildingName(Enum):
    GRILL = 'Grill'
    GRISTMILL = 'Gristmill'
    BAKERY = 'Bakery'
    COFFEE_BREWERY = 'Coffee Brewery'
    FERMENTER = 'Fermenter'
    FOOD_FACTORY = 'Food Factory'
    HYDROPONIC_GARDEN = 'Hydroponic Garden'
    OIL_PRESS = 'Oil Press'


class FoodRecipeName(Enum):
    GRILLED_POTATOES = 'Grilled Potatoes'
    GRILLED_CHESTNUTS = 'Grilled Chestnuts'
    GRILLED_SPADDERDOCKS = 'Grilled Spadderdocks'
    WHEAT_FLOUR = 'Wheat Flour'
    CATTAIL_FLOUR = 'Cattail Flour'


class GoodsBuildingName(Enum):
    LUMBER_MILL = 'Lumber Mill'
    INDUSTRIAL_LUMBER_MILL = 'Industrial Lumber Mill'
    GEAR_WORKSHOP = 'Gear Workshop'
    PAPER_MILL = 'Paper Mill'
    PRINTING_PRESS = 'Printing Press'
    WOOD_WORKSHOP = 'Wood Workshop'
    SMELTER = 'Smelter'
    MINE = 'Mine'
    EFFICIENT_MINE = 'Efficient Mine'
    RAFINERY = 'Rafinery'
    GREASE_FACTORY = 'Grease Factory'
    BOT_PART_FACTORY = 'Bot Part Factory'
    BOT_ASSEMBLER = 'Bot Assembler'
    EXPLOSIVES_FACTORY = 'Explosives Factory'
    CENTRIFUGE = 'Centrifuge'
    HERBALIST = 'Herbalist'


class DataKeys:
    FACTION_DATA = 'faction_data'
    NAME = 'name'
    DIFFICULTY = 'difficulty'
    MODIFIER = 'modifier'
    CONSUMPTION = 'consumption'
    FOOD = 'food'
    WATER = 'water'
    PRODUCTION = 'production'
    BEEHIVE = 'beehive'
    CROPS = 'crops'
    GROWTH_TIME = 'growth_time'
    HARVEST = 'harvest'
    TIME = 'time'
    YIELD = 'yield'
    TREES = 'trees'
    LOG_OUTPUT = 'log_output'
    RECIPES = 'recipes'
    PROD_TIME = 'production_time'
    INPUTS = 'inputs'
    QUANTITY = 'quantity'
    OUT_QUANTITY = 'output_quantity'
    FOOD_PROCESSING = 'food_processing'
    WORKERS = 'workers'
    GOODS = 'goods'
