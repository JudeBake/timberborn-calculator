import math

from ..data.emunerators import ConsumptionType, CropName, DifficultyLevel
from ..data.emunerators import FoodProcessingBuildingName, FoodRecipeName
from ..data.emunerators import HarvestName, TreeName, WaterBuildingName
from ..data.factionData import FactionData


class Folktail:
    """
    Folktail faction calculator class.

    This class encapsulates Folktail-specific faction data and provides
    methods to calculate resource requirements for a Folktail population.
    """

    def __init__(self) -> None:
        """
        Initialize the Folktail calculator with faction data.
        """
        self.factionData = FactionData('./data/folktails.yml')

    def getDailyFoodConsumption(self, population: int,
                                difficulty: DifficultyLevel) -> float:
        """
        Calculate the daily food consumption for a given population at a
        given difficulty level.

        :param population: The population size.
        :type population: int
        :param difficulty: The difficulty level.
        :type difficulty: DifficultyLevel

        :return: Daily food consumption.
        :rtype: float

        :raises ValueError: If population is negative.
        """
        if population < 0:
            raise ValueError("Population cannot be negative.")

        baseConsumption = self.factionData.getConsumption(
            ConsumptionType.FOOD)
        difficultyModifier = self.factionData.getDifficultyModifier(difficulty)
        return population * baseConsumption * difficultyModifier

    def getDailyWaterConsumption(self, population: int,
                                 difficulty: DifficultyLevel) -> float:
        """
        Calculate the daily water consumption for a given population at a
        given difficulty level.

        :param population: The population size.
        :type population: int
        :param difficulty: The difficulty level.
        :type difficulty: DifficultyLevel

        :return: Daily water consumption.
        :rtype: float

        :raises ValueError: If population is negative.
        """
        if population < 0:
            raise ValueError("Population cannot be negative.")

        baseConsumption = self.factionData.getConsumption(
            ConsumptionType.WATER)
        difficultyModifier = self.factionData.getDifficultyModifier(difficulty)
        return population * baseConsumption * difficultyModifier

    def getFoodPerType(self, population: int, foodTypeCount: int,
                       difficulty: DifficultyLevel) -> int:
        """
        Calculate the amount of food needed per food type to support a
        given population, assuming equal distribution across the specified
        number of food types.

        :param population: The population size.
        :type population: int
        :param foodTypeCount: Number of different food types to distribute
                              consumption across.
        :type foodTypeCount: int
        :param difficulty: The difficulty level.
        :type difficulty: DifficultyLevel

        :return: Daily food amount needed per food type.
        :rtype: int

        :raises ValueError: If population is negative or foodTypeCount is
                            not positive.
        """
        if population < 0:
            raise ValueError("Population cannot be negative.")
        if foodTypeCount <= 0:
            raise ValueError("Food type count must be positive.")

        totalFoodConsumption = self.getDailyFoodConsumption(population,
                                                            difficulty)
        return math.ceil(totalFoodConsumption / foodTypeCount)

    def getBerryTilesNeeded(self, berryAmount: float) -> int:
        """
        Calculate the number of berry tiles needed to produce a given
        amount of berries per day.

        :param berryAmount: Daily amount of berries needed.
        :type berryAmount: float

        :return: Number of berry tiles needed.
        :rtype: int

        :raises ValueError: If berry amount is negative.
        """
        if berryAmount < 0:
            raise ValueError("Berry amount cannot be negative.")

        harvestTime = self.factionData.getCropHarvestTime(CropName.BERRY_BUSH)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.BERRY_BUSH)
        productionPerTile = harvestYield / harvestTime

        return math.ceil(berryAmount / productionPerTile)

    def getCarrotTilesNeeded(self, carrotAmount: float,
                             useBeehive: bool) -> int:
        """
        Calculate the number of carrot tiles needed to produce a given
        amount of carrots per day.

        :param carrotAmount: Daily amount of carrots needed.
        :type carrotAmount: float
        :param useBeehive: Whether to apply beehive production modifier.
        :type useBeehive: bool

        :return: Number of carrot tiles needed.
        :rtype: int

        :raises ValueError: If carrot amount is negative.
        """
        if carrotAmount < 0:
            raise ValueError("Carrot amount cannot be negative.")

        harvestTime = self.factionData.getCropHarvestTime(CropName.CARROT_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.CARROT_CROP)
        productionPerTile = harvestYield / harvestTime

        if useBeehive:
            beehiveModifier = self.factionData.getBeehiveModifier()
            productionPerTile *= beehiveModifier

        return math.ceil(carrotAmount / productionPerTile)

    def getSunflowerTilesNeeded(self, sunflowerSeedAmount: float,
                                useBeehive: bool) -> int:
        """
        Calculate the number of sunflower tiles needed to produce a given
        amount of sunflower seeds per day.

        :param sunflowerSeedAmount: Daily amount of sunflower seeds needed.
        :type sunflowerSeedAmount: float
        :param useBeehive: Whether to apply beehive production modifier.
        :type useBeehive: bool

        :return: Number of sunflower tiles needed.
        :rtype: int

        :raises ValueError: If sunflower seed amount is negative.
        """
        if sunflowerSeedAmount < 0:
            raise ValueError("Sunflower seed amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.SUNFLOWER_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.SUNFLOWER_CROP)
        productionPerTile = harvestYield / harvestTime

        if useBeehive:
            beehiveModifier = self.factionData.getBeehiveModifier()
            productionPerTile *= beehiveModifier

        return math.ceil(sunflowerSeedAmount / productionPerTile)

    def getPotatoTilesNeeded(self, potatoAmount: float,
                             useBeehive: bool) -> int:
        """
        Calculate the number of potato tiles needed to produce a given
        amount of potatoes per day.

        :param potatoAmount: Daily amount of potatoes needed.
        :type potatoAmount: float
        :param useBeehive: Whether to apply beehive production modifier.
        :type useBeehive: bool

        :return: Number of potato tiles needed.
        :rtype: int

        :raises ValueError: If potato amount is negative.
        """
        if potatoAmount < 0:
            raise ValueError("Potato amount cannot be negative.")

        harvestTime = self.factionData.getCropHarvestTime(CropName.POTATO_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.POTATO_CROP)
        productionPerTile = harvestYield / harvestTime

        if useBeehive:
            beehiveModifier = self.factionData.getBeehiveModifier()
            productionPerTile *= beehiveModifier

        return math.ceil(potatoAmount / productionPerTile)

    def getWheatTilesNeeded(self, wheatAmount: float,
                            useBeehive: bool) -> int:
        """
        Calculate the number of wheat tiles needed to produce a given
        amount of wheat per day.

        :param wheatAmount: Daily amount of wheat needed.
        :type wheatAmount: float
        :param useBeehive: Whether to apply beehive production modifier.
        :type useBeehive: bool

        :return: Number of wheat tiles needed.
        :rtype: int

        :raises ValueError: If wheat amount is negative.
        """
        if wheatAmount < 0:
            raise ValueError("Wheat amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.WHEAT_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.WHEAT_CROP)
        productionPerTile = harvestYield / harvestTime

        if useBeehive:
            beehiveModifier = self.factionData.getBeehiveModifier()
            productionPerTile *= beehiveModifier

        return math.ceil(wheatAmount / productionPerTile)

    def getCattailTilesNeeded(self, cattailRootAmount: float,
                              useBeehive: bool) -> int:
        """
        Calculate the number of cattail tiles needed to produce a given
        amount of cattail roots per day.

        :param cattailRootAmount: Daily amount of cattail roots needed.
        :type cattailRootAmount: float
        :param useBeehive: Whether to apply beehive production modifier.
        :type useBeehive: bool

        :return: Number of cattail tiles needed.
        :rtype: int

        :raises ValueError: If cattail root amount is negative.
        """
        if cattailRootAmount < 0:
            raise ValueError("Cattail root amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.CATTAIL_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.CATTAIL_CROP)
        productionPerTile = harvestYield / harvestTime

        if useBeehive:
            beehiveModifier = self.factionData.getBeehiveModifier()
            productionPerTile *= beehiveModifier

        return math.ceil(cattailRootAmount / productionPerTile)

    def getSpadderdockTilesNeeded(self, spadderdockAmount: float,
                                  useBeehive: bool) -> int:
        """
        Calculate the number of spadderdock tiles needed to produce a given
        amount of spadderdocks per day.

        :param spadderdockAmount: Daily amount of spadderdocks needed.
        :type spadderdockAmount: float
        :param useBeehive: Whether to apply beehive production modifier.
        :type useBeehive: bool

        :return: Number of spadderdock tiles needed.
        :rtype: int

        :raises ValueError: If spadderdock amount is negative.
        """
        if spadderdockAmount < 0:
            raise ValueError("Spadderdock amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.SPADDERDOCK_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.SPADDERDOCK_CROP)
        productionPerTile = harvestYield / harvestTime

        if useBeehive:
            beehiveModifier = self.factionData.getBeehiveModifier()
            productionPerTile *= beehiveModifier

        return math.ceil(spadderdockAmount / productionPerTile)

    def getLogPerType(self, totalLogAmount: float, treeTypeCount: int) -> int:
        """
        Calculate the amount of logs needed per tree type.

        :param totalLogAmount: Total amount of logs needed.
        :type totalLogAmount: float
        :param treeTypeCount: Number of tree types.
        :type treeTypeCount: int

        :return: Amount of logs per tree type.
        :rtype: int

        :raises ValueError: If total log amount is negative or tree type count
                            is not positive.
        """
        if totalLogAmount < 0:
            raise ValueError("Total log amount cannot be negative.")
        if treeTypeCount <= 0:
            raise ValueError("Tree type count must be positive.")

        return math.ceil(totalLogAmount / treeTypeCount)

    def getBirchLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of birch tree tiles needed to produce a given
        amount of logs per day.

        :param logAmount: Daily amount of logs needed.
        :type logAmount: float

        :return: Number of birch tree tiles needed.
        :rtype: int

        :raises ValueError: If log amount is negative.
        """
        if logAmount < 0:
            raise ValueError("Log amount cannot be negative.")

        growthTime = self.factionData.getTreeGrowthTime(TreeName.BIRCH)
        logOutput = self.factionData.getTreeLogOutput(TreeName.BIRCH)
        productionPerTile = logOutput / growthTime

        return math.ceil(logAmount / productionPerTile)

    def getPineLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of pine tree tiles needed to produce a given
        amount of logs per day.

        :param logAmount: Daily amount of logs needed.
        :type logAmount: float

        :return: Number of pine tree tiles needed.
        :rtype: int

        :raises ValueError: If log amount is negative.
        """
        if logAmount < 0:
            raise ValueError("Log amount cannot be negative.")

        growthTime = self.factionData.getTreeGrowthTime(TreeName.PINE)
        logOutput = self.factionData.getTreeLogOutput(TreeName.PINE)
        productionPerTile = logOutput / growthTime

        return math.ceil(logAmount / productionPerTile)

    def getPineResinTilesNeeded(self, pineResinAmount: float) -> int:
        """
        Calculate the number of pine tree tiles needed to produce a given
        amount of pine resin per day.

        :param pineResinAmount: Daily amount of pine resin needed.
        :type pineResinAmount: float

        :return: Number of pine tree tiles needed.
        :rtype: int

        :raises ValueError: If pine resin amount is negative.
        """
        if pineResinAmount < 0:
            raise ValueError("Pine resin amount cannot be negative.")

        harvestTime = self.factionData.getTreeHarvestTime(TreeName.PINE)
        harvestYield = self.factionData.getTreeHarvestYield(TreeName.PINE)
        productionPerTile = harvestYield / harvestTime

        return math.ceil(pineResinAmount / productionPerTile)

    def getMapleLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of maple tree tiles needed to produce a given
        amount of logs per day.

        :param logAmount: Daily amount of logs needed.
        :type logAmount: float

        :return: Number of maple tree tiles needed.
        :rtype: int

        :raises ValueError: If log amount is negative.
        """
        if logAmount < 0:
            raise ValueError("Log amount cannot be negative.")

        growthTime = self.factionData.getTreeGrowthTime(TreeName.MAPLE)
        logOutput = self.factionData.getTreeLogOutput(TreeName.MAPLE)
        productionPerTile = logOutput / growthTime

        return math.ceil(logAmount / productionPerTile)

    def getMapleSyrupTilesNeeded(self, mapleSyrupAmount: float) -> int:
        """
        Calculate the number of maple tree tiles needed to produce a given
        amount of maple syrup per day.

        :param mapleSyrupAmount: Daily amount of maple syrup needed.
        :type mapleSyrupAmount: float

        :return: Number of maple tree tiles needed.
        :rtype: int

        :raises ValueError: If maple syrup amount is negative.
        """
        if mapleSyrupAmount < 0:
            raise ValueError("Maple syrup amount cannot be negative.")

        harvestTime = self.factionData.getTreeHarvestTime(TreeName.MAPLE)
        harvestYield = self.factionData.getTreeHarvestYield(TreeName.MAPLE)
        productionPerTile = harvestYield / harvestTime

        return math.ceil(mapleSyrupAmount / productionPerTile)

    def getChestnutLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of chestnut tree tiles needed to produce a given
        amount of logs per day.

        :param logAmount: Daily amount of logs needed.
        :type logAmount: float

        :return: Number of chestnut tree tiles needed.
        :rtype: int

        :raises ValueError: If log amount is negative.
        """
        if logAmount < 0:
            raise ValueError("Log amount cannot be negative.")

        growthTime = self.factionData.getTreeGrowthTime(
            TreeName.CHESTNUT_TREE)
        logOutput = self.factionData.getTreeLogOutput(TreeName.CHESTNUT_TREE)
        productionPerTile = logOutput / growthTime

        return math.ceil(logAmount / productionPerTile)

    def getChestnutTilesNeeded(self, chestnutAmount: float) -> int:
        """
        Calculate the number of chestnut tree tiles needed to produce a given
        amount of chestnuts per day.

        :param chestnutAmount: Daily amount of chestnuts needed.
        :type chestnutAmount: float

        :return: Number of chestnut tree tiles needed.
        :rtype: int

        :raises ValueError: If chestnut amount is negative.
        """
        if chestnutAmount < 0:
            raise ValueError("Chestnut amount cannot be negative.")

        harvestTime = self.factionData \
            .getTreeHarvestTime(TreeName.CHESTNUT_TREE)
        harvestYield = self.factionData \
            .getTreeHarvestYield(TreeName.CHESTNUT_TREE)
        productionPerTile = harvestYield / harvestTime

        return math.ceil(chestnutAmount / productionPerTile)

    def getOakLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of oak tree tiles needed to produce a given
        amount of logs per day.

        :param logAmount: Daily amount of logs needed.
        :type logAmount: float

        :return: Number of oak tree tiles needed.
        :rtype: int

        :raises ValueError: If log amount is negative.
        """
        if logAmount < 0:
            raise ValueError("Log amount cannot be negative.")

        growthTime = self.factionData.getTreeGrowthTime(TreeName.OAK)
        logOutput = self.factionData.getTreeLogOutput(TreeName.OAK)
        productionPerTile = logOutput / growthTime

        return math.ceil(logAmount / productionPerTile)

    def getWaterPumpsNeeded(self, waterAmount: float) -> int:
        """
        Calculate the number of water pumps needed to produce a given
        amount of water per day.

        :param waterAmount: Daily amount of water needed.
        :type waterAmount: float

        :return: Number of water pumps needed.
        :rtype: int

        :raises ValueError: If water amount is negative.
        """
        if waterAmount < 0:
            raise ValueError("Water amount cannot be negative.")

        productionTime = self.factionData \
            .getWaterProductionTime(WaterBuildingName.WATER_PUMP)
        outputQuantity = self.factionData \
            .getWaterOutputQuantity(WaterBuildingName.WATER_PUMP)
        # Production time is in hours, calculate daily production
        productionPerPump = (outputQuantity / productionTime) * 24

        return math.ceil(waterAmount / productionPerPump)

    def getLargeWaterPumpsNeeded(self, waterAmount: float,
                                 workersCount: int) -> int:
        """
        Calculate the number of large water pumps needed to produce a given
        amount of water per day with a specified number of workers per pump.

        :param waterAmount: Daily amount of water needed.
        :type waterAmount: float
        :param workersCount: Number of workers assigned per pump.
        :type workersCount: int

        :return: Number of large water pumps needed.
        :rtype: int

        :raises ValueError: If water amount is negative, workers count is
                            negative, or workers count exceeds maximum.
        """
        if waterAmount < 0:
            raise ValueError("Water amount cannot be negative.")
        if workersCount < 0:
            raise ValueError("Workers count cannot be negative.")

        maxWorkers = self.factionData \
            .getWaterWorkers(WaterBuildingName.LARGE_WATER_PUMP)
        if workersCount > maxWorkers:
            raise ValueError(f"Workers count cannot exceed {maxWorkers}.")

        productionTime = self.factionData \
            .getWaterProductionTime(WaterBuildingName.LARGE_WATER_PUMP)
        outputQuantity = self.factionData \
            .getWaterOutputQuantity(WaterBuildingName.LARGE_WATER_PUMP)

        # Reduce output based on workers assigned
        effectiveOutput = outputQuantity * (workersCount / maxWorkers)
        # Production time is in hours, calculate daily production
        productionPerPump = (effectiveOutput / productionTime) * 24

        return math.ceil(waterAmount / productionPerPump)

    def getBadwaterPumpsNeeded(self, waterAmount: float) -> int:
        """
        Calculate the number of badwater pumps needed to produce a given
        amount of water per day.

        :param waterAmount: Daily amount of water needed.
        :type waterAmount: float

        :return: Number of badwater pumps needed.
        :rtype: int

        :raises ValueError: If water amount is negative.
        """
        if waterAmount < 0:
            raise ValueError("Water amount cannot be negative.")

        productionTime = self.factionData \
            .getWaterProductionTime(WaterBuildingName.BADWATER_PUMP)
        outputQuantity = self.factionData \
            .getWaterOutputQuantity(WaterBuildingName.BADWATER_PUMP)
        # Production time is in hours, calculate daily production
        productionPerPump = (outputQuantity / productionTime) * 24

        return math.ceil(waterAmount / productionPerPump)

    def getGrillsNeededForPotatoes(self, grilledPotatoAmount: float) -> int:
        """
        Calculate the number of grills needed to produce a given amount of
        grilled potatoes per day.

        :param grilledPotatoAmount: Daily amount of grilled potatoes needed.
        :type grilledPotatoAmount: float

        :return: Number of grills needed.
        :rtype: int

        :raises ValueError: If grilled potato amount is negative.
        """
        if grilledPotatoAmount < 0:
            raise ValueError("Grilled potato amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_POTATOES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGrill = (outputQuantity / productionTime) * 24

        return math.ceil(grilledPotatoAmount / productionPerGrill)

    def getPotatoesNeededForGrills(self, grillsCount: int) -> int:
        """
        Calculate the number of potatoes needed per day to keep a given
        number of grills running producing grilled potatoes.

        :param grillsCount: Number of grills.
        :type grillsCount: int

        :return: Daily amount of potatoes needed.
        :rtype: int

        :raises ValueError: If grills count is negative.
        """
        if grillsCount < 0:
            raise ValueError("Grills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_POTATOES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        potatoInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_POTATOES,
            HarvestName.POTATOES.value)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        potatoesPerGrillPerDay = potatoInput * cyclesPerDay

        return math.ceil(grillsCount * potatoesPerGrillPerDay)

    def getLogsNeededForGrillsWithPotatoes(self, grillsCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number
        of grills running producing grilled potatoes.

        :param grillsCount: Number of grills.
        :type grillsCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If grills count is negative.
        """
        if grillsCount < 0:
            raise ValueError("Grills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_POTATOES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        logInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_POTATOES,
            "Logs")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerGrillPerDay = logInput * cyclesPerDay

        return grillsCount * logsPerGrillPerDay

    def getGrillsNeededForChestnuts(self, grilledChestnutAmount: float) -> int:
        """
        Calculate the number of grills needed to produce a given amount of
        grilled chestnuts per day.

        :param grilledChestnutAmount: Daily amount of grilled chestnuts needed.
        :type grilledChestnutAmount: float

        :return: Number of grills needed.
        :rtype: int

        :raises ValueError: If grilled chestnut amount is negative.
        """
        if grilledChestnutAmount < 0:
            raise ValueError("Grilled chestnut amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_CHESTNUTS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGrill = (outputQuantity / productionTime) * 24

        return math.ceil(grilledChestnutAmount / productionPerGrill)

    def getChestnutsNeededForGrills(self, grillsCount: int) -> int:
        """
        Calculate the number of chestnuts needed per day to keep a given
        number of grills running producing grilled chestnuts.

        :param grillsCount: Number of grills.
        :type grillsCount: int

        :return: Daily amount of chestnuts needed.
        :rtype: int

        :raises ValueError: If grills count is negative.
        """
        if grillsCount < 0:
            raise ValueError("Grills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_CHESTNUTS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        chestnutInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_CHESTNUTS,
            HarvestName.CHESTNUTS.value)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        chestnutsPerGrillPerDay = chestnutInput * cyclesPerDay

        return math.ceil(grillsCount * chestnutsPerGrillPerDay)

    def getLogsNeededForGrillsWithChestnuts(self, grillsCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number
        of grills running producing grilled chestnuts.

        :param grillsCount: Number of grills.
        :type grillsCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If grills count is negative.
        """
        if grillsCount < 0:
            raise ValueError("Grills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_CHESTNUTS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        logInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_CHESTNUTS,
            "Logs")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerGrillPerDay = logInput * cyclesPerDay

        return grillsCount * logsPerGrillPerDay

    def getGrillsNeededForSpadderdocks(self,
                                       grilledSpadderdockAmount: float) -> int:
        """
        Calculate the number of grills needed to produce a given amount of
        grilled spadderdocks per day.

        :param grilledSpadderdockAmount: Daily amount of grilled spadderdocks
            needed.
        :type grilledSpadderdockAmount: float

        :return: Number of grills needed.
        :rtype: int

        :raises ValueError: If grilled spadderdock amount is negative.
        """
        if grilledSpadderdockAmount < 0:
            raise ValueError("Grilled spadderdock amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL,
            FoodRecipeName.GRILLED_SPADDERDOCKS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGrill = (outputQuantity / productionTime) * 24

        return math.ceil(grilledSpadderdockAmount / productionPerGrill)

    def getSpadderdocksNeededForGrills(self, grillsCount: int) -> int:
        """
        Calculate the number of spadderdocks needed per day to keep a given
        number of grills running producing grilled spadderdocks.

        :param grillsCount: Number of grills.
        :type grillsCount: int

        :return: Daily amount of spadderdocks needed.
        :rtype: int

        :raises ValueError: If grills count is negative.
        """
        if grillsCount < 0:
            raise ValueError("Grills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL,
            FoodRecipeName.GRILLED_SPADDERDOCKS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        spadderdockInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRILL,
            FoodRecipeName.GRILLED_SPADDERDOCKS,
            HarvestName.SPADDERDOCKS.value)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        spadderdocksPerGrillPerDay = spadderdockInput * cyclesPerDay

        return math.ceil(grillsCount * spadderdocksPerGrillPerDay)

    def getLogsNeededForGrillsWithSpadderdocks(self,
                                               grillsCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number
        of grills running producing grilled spadderdocks.

        :param grillsCount: Number of grills.
        :type grillsCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If grills count is negative.
        """
        if grillsCount < 0:
            raise ValueError("Grills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRILL,
            FoodRecipeName.GRILLED_SPADDERDOCKS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRILL, recipeIndex)
        logInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRILL,
            FoodRecipeName.GRILLED_SPADDERDOCKS,
            "Logs")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerGrillPerDay = logInput * cyclesPerDay

        return grillsCount * logsPerGrillPerDay

    def getGristmillsNeededForWheatFlour(self, wheatFlourAmount: float) -> int:
        """
        Calculate the number of gristmills needed to produce a given amount of
        wheat flour per day.

        :param wheatFlourAmount: Daily amount of wheat flour needed.
        :type wheatFlourAmount: float

        :return: Number of gristmills needed.
        :rtype: int

        :raises ValueError: If wheat flour amount is negative.
        """
        if wheatFlourAmount < 0:
            raise ValueError("Wheat flour amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRISTMILL,
            FoodRecipeName.WHEAT_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRISTMILL, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.GRISTMILL, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGristmill = (outputQuantity / productionTime) * 24

        return math.ceil(wheatFlourAmount / productionPerGristmill)

    def getWheatNeededForGristmills(self, gristmillsCount: int) -> int:
        """
        Calculate the number of wheat needed per day to keep a given number of
        gristmills running producing wheat flour.

        :param gristmillsCount: Number of gristmills.
        :type gristmillsCount: int

        :return: Daily amount of wheat needed.
        :rtype: int

        :raises ValueError: If gristmills count is negative.
        """
        if gristmillsCount < 0:
            raise ValueError("Gristmills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRISTMILL,
            FoodRecipeName.WHEAT_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRISTMILL, recipeIndex)
        wheatInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRISTMILL,
            FoodRecipeName.WHEAT_FLOUR,
            HarvestName.WHEAT.value)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        wheatPerGristmillPerDay = wheatInput * cyclesPerDay

        return math.ceil(gristmillsCount * wheatPerGristmillPerDay)

    def getGristmillsNeededForCattailFlour(self,
                                           cattailFlourAmount: float) -> int:
        """
        Calculate the number of gristmills needed to produce a given amount of
        cattail flour per day.

        :param cattailFlourAmount: Daily amount of cattail flour needed.
        :type cattailFlourAmount: float

        :return: Number of gristmills needed.
        :rtype: int

        :raises ValueError: If cattail flour amount is negative.
        """
        if cattailFlourAmount < 0:
            raise ValueError("Cattail flour amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRISTMILL,
            FoodRecipeName.CATTAIL_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRISTMILL, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.GRISTMILL, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGristmill = (outputQuantity / productionTime) * 24

        return math.ceil(cattailFlourAmount / productionPerGristmill)

    def getCattailRootsNeededForGristmills(self, gristmillsCount: int) -> int:
        """
        Calculate the number of cattail roots needed per day to keep a given
        number of gristmills running producing cattail flour.

        :param gristmillsCount: Number of gristmills.
        :type gristmillsCount: int

        :return: Daily amount of cattail roots needed.
        :rtype: int

        :raises ValueError: If gristmills count is negative.
        """
        if gristmillsCount < 0:
            raise ValueError("Gristmills count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.GRISTMILL,
            FoodRecipeName.CATTAIL_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.GRISTMILL, recipeIndex)
        cattailRootsInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRISTMILL,
            FoodRecipeName.CATTAIL_FLOUR,
            HarvestName.CATTAIL_ROOTS.value)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        cattailRootsPerGristmillPerDay = cattailRootsInput * cyclesPerDay

        return math.ceil(gristmillsCount * cattailRootsPerGristmillPerDay)

    def getBakeriesNeededForBreads(self, breadsAmount: float) -> int:
        """
        Calculate the number of bakeries needed to produce a given amount of
        breads per day.

        :param breadsAmount: Daily amount of breads needed.
        :type breadsAmount: float

        :return: Number of bakeries needed.
        :rtype: int

        :raises ValueError: If breads amount is negative.
        """
        if breadsAmount < 0:
            raise ValueError("Breads amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.BREADS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBakery = (outputQuantity / productionTime) * 24

        return math.ceil(breadsAmount / productionPerBakery)

    def getWheatFlourNeededForBakeriesWithBreads(self,
                                                 bakeriesCount: int) -> int:
        """
        Calculate the number of wheat flour needed per day to keep a given
        number of bakeries running producing breads.

        :param bakeriesCount: Number of bakeries.
        :type bakeriesCount: int

        :return: Daily amount of wheat flour needed.
        :rtype: int

        :raises ValueError: If bakeries count is negative.
        """
        if bakeriesCount < 0:
            raise ValueError("Bakeries count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.BREADS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        wheatFlourInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.BREADS,
            "Wheat Flour")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        wheatFlourPerBakeryPerDay = wheatFlourInput * cyclesPerDay

        return math.ceil(bakeriesCount * wheatFlourPerBakeryPerDay)

    def getLogsNeededForBakeriesWithBreads(self, bakeriesCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number
        of bakeries running producing breads.

        :param bakeriesCount: Number of bakeries.
        :type bakeriesCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If bakeries count is negative.
        """
        if bakeriesCount < 0:
            raise ValueError("Bakeries count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.BREADS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        logInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.BREADS,
            "Logs")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerBakeryPerDay = logInput * cyclesPerDay

        return bakeriesCount * logsPerBakeryPerDay

    def getBakeriesNeededForCattailCrackers(self,
                                            cattailCrackersAmount: float
                                            ) -> int:
        """
        Calculate the number of bakeries needed to produce a given amount of
        cattail crackers per day.

        :param cattailCrackersAmount: Daily amount of cattail crackers needed.
        :type cattailCrackersAmount: float

        :return: Number of bakeries needed.
        :rtype: int

        :raises ValueError: If cattail crackers amount is negative.
        """
        if cattailCrackersAmount < 0:
            raise ValueError("Cattail crackers amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.CATTAIL_CRACKERS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBakery = (outputQuantity / productionTime) * 24

        return math.ceil(cattailCrackersAmount / productionPerBakery)

    def getCattailFlourNeededForBakeriesWithCattailCrackers(self,
                                                            bakeriesCount: int
                                                            ) -> int:
        """
        Calculate the number of cattail flour needed per day to keep a given
        number of bakeries running producing cattail crackers.

        :param bakeriesCount: Number of bakeries.
        :type bakeriesCount: int

        :return: Daily amount of cattail flour needed.
        :rtype: int

        :raises ValueError: If bakeries count is negative.
        """
        if bakeriesCount < 0:
            raise ValueError("Bakeries count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.CATTAIL_CRACKERS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        cattailFlourInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.CATTAIL_CRACKERS,
            "Cattail Flour")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        cattailFlourPerBakeryPerDay = cattailFlourInput * cyclesPerDay

        return math.ceil(bakeriesCount * cattailFlourPerBakeryPerDay)

    def getLogsNeededForBakeriesWithCattailCrackers(self,
                                                    bakeriesCount: int
                                                    ) -> float:
        """
        Calculate the number of logs needed per day to keep a given number
        of bakeries running producing cattail crackers.

        :param bakeriesCount: Number of bakeries.
        :type bakeriesCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If bakeries count is negative.
        """
        if bakeriesCount < 0:
            raise ValueError("Bakeries count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.CATTAIL_CRACKERS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        logInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.CATTAIL_CRACKERS,
            "Logs")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerBakeryPerDay = logInput * cyclesPerDay

        return bakeriesCount * logsPerBakeryPerDay

    def getBakeriesNeededForMaplePastries(self,
                                          maplePastriesAmount: float) -> int:
        """
        Calculate the number of bakeries needed to produce a given amount of
        maple pastries per day.

        :param maplePastriesAmount: Daily amount of maple pastries needed.
        :type maplePastriesAmount: float

        :return: Number of bakeries needed.
        :rtype: int

        :raises ValueError: If maple pastries amount is negative.
        """
        if maplePastriesAmount < 0:
            raise ValueError("Maple pastries amount cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBakery = (outputQuantity / productionTime) * 24

        return math.ceil(maplePastriesAmount / productionPerBakery)

    def getWheatFlourNeededForBakeriesWithMaplePastries(self,
                                                        bakeriesCount: int
                                                        ) -> int:
        """
        Calculate the number of wheat flour needed per day to keep a given
        number of bakeries running producing maple pastries.

        :param bakeriesCount: Number of bakeries.
        :type bakeriesCount: int

        :return: Daily amount of wheat flour needed.
        :rtype: int

        :raises ValueError: If bakeries count is negative.
        """
        if bakeriesCount < 0:
            raise ValueError("Bakeries count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        wheatFlourInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.MAPLE_PASTRIES,
            "Wheat Flour")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        wheatFlourPerBakeryPerDay = wheatFlourInput * cyclesPerDay

        return math.ceil(bakeriesCount * wheatFlourPerBakeryPerDay)

    def getMapleSyrupNeededForBakeriesWithMaplePastries(
            self, bakeriesCount: int) -> int:
        """
        Calculate the number of maple syrup needed per day to keep a given
        number of bakeries running producing maple pastries.

        :param bakeriesCount: Number of bakeries.
        :type bakeriesCount: int

        :return: Daily amount of maple syrup needed.
        :rtype: int

        :raises ValueError: If bakeries count is negative.
        """
        if bakeriesCount < 0:
            raise ValueError("Bakeries count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        mapleSyrupInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.MAPLE_PASTRIES,
            HarvestName.MAPLE_SYRUP.value)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        mapleSyrupPerBakeryPerDay = mapleSyrupInput * cyclesPerDay

        return math.ceil(bakeriesCount * mapleSyrupPerBakeryPerDay)

    def getLogsNeededForBakeriesWithMaplePastries(self,
                                                  bakeriesCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number
        of bakeries running producing maple pastries.

        :param bakeriesCount: Number of bakeries.
        :type bakeriesCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If bakeries count is negative.
        """
        if bakeriesCount < 0:
            raise ValueError("Bakeries count cannot be negative.")

        recipeIndex = self.factionData.getFoodProcessingRecipeIndex(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.BAKERY, recipeIndex)
        logInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.BAKERY,
            FoodRecipeName.MAPLE_PASTRIES,
            "Logs")

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerBakeryPerDay = logInput * cyclesPerDay

        return bakeriesCount * logsPerBakeryPerDay
