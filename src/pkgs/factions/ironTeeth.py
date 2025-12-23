import math

from ..data.enumerators import ConsumptionType, CropName, DifficultyLevel
from ..data.enumerators import FoodProcessingBuildingName, FoodRecipeName
from ..data.enumerators import GoodsBuildingName, GoodsRecipeName
from ..data.enumerators import HarvestName, TreeName, WaterBuildingName
from ..data.factionData import FactionData


class IronTeeth:
    """
    IronTeeth faction calculator class.

    This class encapsulates IronTeeth-specific faction data and provides
    methods to calculate resource requirements for an IronTeeth population.
    """

    def __init__(self) -> None:
        """
        Initialize the IronTeeth calculator with faction data.
        """
        self.factionData = FactionData('./data/ironTeeth.yml')

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

    def getLogPerType(self, totalLogAmount: float,
                      treeTypeCount: int) -> float:
        """
        Calculate the amount of logs needed per tree type, assuming equal
        distribution across the specified number of tree types.

        :param totalLogAmount: Total amount of logs needed per day.
        :type totalLogAmount: float
        :param treeTypeCount: Number of different tree types to distribute
                              log production across.
        :type treeTypeCount: int

        :return: Daily log amount needed per tree type.
        :rtype: float

        :raises ValueError: If totalLogAmount is negative or treeTypeCount
                            is not positive.
        """
        if totalLogAmount < 0:
            raise ValueError("Total log amount cannot be negative.")
        if treeTypeCount <= 0:
            raise ValueError("Tree type count must be positive.")

        return totalLogAmount / treeTypeCount

    def getDeepWaterPumpsNeeded(self, waterAmount: float) -> int:
        """
        Calculate the number of deep water pumps needed to produce a given
        amount of water per day.

        :param waterAmount: Daily amount of water needed.
        :type waterAmount: float

        :return: Number of deep water pumps needed.
        :rtype: int

        :raises ValueError: If water amount is negative.
        """
        if waterAmount < 0:
            raise ValueError("Water amount cannot be negative.")

        productionTime = self.factionData \
            .getWaterProductionTime(WaterBuildingName.DEEP_WATER_PUMP)
        outputQuantity = self.factionData \
            .getWaterOutputQuantity(WaterBuildingName.DEEP_WATER_PUMP)
        # Production time is in hours, calculate daily production
        productionPerPump = (outputQuantity / productionTime) * 24

        return math.ceil(waterAmount / productionPerPump)

    def getDeepBadwaterPumpsNeeded(self, badwaterAmount: float) -> int:
        """
        Calculate the number of deep badwater pumps needed to produce a given
        amount of badwater per day.

        :param badwaterAmount: Daily amount of badwater needed.
        :type badwaterAmount: float

        :return: Number of deep badwater pumps needed.
        :rtype: int

        :raises ValueError: If badwater amount is negative.
        """
        if badwaterAmount < 0:
            raise ValueError("Badwater amount cannot be negative.")

        productionTime = self.factionData \
            .getWaterProductionTime(WaterBuildingName.DEEP_BADWATER_PUMP)
        outputQuantity = self.factionData \
            .getWaterOutputQuantity(WaterBuildingName.DEEP_BADWATER_PUMP)
        # Production time is in hours, calculate daily production
        productionPerPump = (outputQuantity / productionTime) * 24

        return math.ceil(badwaterAmount / productionPerPump)

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

    def getCoffeeBeanTilesNeeded(self, coffeeBeanAmount: float) -> int:
        """
        Calculate the number of coffee bush tiles needed to produce a given
        amount of coffee beans per day.

        :param coffeeBeanAmount: Daily amount of coffee beans needed.
        :type coffeeBeanAmount: float

        :return: Number of coffee bush tiles needed.
        :rtype: int

        :raises ValueError: If coffee bean amount is negative.
        """
        if coffeeBeanAmount < 0:
            raise ValueError("Coffee bean amount cannot be negative.")

        harvestTime = self.factionData.getCropHarvestTime(CropName.COFFEE_BUSH)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.COFFEE_BUSH)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(coffeeBeanAmount / productionPerTile)

    def getKohlrabiTilesNeeded(self, kohlrabiAmount: float) -> int:
        """
        Calculate the number of kohlrabi tiles needed to produce a given
        amount of kohlrabies per day.

        :param kohlrabiAmount: Daily amount of kohlrabies needed.
        :type kohlrabiAmount: float

        :return: Number of kohlrabi tiles needed.
        :rtype: int

        :raises ValueError: If kohlrabi amount is negative.
        """
        if kohlrabiAmount < 0:
            raise ValueError("Kohlrabi amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.KOHLRABI_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.KOHLRABI_CROP)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(kohlrabiAmount / productionPerTile)

    def getCassavaTilesNeeded(self, cassavaAmount: float) -> int:
        """
        Calculate the number of cassava tiles needed to produce a given
        amount of cassavas per day.

        :param cassavaAmount: Daily amount of cassavas needed.
        :type cassavaAmount: float

        :return: Number of cassava tiles needed.
        :rtype: int

        :raises ValueError: If cassava amount is negative.
        """
        if cassavaAmount < 0:
            raise ValueError("Cassava amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.CASSAVA_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.CASSAVA_CROP)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(cassavaAmount / productionPerTile)

    def getSoybeanTilesNeeded(self, soybeanAmount: float) -> int:
        """
        Calculate the number of soybean tiles needed to produce a given
        amount of soybeans per day.

        :param soybeanAmount: Daily amount of soybeans needed.
        :type soybeanAmount: float

        :return: Number of soybean tiles needed.
        :rtype: int

        :raises ValueError: If soybean amount is negative.
        """
        if soybeanAmount < 0:
            raise ValueError("Soybean amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.SOYBEAN_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.SOYBEAN_CROP)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(soybeanAmount / productionPerTile)

    def getCanolaSeedTilesNeeded(self, canolaSeedAmount: float) -> int:
        """
        Calculate the number of canola tiles needed to produce a given
        amount of canola seeds per day.

        :param canolaSeedAmount: Daily amount of canola seeds needed.
        :type canolaSeedAmount: float

        :return: Number of canola tiles needed.
        :rtype: int

        :raises ValueError: If canola seed amount is negative.
        """
        if canolaSeedAmount < 0:
            raise ValueError("Canola seed amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.CANOLA_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.CANOLA_CROP)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(canolaSeedAmount / productionPerTile)

    def getCornTilesNeeded(self, cornAmount: float) -> int:
        """
        Calculate the number of corn tiles needed to produce a given
        amount of corn per day.

        :param cornAmount: Daily amount of corn needed.
        :type cornAmount: float

        :return: Number of corn tiles needed.
        :rtype: int

        :raises ValueError: If corn amount is negative.
        """
        if cornAmount < 0:
            raise ValueError("Corn amount cannot be negative.")

        harvestTime = self.factionData.getCropHarvestTime(CropName.CORN_CROP)
        harvestYield = self.factionData.getCropHarvestYield(CropName.CORN_CROP)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(cornAmount / productionPerTile)

    def getEggplantTilesNeeded(self, eggplantAmount: float) -> int:
        """
        Calculate the number of eggplant tiles needed to produce a given
        amount of eggplants per day.

        :param eggplantAmount: Daily amount of eggplants needed.
        :type eggplantAmount: float

        :return: Number of eggplant tiles needed.
        :rtype: int

        :raises ValueError: If eggplant amount is negative.
        """
        if eggplantAmount < 0:
            raise ValueError("Eggplant amount cannot be negative.")

        harvestTime = self.factionData \
            .getCropHarvestTime(CropName.EGGPLANT_CROP)
        harvestYield = self.factionData \
            .getCropHarvestYield(CropName.EGGPLANT_CROP)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(eggplantAmount / productionPerTile)

    def getBirchLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of birch trees needed to produce a given
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
        Calculate the number of pine trees needed to produce a given
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

    def getMangroveLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of mangrove trees needed to produce a given
        amount of logs per day.

        :param logAmount: Daily amount of logs needed.
        :type logAmount: float

        :return: Number of mangrove tree tiles needed.
        :rtype: int

        :raises ValueError: If log amount is negative.
        """
        if logAmount < 0:
            raise ValueError("Log amount cannot be negative.")

        growthTime = self.factionData.getTreeGrowthTime(TreeName.MANGROVE_TREE)
        logOutput = self.factionData.getTreeLogOutput(TreeName.MANGROVE_TREE)
        productionPerTile = logOutput / growthTime
        return math.ceil(logAmount / productionPerTile)

    def getOakLogTilesNeeded(self, logAmount: float) -> int:
        """
        Calculate the number of oak trees needed to produce a given
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

    def getMangroveFruitTilesNeeded(self, mangroveFruitAmount: float) -> int:
        """
        Calculate the number of mangrove tree tiles needed to produce a given
        amount of mangrove fruits per day.

        :param mangroveFruitAmount: Daily amount of mangrove fruits needed.
        :type mangroveFruitAmount: float

        :return: Number of mangrove tree tiles needed.
        :rtype: int

        :raises ValueError: If mangrove fruit amount is negative.
        """
        if mangroveFruitAmount < 0:
            raise ValueError("Mangrove fruit amount cannot be negative.")

        harvestTime = self.factionData \
            .getTreeHarvestTime(TreeName.MANGROVE_TREE)
        harvestYield = self.factionData \
            .getTreeHarvestYield(TreeName.MANGROVE_TREE)
        productionPerTile = harvestYield / harvestTime
        return math.ceil(mangroveFruitAmount / productionPerTile)

    # Food Processing Methods - Coffee Brewery
    def getCoffeeBreweriesNeededForCoffee(self, coffeeAmount: float) -> int:
        """
        Calculate the number of coffee breweries needed to produce a given
        amount of coffee per day.

        :param coffeeAmount: Daily amount of coffee needed.
        :type coffeeAmount: float

        :return: Number of coffee breweries needed.
        :rtype: int

        :raises ValueError: If coffee amount is negative.
        """
        if coffeeAmount < 0:
            raise ValueError("Coffee amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.COFFEE_BREWERY,    # noqa: E501
                                          FoodRecipeName.COFFEE)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(
                FoodProcessingBuildingName.COFFEE_BREWERY, recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.COFFEE_BREWERY,     # noqa: E501
                                             recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerBrewery = (outputQuantity / productionTime) * 24

        return math.ceil(coffeeAmount / productionPerBrewery)

    def getCoffeeBeansNeededForCoffeeBreweries(
            self, coffeeBreweriesCount: int) -> int:
        """
        Calculate the number of coffee beans needed per day to keep a given
        number of coffee breweries running.

        :param coffeeBreweriesCount: Number of coffee breweries.
        :type coffeeBreweriesCount: int

        :return: Daily amount of coffee beans needed.
        :rtype: int

        :raises ValueError: If coffee breweries count is negative.
        """
        if coffeeBreweriesCount < 0:
            raise ValueError("Coffee breweries count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.COFFEE_BREWERY,    # noqa: E501
                                          FoodRecipeName.COFFEE)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.COFFEE_BREWERY,     # noqa: E501
                                             recipeIndex)
        coffeeBeansInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.COFFEE_BREWERY,  # noqa: E501
                                            FoodRecipeName.COFFEE,
                                            HarvestName.COFFEE_BEANS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        coffeeBeansPerBreweryPerDay = coffeeBeansInput * cyclesPerDay

        return math.ceil(coffeeBreweriesCount * coffeeBeansPerBreweryPerDay)

    # Goods Production Methods - Industrial Lumber Mill
    def getIndustrialLumberMillsNeededForPlanks(
            self, planksAmount: float) -> int:
        """
        Calculate the number of industrial lumber mills needed to produce
        a given amount of planks per day.

        :param planksAmount: Daily amount of planks needed.
        :type planksAmount: float

        :return: Number of industrial lumber mills needed.
        :rtype: int

        :raises ValueError: If planks amount is negative.
        """
        if planksAmount < 0:
            raise ValueError("Planks amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.INDUSTRIAL_LUMBER_MILL,
                                 GoodsRecipeName.PLANKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.INDUSTRIAL_LUMBER_MILL,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.INDUSTRIAL_LUMBER_MILL,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerMill = (outputQuantity / productionTime) * 24

        return math.ceil(planksAmount / productionPerMill)

    def getLogsNeededForIndustrialLumberMills(
            self, industrialLumberMillsCount: int) -> float:
        """
        Calculate the number of logs needed per day to keep a given number
        of industrial lumber mills running.

        :param industrialLumberMillsCount: Number of industrial lumber mills.
        :type industrialLumberMillsCount: int

        :return: Daily amount of logs needed.
        :rtype: float

        :raises ValueError: If industrial lumber mills count is negative.
        """
        if industrialLumberMillsCount < 0:
            raise ValueError(
                "Industrial lumber mills count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.INDUSTRIAL_LUMBER_MILL,
                                 GoodsRecipeName.PLANKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.INDUSTRIAL_LUMBER_MILL,
                                    recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.INDUSTRIAL_LUMBER_MILL,
                                   GoodsRecipeName.PLANKS,
                                   HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerMillPerDay = logsInput * cyclesPerDay

        return industrialLumberMillsCount * logsPerMillPerDay

    # Efficient Mine Methods
    def getEfficientMinesNeededForScrapMetal(
            self, scrapMetalAmount: float) -> int:
        """
        Calculate the number of efficient mines needed to produce a given
        amount of scrap metal per day (without extract).

        :param scrapMetalAmount: Daily amount of scrap metal needed.
        :type scrapMetalAmount: float

        :return: Number of efficient mines needed.
        :rtype: int

        :raises ValueError: If scrap metal amount is negative.
        """
        if scrapMetalAmount < 0:
            raise ValueError("Scrap metal amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.EFFICIENT_MINE,
                                 GoodsRecipeName.SCRAP_METAL)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.EFFICIENT_MINE,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.EFFICIENT_MINE,
                                    recipeIndex)
        # Production time is in hours, calculate daily production
        productionPerMine = (outputQuantity / productionTime) * 24

        return math.ceil(scrapMetalAmount / productionPerMine)

    def getTreatedPlanksNeededForEfficientMines(
            self, efficientMinesCount: int) -> int:
        """
        Calculate the number of treated planks needed per day to keep a given
        number of efficient mines running.

        :param efficientMinesCount: Number of efficient mines.
        :type efficientMinesCount: int

        :return: Daily amount of treated planks needed.
        :rtype: int

        :raises ValueError: If efficient mines count is negative.
        """
        if efficientMinesCount < 0:
            raise ValueError("Efficient mines count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.EFFICIENT_MINE,
                                 GoodsRecipeName.SCRAP_METAL)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.EFFICIENT_MINE,
                                    recipeIndex)
        treatedPlanksInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.EFFICIENT_MINE,
                                   GoodsRecipeName.SCRAP_METAL,
                                   GoodsRecipeName.TREATED_PLANKS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        treatedPlanksPerMinePerDay = treatedPlanksInput * cyclesPerDay

        return math.ceil(efficientMinesCount * treatedPlanksPerMinePerDay)
