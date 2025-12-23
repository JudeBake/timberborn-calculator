import math

from ..data.enumerators import ConsumptionType, CropName, DifficultyLevel
from ..data.enumerators import FoodProcessingBuildingName, FoodRecipeName
from ..data.enumerators import GoodsBuildingName, GoodsRecipeName
from ..data.enumerators import HarvestName, TreeName, WaterBuildingName
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

        baseConsumption = self.factionData.getConsumption(ConsumptionType.FOOD)
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

        baseConsumption = self.factionData \
            .getConsumption(ConsumptionType.WATER)
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

    def getDandelionTilesNeeded(self, dandelionAmount: float) -> int:
        """
        Calculate the number of dandelion tiles needed to produce a given
        amount of dandelions per day.

        :param dandelionAmount: Daily amount of dandelions needed.
        :type dandelionAmount: float

        :return: Number of dandelion tiles needed.
        :rtype: int

        :raises ValueError: If dandelion amount is negative.
        """
        if dandelionAmount < 0:
            raise ValueError("Dandelion amount cannot be negative.")

        harvestTime = self.factionData.getCropHarvestTime(
            CropName.DANDELION_BUSH)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.DANDELION_BUSH)
        productionPerTile = harvestYield / harvestTime

        return math.ceil(dandelionAmount / productionPerTile)

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

        growthTime = self.factionData.getTreeGrowthTime(TreeName.CHESTNUT_TREE)
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_POTATOES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGrill = (outputQuantity / productionTime) * 24

        return math.ceil(grilledPotatoAmount / productionPerGrill)

    def getPotatoesNeededForGrilledPotatoesProduction(self,
                                                      grillsCount: int) -> int:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_POTATOES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        potatoInput = self.factionData.getFoodProcessingInputQuantity(
            FoodProcessingBuildingName.GRILL, FoodRecipeName.GRILLED_POTATOES,
            HarvestName.POTATOES)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        potatoesPerGrillPerDay = potatoInput * cyclesPerDay

        return math.ceil(grillsCount * potatoesPerGrillPerDay)

    def getLogsNeededForGrilledPotatoesProduction(self,
                                                  grillsCount: int) -> float:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_POTATOES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        logInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.GRILL,
                                            FoodRecipeName.GRILLED_POTATOES,
                                            HarvestName.LOGS)

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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_CHESTNUTS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGrill = (outputQuantity / productionTime) * 24

        return math.ceil(grilledChestnutAmount / productionPerGrill)

    def getChestnutsNeededForGrilledChestnutsProduction(self,
                                                        grillsCount: int
                                                        ) -> int:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_CHESTNUTS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        chestnutInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.GRILL,
                                            FoodRecipeName.GRILLED_CHESTNUTS,
                                            HarvestName.CHESTNUTS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        chestnutsPerGrillPerDay = chestnutInput * cyclesPerDay

        return math.ceil(grillsCount * chestnutsPerGrillPerDay)

    def getLogsNeededForGrilledChestnutsProduction(self,
                                                   grillsCount: int) -> float:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_CHESTNUTS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        logInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.GRILL,
                                            FoodRecipeName.GRILLED_CHESTNUTS,
                                            HarvestName.LOGS)

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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_SPADDERDOCKS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGrill = (outputQuantity / productionTime) * 24

        return math.ceil(grilledSpadderdockAmount / productionPerGrill)

    def getSpadderdocksNeededForGrilledSpadderdocksProduction(self,
                                                              grillsCount: int
                                                              ) -> int:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_SPADDERDOCKS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        spadderdockInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.GRILL,
                                            FoodRecipeName.GRILLED_SPADDERDOCKS,    # noqa: E501
                                            HarvestName.SPADDERDOCKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        spadderdocksPerGrillPerDay = spadderdockInput * cyclesPerDay

        return math.ceil(grillsCount * spadderdocksPerGrillPerDay)

    def getLogsNeededForGrilledSpadderdocksProduction(self,
                                                      grillsCount: int
                                                      ) -> float:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRILL,
                                          FoodRecipeName.GRILLED_SPADDERDOCKS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRILL,
                                             recipeIndex)
        logInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.GRILL,
                                            FoodRecipeName.GRILLED_SPADDERDOCKS,    # noqa: E501
                                            HarvestName.LOGS)

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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRISTMILL,
                                          FoodRecipeName.WHEAT_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRISTMILL,  # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.GRISTMILL,  # noqa: E501
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGristmill = (outputQuantity / productionTime) * 24

        return math.ceil(wheatFlourAmount / productionPerGristmill)

    def getWheatNeededForWheatFlourProduction(self,
                                              gristmillsCount: int) -> int:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRISTMILL,
                                          FoodRecipeName.WHEAT_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRISTMILL,  # noqa: E501
                                             recipeIndex)
        wheatInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.GRISTMILL,   # noqa: E501
                                            FoodRecipeName.WHEAT_FLOUR,
                                            HarvestName.WHEAT)

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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRISTMILL,
                                          FoodRecipeName.CATTAIL_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRISTMILL,  # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.GRISTMILL,  # noqa: E501
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGristmill = (outputQuantity / productionTime) * 24

        return math.ceil(cattailFlourAmount / productionPerGristmill)

    def getCattailRootsNeededForCattailFlourProduction(self,
                                                       gristmillsCount: int
                                                       ) -> int:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.GRISTMILL,
                                          FoodRecipeName.CATTAIL_FLOUR)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.GRISTMILL,  # noqa: E501
                                             recipeIndex)
        cattailRootsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.GRISTMILL,   # noqa: E501
                                            FoodRecipeName.CATTAIL_FLOUR,
                                            HarvestName.CATTAIL_ROOTS)

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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.BREADS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBakery = (outputQuantity / productionTime) * 24

        return math.ceil(breadsAmount / productionPerBakery)

    def getWheatFlourNeededForBreadsProduction(self,
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.BREADS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        wheatFlourInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.BAKERY,
                                            FoodRecipeName.BREADS,
                                            FoodRecipeName.WHEAT_FLOUR)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        wheatFlourPerBakeryPerDay = wheatFlourInput * cyclesPerDay

        return math.ceil(bakeriesCount * wheatFlourPerBakeryPerDay)

    def getLogsNeededForBreadsProduction(self, bakeriesCount: int) -> float:
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.BREADS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        logInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.BAKERY,
                                            FoodRecipeName.BREADS,
                                            HarvestName.LOGS)

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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.CATTAIL_CRACKERS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBakery = (outputQuantity / productionTime) * 24

        return math.ceil(cattailCrackersAmount / productionPerBakery)

    def getCattailFlourNeededForCattailCrackersProduction(self,
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.CATTAIL_CRACKERS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        cattailFlourInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.BAKERY,
                                            FoodRecipeName.CATTAIL_CRACKERS,
                                            FoodRecipeName.CATTAIL_FLOUR)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        cattailFlourPerBakeryPerDay = cattailFlourInput * cyclesPerDay

        return math.ceil(bakeriesCount * cattailFlourPerBakeryPerDay)

    def getLogsNeededForCattailCrackersProduction(self,
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.CATTAIL_CRACKERS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        logInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.BAKERY,
                                            FoodRecipeName.CATTAIL_CRACKERS,
                                            HarvestName.LOGS)

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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBakery = (outputQuantity / productionTime) * 24

        return math.ceil(maplePastriesAmount / productionPerBakery)

    def getWheatFlourNeededForMaplePastriesProduction(self,
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        wheatFlourInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.BAKERY,
                                            FoodRecipeName.MAPLE_PASTRIES,
                                            FoodRecipeName.WHEAT_FLOUR)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        wheatFlourPerBakeryPerDay = wheatFlourInput * cyclesPerDay

        return math.ceil(bakeriesCount * wheatFlourPerBakeryPerDay)

    def getMapleSyrupNeededForMaplePastriesProduction(
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        mapleSyrupInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.BAKERY,
                                            FoodRecipeName.MAPLE_PASTRIES,
                                            HarvestName.MAPLE_SYRUP)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        mapleSyrupPerBakeryPerDay = mapleSyrupInput * cyclesPerDay

        return math.ceil(bakeriesCount * mapleSyrupPerBakeryPerDay)

    def getLogsNeededForMaplePastriesProduction(self,
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

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.BAKERY,
                                          FoodRecipeName.MAPLE_PASTRIES)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.BAKERY,
                                             recipeIndex)
        logInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.BAKERY,
                                            FoodRecipeName.MAPLE_PASTRIES,
                                            HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerBakeryPerDay = logInput * cyclesPerDay

        return bakeriesCount * logsPerBakeryPerDay

    def getLumberMillsNeededForPlanks(self, planksAmount: float) -> int:
        """
        Calculate the number of lumber mills needed to produce a given amount
        of planks per day.

        :param planksAmount: Daily amount of planks needed.
        :type planksAmount: float

        :return: Number of lumber mills needed.
        :rtype: int

        :raises ValueError: If planks amount is negative.
        """
        if planksAmount < 0:
            raise ValueError("Planks amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.LUMBER_MILL,
                                 GoodsRecipeName.PLANKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.LUMBER_MILL, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.LUMBER_MILL, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerLumberMill = (outputQuantity / productionTime) * 24

        return math.ceil(planksAmount / productionPerLumberMill)

    def getLogsNeededForPlanksProduction(self, lumberMillsCount: int) -> int:
        """
        Calculate the number of logs needed per day to keep a given number of
        lumber mills running producing planks.

        :param lumberMillsCount: Number of lumber mills.
        :type lumberMillsCount: int

        :return: Daily amount of logs needed.
        :rtype: int

        :raises ValueError: If lumber mills count is negative.
        """
        if lumberMillsCount < 0:
            raise ValueError("Lumber mills count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.LUMBER_MILL,
                                 GoodsRecipeName.PLANKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.LUMBER_MILL, recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.LUMBER_MILL,
                                   GoodsRecipeName.PLANKS,
                                   HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerLumberMillPerDay = logsInput * cyclesPerDay

        return math.ceil(lumberMillsCount * logsPerLumberMillPerDay)

    def getGearWorkshopsNeededForGears(self, gearsAmount: float) -> int:
        """
        Calculate the number of gear workshops needed to produce a given
        amount of gears per day.

        :param gearsAmount: Daily amount of gears needed.
        :type gearsAmount: float

        :return: Number of gear workshops needed.
        :rtype: int

        :raises ValueError: If gears amount is negative.
        """
        if gearsAmount < 0:
            raise ValueError("Gears amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.GEAR_WORKSHOP,
                                 GoodsRecipeName.GEARS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.GEAR_WORKSHOP,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.GEAR_WORKSHOP,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerGearWorkshop = (outputQuantity / productionTime) * 24

        return math.ceil(gearsAmount / productionPerGearWorkshop)

    def getPlanksNeededForGearsProduction(self,
                                          gearWorkshopsCount: int) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of gear workshops running producing gears.

        :param gearWorkshopsCount: Number of gear workshops.
        :type gearWorkshopsCount: int

        :return: Daily amount of planks needed.
        :rtype: int

        :raises ValueError: If gear workshops count is negative.
        """
        if gearWorkshopsCount < 0:
            raise ValueError("Gear workshops count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.GEAR_WORKSHOP,
                                 GoodsRecipeName.GEARS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.GEAR_WORKSHOP,
                                    recipeIndex)
        planksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.GEAR_WORKSHOP,
                                   GoodsRecipeName.GEARS,
                                   GoodsRecipeName.PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        planksPerGearWorkshopPerDay = planksInput * cyclesPerDay

        return math.ceil(gearWorkshopsCount * planksPerGearWorkshopPerDay)

    def getPaperMillsNeededForPaper(self, paperAmount: float) -> int:
        """
        Calculate the number of paper mills needed to produce a given amount
        of paper per day.

        :param paperAmount: Daily amount of paper needed.
        :type paperAmount: float

        :return: Number of paper mills needed.
        :rtype: int

        :raises ValueError: If paper amount is negative.
        """
        if paperAmount < 0:
            raise ValueError("Paper amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.PAPER_MILL,
                                 GoodsRecipeName.PAPER)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.PAPER_MILL, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.PAPER_MILL, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerPaperMill = (outputQuantity / productionTime) * 24

        return math.ceil(paperAmount / productionPerPaperMill)

    def getLogsNeededForPaperProduction(self, paperMillsCount: int) -> int:
        """
        Calculate the number of logs needed per day to keep a given number of
        paper mills running producing paper.

        :param paperMillsCount: Number of paper mills.
        :type paperMillsCount: int

        :return: Daily amount of logs needed.
        :rtype: int

        :raises ValueError: If paper mills count is negative.
        """
        if paperMillsCount < 0:
            raise ValueError("Paper mills count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.PAPER_MILL,
                                 GoodsRecipeName.PAPER)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.PAPER_MILL, recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.PAPER_MILL,
                                   GoodsRecipeName.PAPER,
                                   HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerPaperMillPerDay = logsInput * cyclesPerDay

        return math.ceil(paperMillsCount * logsPerPaperMillPerDay)

    def getPrintingPressesNeededForBooks(self, booksAmount: float) -> int:
        """
        Calculate the number of printing presses needed to produce a given
        amount of books per day.

        :param booksAmount: Daily amount of books needed.
        :type booksAmount: float

        :return: Number of printing presses needed.
        :rtype: int

        :raises ValueError: If books amount is negative.
        """
        if booksAmount < 0:
            raise ValueError("Books amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.PRINTING_PRESS,
                                 GoodsRecipeName.BOOKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.PRINTING_PRESS,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.PRINTING_PRESS,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerPrintingPress = (outputQuantity / productionTime) * 24

        return math.ceil(booksAmount / productionPerPrintingPress)

    def getPaperNeededForBooksProduction(self,
                                         printingPressesCount: int) -> int:
        """
        Calculate the number of paper needed per day to keep a given number of
        printing presses running producing books.

        :param printingPressesCount: Number of printing presses.
        :type printingPressesCount: int

        :return: Daily amount of paper needed.
        :rtype: int

        :raises ValueError: If printing presses count is negative.
        """
        if printingPressesCount < 0:
            raise ValueError("Printing presses count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.PRINTING_PRESS,
                                 GoodsRecipeName.BOOKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.PRINTING_PRESS,
                                    recipeIndex)
        paperInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.PRINTING_PRESS,
                                   GoodsRecipeName.BOOKS,
                                   GoodsRecipeName.PAPER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        paperPerPrintingPressPerDay = paperInput * cyclesPerDay

        return math.ceil(printingPressesCount * paperPerPrintingPressPerDay)

    def getPrintingPressesNeededForPunchcards(self,
                                              punchcardsAmount: float) -> int:
        """
        Calculate the number of printing presses needed to produce a given
        amount of punchcards per day.

        :param punchcardsAmount: Daily amount of punchcards needed.
        :type punchcardsAmount: float

        :return: Number of printing presses needed.
        :rtype: int

        :raises ValueError: If punchcards amount is negative.
        """
        if punchcardsAmount < 0:
            raise ValueError("Punchcards amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.PRINTING_PRESS,
                                 GoodsRecipeName.PUNCHCARDS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.PRINTING_PRESS,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.PRINTING_PRESS,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerPrintingPress = (outputQuantity / productionTime) * 24

        return math.ceil(punchcardsAmount / productionPerPrintingPress)

    def getPaperNeededForPunchcardsProduction(self,
                                              printingPressesCount: int
                                              ) -> int:
        """
        Calculate the number of paper needed per day to keep a given number of
        printing presses running producing punchcards.

        :param printingPressesCount: Number of printing presses.
        :type printingPressesCount: int

        :return: Daily amount of paper needed.
        :rtype: int

        :raises ValueError: If printing presses count is negative.
        """
        if printingPressesCount < 0:
            raise ValueError("Printing presses count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.PRINTING_PRESS,
                                 GoodsRecipeName.PUNCHCARDS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.PRINTING_PRESS,
                                    recipeIndex)
        paperInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.PRINTING_PRESS,
                                   GoodsRecipeName.PUNCHCARDS,
                                   GoodsRecipeName.PAPER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        paperPerPrintingPressPerDay = paperInput * cyclesPerDay

        return math.ceil(printingPressesCount * paperPerPrintingPressPerDay)

    def getPlanksNeededForPunchcardsProduction(self,
                                               printingPressesCount: int
                                               ) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of printing presses running producing punchcards.

        :param printingPressesCount: Number of printing presses.
        :type printingPressesCount: int

        :return: Daily amount of planks needed.
        :rtype: int

        :raises ValueError: If printing presses count is negative.
        """
        if printingPressesCount < 0:
            raise ValueError("Printing presses count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.PRINTING_PRESS,
                                 GoodsRecipeName.PUNCHCARDS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.PRINTING_PRESS,
                                    recipeIndex)
        planksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.PRINTING_PRESS,
                                   GoodsRecipeName.PUNCHCARDS,
                                   GoodsRecipeName.PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        planksPerPrintingPressPerDay = planksInput * cyclesPerDay

        return math.ceil(printingPressesCount * planksPerPrintingPressPerDay)

    def getWoodWorkshopsNeededForTreatedPlanks(self,
                                               treatedPlanksAmount: float
                                               ) -> int:
        """
        Calculate the number of wood workshops needed to produce a given
        amount of treated planks per day.

        :param treatedPlanksAmount: Daily amount of treated planks needed.
        :type treatedPlanksAmount: float

        :return: Number of wood workshops needed.
        :rtype: int

        :raises ValueError: If treated planks amount is negative.
        """
        if treatedPlanksAmount < 0:
            raise ValueError("Treated planks amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.WOOD_WORKSHOP,
                                 GoodsRecipeName.TREATED_PLANKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.WOOD_WORKSHOP,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.WOOD_WORKSHOP,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerWoodWorkshop = (outputQuantity / productionTime) * 24

        return math.ceil(treatedPlanksAmount / productionPerWoodWorkshop)

    def getPineResinNeededForTreatedPlanksProduction(self,
                                                     woodWorkshopsCount: int
                                                     ) -> int:
        """
        Calculate the number of pine resin needed per day to keep a given
        number of wood workshops running producing treated planks.

        :param woodWorkshopsCount: Number of wood workshops.
        :type woodWorkshopsCount: int

        :return: Daily amount of pine resin needed.
        :rtype: int

        :raises ValueError: If wood workshops count is negative.
        """
        if woodWorkshopsCount < 0:
            raise ValueError("Wood workshops count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.WOOD_WORKSHOP,
                                 GoodsRecipeName.TREATED_PLANKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.WOOD_WORKSHOP,
                                    recipeIndex)
        pineResinInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.WOOD_WORKSHOP,
                                   GoodsRecipeName.TREATED_PLANKS,
                                   HarvestName.PINE_RESIN)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        pineResinPerWoodWorkshopPerDay = pineResinInput * cyclesPerDay

        return math.ceil(woodWorkshopsCount * pineResinPerWoodWorkshopPerDay)

    def getPlanksNeededForTreatedPlanksProduction(self,
                                                  woodWorkshopsCount: int
                                                  ) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of wood workshops running producing treated planks.

        :param woodWorkshopsCount: Number of wood workshops.
        :type woodWorkshopsCount: int

        :return: Daily amount of planks needed.
        :rtype: int

        :raises ValueError: If wood workshops count is negative.
        """
        if woodWorkshopsCount < 0:
            raise ValueError("Wood workshops count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.WOOD_WORKSHOP,
                                 GoodsRecipeName.TREATED_PLANKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.WOOD_WORKSHOP,
                                    recipeIndex)
        planksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.WOOD_WORKSHOP,
                                   GoodsRecipeName.TREATED_PLANKS,
                                   GoodsRecipeName.PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        planksPerWoodWorkshopPerDay = planksInput * cyclesPerDay

        return math.ceil(woodWorkshopsCount * planksPerWoodWorkshopPerDay)

    def getSmeltersNeededForMetalBlocks(self, metalBlocksAmount: float) -> int:
        """
        Calculate the number of smelters needed to produce a given amount of
        metal blocks per day.

        :param metalBlocksAmount: Daily amount of metal blocks needed.
        :type metalBlocksAmount: float

        :return: Number of smelters needed.
        :rtype: int

        :raises ValueError: If metal blocks amount is negative.
        """
        if metalBlocksAmount < 0:
            raise ValueError("Metal blocks amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.SMELTER,
                                 GoodsRecipeName.METAL_BLOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.SMELTER, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.SMELTER, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerSmelter = (outputQuantity / productionTime) * 24

        return math.ceil(metalBlocksAmount / productionPerSmelter)

    def getScrapMetalNeededForMetalBlocksProduction(self,
                                                    smeltersCount: int) -> int:
        """
        Calculate the number of scrap metal needed per day to keep a given
        number of smelters running producing metal blocks.

        :param smeltersCount: Number of smelters.
        :type smeltersCount: int

        :return: Daily amount of scrap metal needed.
        :rtype: int

        :raises ValueError: If smelters count is negative.
        """
        if smeltersCount < 0:
            raise ValueError("Smelters count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.SMELTER,
                                 GoodsRecipeName.METAL_BLOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.SMELTER, recipeIndex)
        scrapMetalInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.SMELTER,
                                   GoodsRecipeName.METAL_BLOCKS,
                                   GoodsRecipeName.SCRAP_METAL)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        scrapMetalPerSmelterPerDay = scrapMetalInput * cyclesPerDay

        return math.ceil(smeltersCount * scrapMetalPerSmelterPerDay)

    def getLogsNeededForMetalBlocksProduction(self,
                                              smeltersCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number of
        smelters running producing metal blocks.

        :param smeltersCount: Number of smelters.
        :type smeltersCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If smelters count is negative.
        """
        if smeltersCount < 0:
            raise ValueError("Smelters count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.SMELTER,
                                 GoodsRecipeName.METAL_BLOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.SMELTER, recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.SMELTER,
                                   GoodsRecipeName.METAL_BLOCKS,
                                   HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerSmelterPerDay = logsInput * cyclesPerDay

        return smeltersCount * logsPerSmelterPerDay

    def getMinesNeededForScrapMetal(self, scrapMetalAmount: float) -> int:
        """
        Calculate the number of mines needed to produce a given amount of
        scrap metal per day.

        :param scrapMetalAmount: Daily amount of scrap metal needed.
        :type scrapMetalAmount: float

        :return: Number of mines needed.
        :rtype: int

        :raises ValueError: If scrap metal amount is negative.
        """
        if scrapMetalAmount < 0:
            raise ValueError("Scrap metal amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.MINE,
                                 GoodsRecipeName.SCRAP_METAL)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.MINE, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.MINE, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerMine = (outputQuantity / productionTime) * 24

        return math.ceil(scrapMetalAmount / productionPerMine)

    def getTreatedPlanksNeededForScrapMetalProduction(self,
                                                      minesCount: int) -> int:
        """
        Calculate the number of treated planks needed per day to keep a given
        number of mines running producing scrap metal.

        :param minesCount: Number of mines.
        :type minesCount: int

        :return: Daily amount of treated planks needed.
        :rtype: int

        :raises ValueError: If mines count is negative.
        """
        if minesCount < 0:
            raise ValueError("Mines count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.MINE,
                                 GoodsRecipeName.SCRAP_METAL)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.MINE, recipeIndex)
        treatedPlanksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.MINE,
                                   GoodsRecipeName.SCRAP_METAL,
                                   GoodsRecipeName.TREATED_PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        treatedPlanksPerMinePerDay = treatedPlanksInput * cyclesPerDay

        return math.ceil(minesCount * treatedPlanksPerMinePerDay)

    def getRefineriesNeededForBiofuelCarrots(self,
                                             biofuelCarrotsAmount: float
                                             ) -> int:
        """
        Calculate the number of refineries needed to produce a given amount of
        biofuel per day using carrots.

        :param biofuelCarrotsAmount: Daily amount of biofuel needed.
        :type biofuelCarrotsAmount: float

        :return: Number of refineries needed.
        :rtype: int

        :raises ValueError: If biofuel carrots amount is negative.
        """
        if biofuelCarrotsAmount < 0:
            raise ValueError("Biofuel Carrots amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_CARROTS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.REFINERY, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerRefinery = (outputQuantity / productionTime) * 24

        return math.ceil(biofuelCarrotsAmount / productionPerRefinery)

    def getCarrotsNeededForBiofuelCarrotsProduction(self,
                                                    refineriesCount: int
                                                    ) -> int:
        """
        Calculate the number of carrots needed per day to keep a given number
        of refineries running producing biofuel with carrots.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of carrots needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_CARROTS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        carrotsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.BIOFUEL_CARROTS,
                                   HarvestName.CARROTS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        carrotsPerRefineryPerDay = carrotsInput * cyclesPerDay

        return math.ceil(refineriesCount * carrotsPerRefineryPerDay)

    def getWaterNeededForBiofuelCarrotsProduction(self,
                                                  refineriesCount: int
                                                  ) -> int:
        """
        Calculate the number of water needed per day to keep a given number of
        refineries running producing biofuel with carrots.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of water needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_CARROTS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        waterInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.BIOFUEL_CARROTS,
                                   HarvestName.WATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        waterPerRefineryPerDay = waterInput * cyclesPerDay

        return math.ceil(refineriesCount * waterPerRefineryPerDay)

    def getRefineriesNeededForBiofuelPotatoes(self,
                                              biofuelPotatoesAmount: float
                                              ) -> int:
        """
        Calculate the number of refineries needed to produce a given amount of
        biofuel per day using potatoes.

        :param biofuelPotatoesAmount: Daily amount of biofuel needed.
        :type biofuelPotatoesAmount: float

        :return: Number of refineries needed.
        :rtype: int

        :raises ValueError: If biofuel potatoes amount is negative.
        """
        if biofuelPotatoesAmount < 0:
            raise ValueError("Biofuel Potatoes amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_POTATOES)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.REFINERY, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerRefinery = (outputQuantity / productionTime) * 24

        return math.ceil(biofuelPotatoesAmount / productionPerRefinery)

    def getPotatoesNeededForBiofuelPotatoesProduction(self,
                                                      refineriesCount: int
                                                      ) -> int:
        """
        Calculate the number of potatoes needed per day to keep a given number
        of refineries running producing biofuel with potatoes.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of potatoes needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_POTATOES)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        potatoesInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.BIOFUEL_POTATOES,
                                   HarvestName.POTATOES)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        potatoesPerRefineryPerDay = potatoesInput * cyclesPerDay

        return math.ceil(refineriesCount * potatoesPerRefineryPerDay)

    def getWaterNeededForBiofuelPotatoesProduction(self,
                                                   refineriesCount: int
                                                   ) -> int:
        """
        Calculate the number of water needed per day to keep a given number of
        refineries running producing biofuel with potatoes.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of water needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_POTATOES)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        waterInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.BIOFUEL_POTATOES,
                                   HarvestName.WATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        waterPerRefineryPerDay = waterInput * cyclesPerDay

        return math.ceil(refineriesCount * waterPerRefineryPerDay)

    def getRefineriesNeededForBiofuelSpadderdocks(self,
                                                  biofuelSpadderdocksAmount: float) -> int:     # noqa: E501
        """
        Calculate the number of refineries needed to produce a given amount of
        biofuel per day using spadderdocks.

        :param biofuelSpadderdocksAmount: Daily amount of biofuel needed.
        :type biofuelSpadderdocksAmount: float

        :return: Number of refineries needed.
        :rtype: int

        :raises ValueError: If biofuel spadderdocks amount is negative.
        """
        if biofuelSpadderdocksAmount < 0:
            raise ValueError("Biofuel Spadderdocks amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_SPADDERDOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.REFINERY, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerRefinery = (outputQuantity / productionTime) * 24

        return math.ceil(biofuelSpadderdocksAmount / productionPerRefinery)

    def getSpadderdocksNeededForBiofuelSpadderdocksProduction(self,
                                                              refineriesCount: int) -> int:     # noqa: E501
        """
        Calculate the number of spadderdocks needed per day to keep a given
        number of refineries running producing biofuel with spadderdocks.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of spadderdocks needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_SPADDERDOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        # Note: YAML has typo "Spadderdocks" instead of "Spadderdocks"
        spadderdocksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.BIOFUEL_SPADDERDOCKS,
                                   HarvestName.SPADDERDOCKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        spadderdocksPerRefineryPerDay = spadderdocksInput * cyclesPerDay

        return math.ceil(refineriesCount * spadderdocksPerRefineryPerDay)

    def getWaterNeededForBiofuelSpadderdocksProduction(self,
                                                       refineriesCount: int
                                                       ) -> int:
        """
        Calculate the number of water needed per day to keep a given number of
        refineries running producing biofuel with spadderdocks.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of water needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.BIOFUEL_SPADDERDOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        waterInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.BIOFUEL_SPADDERDOCKS,
                                   HarvestName.WATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        waterPerRefineryPerDay = waterInput * cyclesPerDay

        return math.ceil(refineriesCount * waterPerRefineryPerDay)

    def getRefineriesNeededForCatalyst(self, catalystAmount: float) -> int:
        """
        Calculate the number of refineries needed to produce a given amount of
        catalyst per day.

        :param catalystAmount: Daily amount of catalyst needed.
        :type catalystAmount: float

        :return: Number of refineries needed.
        :rtype: int

        :raises ValueError: If catalyst amount is negative.
        """
        if catalystAmount < 0:
            raise ValueError("Catalyst amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.CATALYST)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.REFINERY, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerRefinery = (outputQuantity / productionTime) * 24

        return math.ceil(catalystAmount / productionPerRefinery)

    def getMapleSyrupNeededForCatalystProduction(self,
                                                 refineriesCount: int
                                                 ) -> int:
        """
        Calculate the number of maple syrup needed per day to keep a given
        number of refineries running producing catalyst.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of maple syrup needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.CATALYST)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        mapleSyrupInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.CATALYST,
                                   HarvestName.MAPLE_SYRUP)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        mapleSyrupPerRefineryPerDay = mapleSyrupInput * cyclesPerDay

        return math.ceil(refineriesCount * mapleSyrupPerRefineryPerDay)

    def getExtractNeededForCatalystProduction(self,
                                              refineriesCount: int) -> int:
        """
        Calculate the number of extract needed per day to keep a given number
        of refineries running producing catalyst.

        :param refineriesCount: Number of refineries.
        :type refineriesCount: int

        :return: Daily amount of extract needed.
        :rtype: int

        :raises ValueError: If refineries count is negative.
        """
        if refineriesCount < 0:
            raise ValueError("Refineries count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.REFINERY,
                                 GoodsRecipeName.CATALYST)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.REFINERY, recipeIndex)
        extractInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.REFINERY,
                                   GoodsRecipeName.CATALYST,
                                   GoodsRecipeName.EXTRACT)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        extractPerRefineryPerDay = extractInput * cyclesPerDay

        return math.ceil(refineriesCount * extractPerRefineryPerDay)

    def getBotPartFactoriesNeededForBotChassis(self,
                                               botChassisAmount: float) -> int:
        """
        Calculate the number of bot part factories needed to produce a given
        amount of bot chassis per day.

        :param botChassisAmount: Daily amount of bot chassis needed.
        :type botChassisAmount: float

        :return: Number of bot part factories needed.
        :rtype: int

        :raises ValueError: If bot chassis amount is negative.
        """
        if botChassisAmount < 0:
            raise ValueError("Bot Chassis amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_CHASSIS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBotPartFactory = (outputQuantity / productionTime) * 24

        return math.ceil(botChassisAmount / productionPerBotPartFactory)

    def getPlanksNeededForBotChassisProduction(self,
                                               botPartFactoriesCount: int
                                               ) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of bot part factories running producing bot chassis.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of planks needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_CHASSIS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        planksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_CHASSIS,
                                   GoodsRecipeName.PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        planksPerBotPartFactoryPerDay = planksInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount * planksPerBotPartFactoryPerDay)

    def getMetalBlocksNeededForBotChassisProduction(self,
                                                    botPartFactoriesCount: int
                                                    ) -> int:
        """
        Calculate the number of metal blocks needed per day to keep a given
        number of bot part factories running producing bot chassis.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of metal blocks needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_CHASSIS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        metalBlocksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_CHASSIS,
                                   GoodsRecipeName.METAL_BLOCKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        metalBlocksPerBotPartFactoryPerDay = metalBlocksInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount *
                         metalBlocksPerBotPartFactoryPerDay)

    def getBiofuelNeededForBotChassisProduction(self,
                                                botPartFactoriesCount: int
                                                ) -> int:
        """
        Calculate the number of biofuel needed per day to keep a given number
        of bot part factories running producing bot chassis.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of biofuel needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_CHASSIS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        biofuelInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_CHASSIS,
                                   GoodsRecipeName.BIOFUEL)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        biofuelPerBotPartFactoryPerDay = biofuelInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount *
                         biofuelPerBotPartFactoryPerDay)

    def getBotPartFactoriesNeededForBotHeads(self,
                                             botHeadsAmount: float) -> int:
        """
        Calculate the number of bot part factories needed to produce a given
        amount of bot heads per day.

        :param botHeadsAmount: Daily amount of bot heads needed.
        :type botHeadsAmount: float

        :return: Number of bot part factories needed.
        :rtype: int

        :raises ValueError: If bot heads amount is negative.
        """
        if botHeadsAmount < 0:
            raise ValueError("Bot Heads amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_HEADS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBotPartFactory = (outputQuantity / productionTime) * 24

        return math.ceil(botHeadsAmount / productionPerBotPartFactory)

    def getGearsNeededForBotHeadsProduction(self,
                                            botPartFactoriesCount: int) -> int:
        """
        Calculate the number of gears needed per day to keep a given number of
        bot part factories running producing bot heads.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of gears needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_HEADS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        gearsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_HEADS,
                                   GoodsRecipeName.GEARS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        gearsPerBotPartFactoryPerDay = gearsInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount * gearsPerBotPartFactoryPerDay)

    def getMetalBlocksNeededForBotHeadsProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of metal blocks needed per day to keep a given
        number of bot part factories running producing bot heads.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of metal blocks needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_HEADS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        metalBlocksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_HEADS,
                                   GoodsRecipeName.METAL_BLOCKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        metalBlocksPerBotPartFactoryPerDay = metalBlocksInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount *
                         metalBlocksPerBotPartFactoryPerDay)

    def getPlanksNeededForBotHeadsProduction(self,
                                             botPartFactoriesCount: int
                                             ) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of bot part factories running producing bot heads.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of planks needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_HEADS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        planksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_HEADS,
                                   GoodsRecipeName.PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        planksPerBotPartFactoryPerDay = planksInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount * planksPerBotPartFactoryPerDay)

    def getBotPartFactoriesNeededForBotLimbs(self,
                                             botLimbsAmount: float) -> int:
        """
        Calculate the number of bot part factories needed to produce a given
        amount of bot limbs per day.

        :param botLimbsAmount: Daily amount of bot limbs needed.
        :type botLimbsAmount: float

        :return: Number of bot part factories needed.
        :rtype: int

        :raises ValueError: If bot limbs amount is negative.
        """
        if botLimbsAmount < 0:
            raise ValueError("Bot Limbs amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_LIMBS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBotPartFactory = (outputQuantity / productionTime) * 24

        return math.ceil(botLimbsAmount / productionPerBotPartFactory)

    def getGearsNeededForBotLimbsProduction(self,
                                            botPartFactoriesCount: int) -> int:
        """
        Calculate the number of gears needed per day to keep a given number of
        bot part factories running producing bot limbs.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of gears needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_LIMBS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        gearsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_LIMBS,
                                   GoodsRecipeName.GEARS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        gearsPerBotPartFactoryPerDay = gearsInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount * gearsPerBotPartFactoryPerDay)

    def getPlanksNeededForBotLimbsProduction(self,
                                             botPartFactoriesCount: int
                                             ) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of bot part factories running producing bot limbs.

        :param botPartFactoriesCount: Number of bot part factories.
        :type botPartFactoriesCount: int

        :return: Daily amount of planks needed.
        :rtype: int

        :raises ValueError: If bot part factories count is negative.
        """
        if botPartFactoriesCount < 0:
            raise ValueError("Bot part factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_LIMBS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        planksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                   GoodsRecipeName.BOT_LIMBS,
                                   GoodsRecipeName.PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        planksPerBotPartFactoryPerDay = planksInput * cyclesPerDay

        return math.ceil(botPartFactoriesCount * planksPerBotPartFactoryPerDay)

    def getBotAssemblersNeededForBots(self, botsAmount: float) -> int:
        """
        Calculate the number of bot assemblers needed to produce a given
        amount of bots per day.

        :param botsAmount: Daily amount of bots needed.
        :type botsAmount: float

        :return: Number of bot assemblers needed.
        :rtype: int

        :raises ValueError: If bots amount is negative.
        """
        if botsAmount < 0:
            raise ValueError("Bots amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_ASSEMBLER,
                                 GoodsRecipeName.BOT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_ASSEMBLER,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.BOT_ASSEMBLER,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBotAssembler = (outputQuantity / productionTime) * 24

        return math.ceil(botsAmount / productionPerBotAssembler)

    def getBotChassisNeededForBotsProduction(self,
                                             botAssemblersCount: int) -> int:
        """
        Calculate the number of bot chassis needed per day to keep a given
        number of bot assemblers running.

        :param botAssemblersCount: Number of bot assemblers.
        :type botAssemblersCount: int

        :return: Daily amount of bot chassis needed.
        :rtype: int

        :raises ValueError: If bot assemblers count is negative.
        """
        if botAssemblersCount < 0:
            raise ValueError("Bot assemblers count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_ASSEMBLER,
                                 GoodsRecipeName.BOT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_ASSEMBLER,
                                    recipeIndex)
        botChassisInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_ASSEMBLER,
                                   GoodsRecipeName.BOT,
                                   GoodsRecipeName.BOT_CHASSIS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        botChassisPerBotAssemblerPerDay = botChassisInput * cyclesPerDay

        return math.ceil(botAssemblersCount * botChassisPerBotAssemblerPerDay)

    def getBotHeadsNeededForBotsProduction(self,
                                           botAssemblersCount: int) -> int:
        """
        Calculate the number of bot heads needed per day to keep a given
        number of bot assemblers running.

        :param botAssemblersCount: Number of bot assemblers.
        :type botAssemblersCount: int

        :return: Daily amount of bot heads needed.
        :rtype: int

        :raises ValueError: If bot assemblers count is negative.
        """
        if botAssemblersCount < 0:
            raise ValueError("Bot assemblers count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_ASSEMBLER,
                                 GoodsRecipeName.BOT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_ASSEMBLER,
                                    recipeIndex)
        botHeadsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_ASSEMBLER,
                                   GoodsRecipeName.BOT,
                                   GoodsRecipeName.BOT_HEADS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        botHeadsPerBotAssemblerPerDay = botHeadsInput * cyclesPerDay

        return math.ceil(botAssemblersCount * botHeadsPerBotAssemblerPerDay)

    def getBotLimbsNeededForBotsProduction(self,
                                           botAssemblersCount: int) -> int:
        """
        Calculate the number of bot limbs needed per day to keep a given
        number of bot assemblers running.

        :param botAssemblersCount: Number of bot assemblers.
        :type botAssemblersCount: int

        :return: Daily amount of bot limbs needed.
        :rtype: int

        :raises ValueError: If bot assemblers count is negative.
        """
        if botAssemblersCount < 0:
            raise ValueError("Bot assemblers count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_ASSEMBLER,
                                 GoodsRecipeName.BOT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_ASSEMBLER,
                                    recipeIndex)
        botLimbsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.BOT_ASSEMBLER,
                                   GoodsRecipeName.BOT,
                                   GoodsRecipeName.BOT_LIMBS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        botLimbsPerBotAssemblerPerDay = botLimbsInput * cyclesPerDay

        return math.ceil(botAssemblersCount * botLimbsPerBotAssemblerPerDay)

    def getExplosivesFactoriesNeededForExplosives(self,
                                                  explosivesAmount: float
                                                  ) -> int:
        """
        Calculate the number of explosives factories needed to produce a given
        amount of explosives per day.

        :param explosivesAmount: Daily amount of explosives needed.
        :type explosivesAmount: float

        :return: Number of explosives factories needed.
        :rtype: int

        :raises ValueError: If explosives amount is negative.
        """
        if explosivesAmount < 0:
            raise ValueError("Explosives amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.EXPLOSIVES_FACTORY,
                                 GoodsRecipeName.EXPLOSIVES)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.EXPLOSIVES_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.EXPLOSIVES_FACTORY,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerExplosivesFactory = (outputQuantity / productionTime) * 24

        return math.ceil(explosivesAmount / productionPerExplosivesFactory)

    def getBadwaterNeededForExplosivesProduction(self,
                                                 explosivesFactoriesCount: int
                                                 ) -> int:
        """
        Calculate the number of badwater needed per day to keep a given number
        of explosives factories running.

        :param explosivesFactoriesCount: Number of explosives factories.
        :type explosivesFactoriesCount: int

        :return: Daily amount of badwater needed.
        :rtype: int

        :raises ValueError: If explosives factories count is negative.
        """
        if explosivesFactoriesCount < 0:
            raise ValueError("Explosives factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.EXPLOSIVES_FACTORY,
                                 GoodsRecipeName.EXPLOSIVES)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.EXPLOSIVES_FACTORY,
                                    recipeIndex)
        badwaterInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.EXPLOSIVES_FACTORY,
                                   GoodsRecipeName.EXPLOSIVES,
                                   HarvestName.BADWATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        badwaterPerExplosivesFactoryPerDay = badwaterInput * cyclesPerDay

        return math.ceil(explosivesFactoriesCount *
                         badwaterPerExplosivesFactoryPerDay)

    def getCentrifugesNeededForExtract(self, extractAmount: float) -> int:
        """
        Calculate the number of centrifuges needed to produce a given amount
        of extract per day.

        :param extractAmount: Daily amount of extract needed.
        :type extractAmount: float

        :return: Number of centrifuges needed.
        :rtype: int

        :raises ValueError: If extract amount is negative.
        """
        if extractAmount < 0:
            raise ValueError("Extract amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.CENTRIFUGE,
                                 GoodsRecipeName.EXTRACT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.CENTRIFUGE, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.CENTRIFUGE, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerCentrifuge = (outputQuantity / productionTime) * 24

        return math.ceil(extractAmount / productionPerCentrifuge)

    def getBadwaterNeededForExtractProduction(self,
                                              centrifugesCount: int) -> int:
        """
        Calculate the number of badwater needed per day to keep a given number
        of centrifuges running.

        :param centrifugesCount: Number of centrifuges.
        :type centrifugesCount: int

        :return: Daily amount of badwater needed.
        :rtype: int

        :raises ValueError: If centrifuges count is negative.
        """
        if centrifugesCount < 0:
            raise ValueError("Centrifuges count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.CENTRIFUGE,
                                 GoodsRecipeName.EXTRACT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.CENTRIFUGE, recipeIndex)
        badwaterInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.CENTRIFUGE,
                                   GoodsRecipeName.EXTRACT,
                                   HarvestName.BADWATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        badwaterPerCentrifugePerDay = badwaterInput * cyclesPerDay

        return math.ceil(centrifugesCount * badwaterPerCentrifugePerDay)

    def getLogsNeededForExtractProduction(self, centrifugesCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number of
        centrifuges running.

        :param centrifugesCount: Number of centrifuges.
        :type centrifugesCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If centrifuges count is negative.
        """
        if centrifugesCount < 0:
            raise ValueError("Centrifuges count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.CENTRIFUGE,
                                 GoodsRecipeName.EXTRACT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.CENTRIFUGE, recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.CENTRIFUGE,
                                   GoodsRecipeName.EXTRACT,
                                   HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerCentrifugePerDay = logsInput * cyclesPerDay

        return centrifugesCount * logsPerCentrifugePerDay

    def getHerbalistsNeededForAntidote(self, antidoteAmount: float) -> int:
        """
        Calculate the number of herbalists needed to produce a given amount of
        antidote per day.

        :param antidoteAmount: Daily amount of antidote needed.
        :type antidoteAmount: float

        :return: Number of herbalists needed.
        :rtype: int

        :raises ValueError: If antidote amount is negative.
        """
        if antidoteAmount < 0:
            raise ValueError("Antidote amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.HERBALIST,
                                 GoodsRecipeName.ANTIDOTE)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.HERBALIST, recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.HERBALIST, recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerHerbalist = (outputQuantity / productionTime) * 24

        return math.ceil(antidoteAmount / productionPerHerbalist)

    def getDandelionsNeededForAntidoteProduction(self,
                                                 herbalistsCount: int) -> int:
        """
        Calculate the number of dandelions needed per day to keep a given
        number of herbalists running.

        :param herbalistsCount: Number of herbalists.
        :type herbalistsCount: int

        :return: Daily amount of dandelions needed.
        :rtype: int

        :raises ValueError: If herbalists count is negative.
        """
        if herbalistsCount < 0:
            raise ValueError("Herbalists count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.HERBALIST,
                                 GoodsRecipeName.ANTIDOTE)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.HERBALIST, recipeIndex)
        dandelionsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.HERBALIST,
                                   GoodsRecipeName.ANTIDOTE,
                                   HarvestName.DANDELIONS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        dandelionsPerHerbalistPerDay = dandelionsInput * cyclesPerDay

        return math.ceil(herbalistsCount * dandelionsPerHerbalistPerDay)

    def getBerriesNeededForAntidoteProduction(self,
                                              herbalistsCount: int) -> int:
        """
        Calculate the number of berries needed per day to keep a given number
        of herbalists running.

        :param herbalistsCount: Number of herbalists.
        :type herbalistsCount: int

        :return: Daily amount of berries needed.
        :rtype: int

        :raises ValueError: If herbalists count is negative.
        """
        if herbalistsCount < 0:
            raise ValueError("Herbalists count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.HERBALIST,
                                 GoodsRecipeName.ANTIDOTE)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.HERBALIST, recipeIndex)
        berriesInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.HERBALIST,
                                   GoodsRecipeName.ANTIDOTE,
                                   HarvestName.BERRIES)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        berriesPerHerbalistPerDay = berriesInput * cyclesPerDay

        return math.ceil(herbalistsCount * berriesPerHerbalistPerDay)

    def getPapersNeededForAntidoteProduction(self,
                                             herbalistsCount: int) -> float:
        """
        Calculate the number of papers needed per day to keep a given number of
        herbalists running.

        :param herbalistsCount: Number of herbalists.
        :type herbalistsCount: int

        :return: Daily amount of papers needed.
        :rtype: float

        :raises ValueError: If herbalists count is negative.
        """
        if herbalistsCount < 0:
            raise ValueError("Herbalists count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.HERBALIST,
                                 GoodsRecipeName.ANTIDOTE)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.HERBALIST, recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.HERBALIST,
                                   GoodsRecipeName.ANTIDOTE,
                                   GoodsRecipeName.PAPER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerHerbalistPerDay = logsInput * cyclesPerDay

        return herbalistsCount * logsPerHerbalistPerDay
