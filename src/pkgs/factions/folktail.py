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

