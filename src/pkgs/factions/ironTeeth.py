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
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.COFFEE_BREWERY,        # noqa: E501
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

    def getCoffeeBeansNeededForCoffeeProduction(self,
                                                coffeeBreweriesCount: int
                                                ) -> int:
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
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.COFFEE_BREWERY,        # noqa: E501
                                          FoodRecipeName.COFFEE)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.COFFEE_BREWERY,     # noqa: E501
                                             recipeIndex)
        coffeeBeansInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.COFFEE_BREWERY,      # noqa: E501
                                            FoodRecipeName.COFFEE,
                                            HarvestName.COFFEE_BEANS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        coffeeBeansPerBreweryPerDay = coffeeBeansInput * cyclesPerDay

        return math.ceil(coffeeBreweriesCount * coffeeBeansPerBreweryPerDay)

    def getWaterNeededForCoffeeProduction(
            self, coffeeBreweriesCount: int) -> int:
        """
        Calculate the amount of water needed per day to keep a given number
        of coffee breweries running.

        :param coffeeBreweriesCount: Number of coffee breweries.
        :type coffeeBreweriesCount: int

        :return: Daily amount of water needed.
        :rtype: int

        :raises ValueError: If coffee breweries count is negative.
        """
        if coffeeBreweriesCount < 0:
            raise ValueError("Coffee breweries count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.COFFEE_BREWERY,        # noqa: E501
                                          FoodRecipeName.COFFEE)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.COFFEE_BREWERY,     # noqa: E501
                                             recipeIndex)
        waterInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.COFFEE_BREWERY,      # noqa: E501
                                            FoodRecipeName.COFFEE,
                                            HarvestName.WATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        waterPerBreweryPerDay = waterInput * cyclesPerDay

        return math.ceil(coffeeBreweriesCount * waterPerBreweryPerDay)

    def getLogsNeededForCoffeeProduction(self,
                                         coffeeBreweriesCount: int) -> int:
        """
        Calculate the number of logs needed per day to keep a given number
        of coffee breweries running.

        :param coffeeBreweriesCount: Number of coffee breweries.
        :type coffeeBreweriesCount: int

        :return: Daily amount of logs needed.
        :rtype: int

        :raises ValueError: If coffee breweries count is negative.
        """
        if coffeeBreweriesCount < 0:
            raise ValueError("Coffee breweries count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.COFFEE_BREWERY,        # noqa: E501
                                          FoodRecipeName.COFFEE)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.COFFEE_BREWERY,     # noqa: E501
                                             recipeIndex)
        logsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.COFFEE_BREWERY,      # noqa: E501
                                            FoodRecipeName.COFFEE,
                                            HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerBreweryPerDay = logsInput * cyclesPerDay

        return math.ceil(coffeeBreweriesCount * logsPerBreweryPerDay)

    # Food Processing Methods - Fermenter
    def getFermentersNeededForFermentedCassava(self,
                                               fermentedCassavaAmount: float
                                               ) -> int:
        """
        Calculate the number of fermenters needed to produce a given amount
        of fermented cassava per day.

        :param fermentedCassavaAmount: Amount of fermented cassava needed
                                        per day.
        :type fermentedCassavaAmount: float

        :return: Number of fermenters needed.
        :rtype: int

        :raises ValueError: If fermented cassava amount is negative.
        """
        if fermentedCassavaAmount < 0:
            raise ValueError(
                "Fermented cassava amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FERMENTER,
                                          FoodRecipeName.FERMENTED_CASSAVA)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.FERMENTER)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(fermentedCassavaAmount / outputPerBuilding)

    def getCassavasNeededForFermentedCassavaProduction(self,
                                                       fermentersCount: int
                                                       ) -> int:
        """
        Calculate the number of cassavas needed per day to keep a given
        number of fermenters running for fermented cassava production.

        :param fermentersCount: Number of fermenters.
        :type fermentersCount: int

        :return: Daily amount of cassavas needed.
        :rtype: int

        :raises ValueError: If fermenters count is negative.
        """
        if fermentersCount < 0:
            raise ValueError("Fermenters count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FERMENTER,
                                          FoodRecipeName.FERMENTED_CASSAVA)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        cassavasInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FERMENTER,   # noqa: E501
                                            FoodRecipeName.FERMENTED_CASSAVA,
                                            HarvestName.CASSAVAS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        cassavasPerFermenterPerDay = cassavasInput * cyclesPerDay

        return math.ceil(fermentersCount * cassavasPerFermenterPerDay)

    def getFermentersNeededForFermentedSoybean(self,
                                               fermentedSoybeanAmount: float
                                               ) -> int:
        """
        Calculate the number of fermenters needed to produce a given amount
        of fermented soybean per day.

        :param fermentedSoybeanAmount: Amount of fermented soybean needed
                                        per day.
        :type fermentedSoybeanAmount: float

        :return: Number of fermenters needed.
        :rtype: int

        :raises ValueError: If fermented soybean amount is negative.
        """
        if fermentedSoybeanAmount < 0:
            raise ValueError(
                "Fermented soybean amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FERMENTER,
                                          FoodRecipeName.FERMENTED_SOYBEAN)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.FERMENTER)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(fermentedSoybeanAmount / outputPerBuilding)

    def getSoybeansNeededForFermentedSoybeanProduction(self,
                                                       fermentersCount: int
                                                       ) -> int:
        """
        Calculate the number of soybeans needed per day to keep a given
        number of fermenters running for fermented soybean production.

        :param fermentersCount: Number of fermenters.
        :type fermentersCount: int

        :return: Daily amount of soybeans needed.
        :rtype: int

        :raises ValueError: If fermenters count is negative.
        """
        if fermentersCount < 0:
            raise ValueError("Fermenters count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FERMENTER,
                                          FoodRecipeName.FERMENTED_SOYBEAN)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        soybeansInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FERMENTER,   # noqa: E501
                                            FoodRecipeName.FERMENTED_SOYBEAN,
                                            HarvestName.SOYBEANS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        soybeansPerFermenterPerDay = soybeansInput * cyclesPerDay

        return math.ceil(fermentersCount * soybeansPerFermenterPerDay)

    def getCanolaOilNeededForFermentedSoybeanProduction(self,
                                                        fermentersCount: int
                                                        ) -> int:
        """
        Calculate the amount of canola oil needed per day to keep a given
        number of fermenters running for fermented soybean production.

        :param fermentersCount: Number of fermenters.
        :type fermentersCount: int

        :return: Daily amount of canola oil needed.
        :rtype: int

        :raises ValueError: If fermenters count is negative.
        """
        if fermentersCount < 0:
            raise ValueError("Fermenters count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FERMENTER,
                                          FoodRecipeName.FERMENTED_SOYBEAN)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        canolaOilInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FERMENTER,   # noqa: E501
                                            FoodRecipeName.FERMENTED_SOYBEAN,
                                            FoodRecipeName.CANOLA_OIL)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        canolaOilPerFermenterPerDay = canolaOilInput * cyclesPerDay

        return math.ceil(fermentersCount * canolaOilPerFermenterPerDay)

    def getFermentersNeededForFermentedMushroom(self,
                                                fermentedMushroomAmount: float
                                                ) -> int:
        """
        Calculate the number of fermenters needed to produce a given amount
        of fermented mushroom per day.

        :param fermentedMushroomAmount: Amount of fermented mushroom needed
                                         per day.
        :type fermentedMushroomAmount: float

        :return: Number of fermenters needed.
        :rtype: int

        :raises ValueError: If fermented mushroom amount is negative.
        """
        if fermentedMushroomAmount < 0:
            raise ValueError(
                "Fermented mushroom amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FERMENTER,
                                          FoodRecipeName.FERMENTED_MUSHROOM)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.FERMENTER)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(fermentedMushroomAmount / outputPerBuilding)

    def getMushroomsNeededForFermentedMushroomProduction(self,
                                                         fermentersCount: int
                                                         ) -> int:
        """
        Calculate the number of mushrooms needed per day to keep a given
        number of fermenters running for fermented mushroom production.

        :param fermentersCount: Number of fermenters.
        :type fermentersCount: int

        :return: Daily amount of mushrooms needed.
        :rtype: int

        :raises ValueError: If fermenters count is negative.
        """
        if fermentersCount < 0:
            raise ValueError("Fermenters count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FERMENTER,
                                          FoodRecipeName.FERMENTED_MUSHROOM)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FERMENTER,  # noqa: E501
                                             recipeIndex)
        mushroomsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FERMENTER,   # noqa: E501
                                            FoodRecipeName.FERMENTED_MUSHROOM,
                                            FoodRecipeName.MUSHROOMS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        mushroomsPerFermenterPerDay = mushroomsInput * cyclesPerDay

        return math.ceil(fermentersCount * mushroomsPerFermenterPerDay)

    # Food Processing Methods - Food Factory
    def getFoodFactoriesNeededForCornRations(self,
                                             cornRationsAmount: float) -> int:
        """
        Calculate the number of food factories needed to produce a given
        amount of corn rations per day.

        :param cornRationsAmount: Amount of corn rations needed per day.
        :type cornRationsAmount: float

        :return: Number of food factories needed.
        :rtype: int

        :raises ValueError: If corn rations amount is negative.
        """
        if cornRationsAmount < 0:
            raise ValueError("Corn rations amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.CORN_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.FOOD_FACTORY)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(cornRationsAmount / outputPerBuilding)

    def getCornNeededForCornRationsProduction(self,
                                              foodFactoriesCount: int) -> int:
        """
        Calculate the amount of corn needed per day to keep a given number
        of food factories running for corn rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of corn needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.CORN_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        cornInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.CORN_RATIONS,
                                            HarvestName.CORN)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        cornPerFactoryPerDay = cornInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * cornPerFactoryPerDay)

    def getLogsNeededForCornRationsProduction(self,
                                              foodFactoriesCount: int) -> int:
        """
        Calculate the number of logs needed per day to keep a given number
        of food factories running for corn rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of logs needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.CORN_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        logsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.CORN_RATIONS,
                                            HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerFactoryPerDay = logsInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * logsPerFactoryPerDay)

    def getFoodFactoriesNeededForEggplantRations(self,
                                                 eggplantRationsAmount: float
                                                 ) -> int:
        """
        Calculate the number of food factories needed to produce a given
        amount of eggplant rations per day.

        :param eggplantRationsAmount: Amount of eggplant rations needed
                                       per day.
        :type eggplantRationsAmount: float

        :return: Number of food factories needed.
        :rtype: int

        :raises ValueError: If eggplant rations amount is negative.
        """
        if eggplantRationsAmount < 0:
            raise ValueError(
                "Eggplant rations amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.EGGPLANT_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.FOOD_FACTORY)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(eggplantRationsAmount / outputPerBuilding)

    def getEggplantsNeededForEggplantRationsProduction(self,
                                                       foodFactoriesCount: int
                                                       ) -> int:
        """
        Calculate the amount of eggplants needed per day to keep a given
        number of food factories running for eggplant rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of eggplants needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.EGGPLANT_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        eggplantsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.EGGPLANT_RATIONS,
                                            HarvestName.EGGPLANTS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        eggplantsPerFactoryPerDay = eggplantsInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * eggplantsPerFactoryPerDay)

    def getCanolaOilNeededForEggplantRationsProduction(self,
                                                       foodFactoriesCount: int
                                                       ) -> int:
        """
        Calculate the amount of canola oil needed per day to keep a given
        number of food factories running for eggplant rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of canola oil needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.EGGPLANT_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        canolaOilInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.EGGPLANT_RATIONS,
                                            FoodRecipeName.CANOLA_OIL)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        canolaOilPerFactoryPerDay = canolaOilInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * canolaOilPerFactoryPerDay)

    def getLogsNeededForEggplantRationsProduction(self,
                                                  foodFactoriesCount: int
                                                  ) -> int:
        """
        Calculate the number of logs needed per day to keep a given number
        of food factories running for eggplant rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of logs needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.EGGPLANT_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        logsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.EGGPLANT_RATIONS,
                                            HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerFactoryPerDay = logsInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * logsPerFactoryPerDay)

    def getFoodFactoriesNeededForAlgaeRations(self,
                                              algaeRationsAmount: float
                                              ) -> int:
        """
        Calculate the number of food factories needed to produce a given
        amount of algae rations per day.

        :param algaeRationsAmount: Amount of algae rations needed per day.
        :type algaeRationsAmount: float

        :return: Number of food factories needed.
        :rtype: int

        :raises ValueError: If algae rations amount is negative.
        """
        if algaeRationsAmount < 0:
            raise ValueError("Algae rations amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.ALGAE_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.FOOD_FACTORY)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(algaeRationsAmount / outputPerBuilding)

    def getAlgaeNeededForAlgaeRationsProduction(self,
                                                foodFactoriesCount: int
                                                ) -> int:
        """
        Calculate the amount of algae needed per day to keep a given number
        of food factories running for algae rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of algae needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.ALGAE_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        algaeInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.ALGAE_RATIONS,
                                            FoodRecipeName.ALGAE)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        algaePerFactoryPerDay = algaeInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * algaePerFactoryPerDay)

    def getCanolaOilNeededForAlgaeRationsProduction(self,
                                                    foodFactoriesCount: int
                                                    ) -> int:
        """
        Calculate the amount of canola oil needed per day to keep a given
        number of food factories running for algae rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of canola oil needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.ALGAE_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        canolaOilInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.ALGAE_RATIONS,
                                            FoodRecipeName.CANOLA_OIL)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        canolaOilPerFactoryPerDay = canolaOilInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * canolaOilPerFactoryPerDay)

    def getLogsNeededForAlgaeRationsProduction(self,
                                               foodFactoriesCount: int) -> int:
        """
        Calculate the number of logs needed per day to keep a given number
        of food factories running for algae rations production.

        :param foodFactoriesCount: Number of food factories.
        :type foodFactoriesCount: int

        :return: Daily amount of logs needed.
        :rtype: int

        :raises ValueError: If food factories count is negative.
        """
        if foodFactoriesCount < 0:
            raise ValueError("Food factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.FOOD_FACTORY,      # noqa: E501
                                          FoodRecipeName.ALGAE_RATIONS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.FOOD_FACTORY,   # noqa: E501
                                             recipeIndex)
        logsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.FOOD_FACTORY,    # noqa: E501
                                            FoodRecipeName.ALGAE_RATIONS,
                                            HarvestName.LOGS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        logsPerFactoryPerDay = logsInput * cyclesPerDay

        return math.ceil(foodFactoriesCount * logsPerFactoryPerDay)

    # Food Processing Methods - Hydroponic Garden
    def getHydroponicGardensNeededForMushrooms(self,
                                               mushroomsAmount: float) -> int:
        """
        Calculate the number of hydroponic gardens needed to produce a given
        amount of mushrooms per day.

        :param mushroomsAmount: Amount of mushrooms needed per day.
        :type mushroomsAmount: float

        :return: Number of hydroponic gardens needed.
        :rtype: int

        :raises ValueError: If mushrooms amount is negative.
        """
        if mushroomsAmount < 0:
            raise ValueError("Mushrooms amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.HYDROPONIC_GARDEN,     # noqa: E501
                                          FoodRecipeName.MUSHROOMS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.HYDROPONIC_GARDEN,  # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.HYDROPONIC_GARDEN,  # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.HYDROPONIC_GARDEN)     # noqa: E501

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(mushroomsAmount / outputPerBuilding)

    def getWaterNeededForMushroomsProduction(self,
                                             hydroponicGardensCount: int
                                             ) -> int:
        """
        Calculate the amount of water needed per day to keep a given number
        of hydroponic gardens running for mushrooms production.

        :param hydroponicGardensCount: Number of hydroponic gardens.
        :type hydroponicGardensCount: int

        :return: Daily amount of water needed.
        :rtype: int

        :raises ValueError: If hydroponic gardens count is negative.
        """
        if hydroponicGardensCount < 0:
            raise ValueError(
                "Hydroponic gardens count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.HYDROPONIC_GARDEN,     # noqa: E501
                                          FoodRecipeName.MUSHROOMS)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.HYDROPONIC_GARDEN,  # noqa: E501
                                             recipeIndex)
        waterInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.HYDROPONIC_GARDEN,   # noqa: E501
                                            FoodRecipeName.MUSHROOMS,
                                            HarvestName.WATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        waterPerGardenPerDay = waterInput * cyclesPerDay

        return math.ceil(hydroponicGardensCount * waterPerGardenPerDay)

    def getHydroponicGardensNeededForAlgae(self, algaeAmount: float) -> int:
        """
        Calculate the number of hydroponic gardens needed to produce a given
        amount of algae per day.

        :param algaeAmount: Amount of algae needed per day.
        :type algaeAmount: float

        :return: Number of hydroponic gardens needed.
        :rtype: int

        :raises ValueError: If algae amount is negative.
        """
        if algaeAmount < 0:
            raise ValueError("Algae amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.HYDROPONIC_GARDEN,     # noqa: E501
                                          FoodRecipeName.ALGAE)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.HYDROPONIC_GARDEN,  # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.HYDROPONIC_GARDEN,  # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.HYDROPONIC_GARDEN)     # noqa: E501

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(algaeAmount / outputPerBuilding)

    def getWaterNeededForAlgaeProduction(self,
                                         hydroponicGardensCount: int) -> int:
        """
        Calculate the amount of water needed per day to keep a given number
        of hydroponic gardens running for algae production.

        :param hydroponicGardensCount: Number of hydroponic gardens.
        :type hydroponicGardensCount: int

        :return: Daily amount of water needed.
        :rtype: int

        :raises ValueError: If hydroponic gardens count is negative.
        """
        if hydroponicGardensCount < 0:
            raise ValueError(
                "Hydroponic gardens count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.HYDROPONIC_GARDEN,     # noqa: E501
                                          FoodRecipeName.ALGAE)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.HYDROPONIC_GARDEN,  # noqa: E501
                                             recipeIndex)
        waterInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.HYDROPONIC_GARDEN,   # noqa: E501
                                            FoodRecipeName.ALGAE,
                                            HarvestName.WATER)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        waterPerGardenPerDay = waterInput * cyclesPerDay

        return math.ceil(hydroponicGardensCount * waterPerGardenPerDay)

    # Food Processing Methods - Oil Press
    def getOilPressesNeededForCanolaOil(self, canolaOilAmount: float) -> int:
        """
        Calculate the number of oil presses needed to produce a given amount
        of canola oil per day.

        :param canolaOilAmount: Amount of canola oil needed per day.
        :type canolaOilAmount: float

        :return: Number of oil presses needed.
        :rtype: int

        :raises ValueError: If canola oil amount is negative.
        """
        if canolaOilAmount < 0:
            raise ValueError("Canola oil amount cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.OIL_PRESS,
                                          FoodRecipeName.CANOLA_OIL)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.OIL_PRESS,      # noqa: E501
                                             recipeIndex)
        outputQuantity = self.factionData \
            .getFoodProcessingOutputQuantity(FoodProcessingBuildingName.OIL_PRESS,      # noqa: E501
                                             recipeIndex)
        workersPerBuilding = self.factionData \
            .getFoodProcessingWorkers(FoodProcessingBuildingName.OIL_PRESS)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(canolaOilAmount / outputPerBuilding)

    def getCanolaSeedsNeededForCanolaOilProduction(self,
                                                   oilPressesCount: int
                                                   ) -> int:
        """
        Calculate the number of canola seeds needed per day to keep a given
        number of oil presses running.

        :param oilPressesCount: Number of oil presses.
        :type oilPressesCount: int

        :return: Daily amount of canola seeds needed.
        :rtype: int

        :raises ValueError: If oil presses count is negative.
        """
        if oilPressesCount < 0:
            raise ValueError("Oil presses count cannot be negative.")

        recipeIndex = self.factionData \
            .getFoodProcessingRecipeIndex(FoodProcessingBuildingName.OIL_PRESS,
                                          FoodRecipeName.CANOLA_OIL)
        productionTime = self.factionData \
            .getFoodProcessingProductionTime(FoodProcessingBuildingName.OIL_PRESS,      # noqa: E501
                                             recipeIndex)
        canolaSeedsInput = self.factionData \
            .getFoodProcessingInputQuantity(FoodProcessingBuildingName.OIL_PRESS,       # noqa: E501
                                            FoodRecipeName.CANOLA_OIL,
                                            HarvestName.CANOLA_SEEDS)

        # Production time is in hours, calculate daily consumption
        cyclesPerDay = 24 / productionTime
        canolaSeedsPerPressPerDay = canolaSeedsInput * cyclesPerDay

        return math.ceil(oilPressesCount * canolaSeedsPerPressPerDay)

    # Goods Production Methods - Industrial Lumber Mill
    def getIndustrialLumberMillsNeededForPlanks(self,
                                                planksAmount: float) -> int:
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

    def getLogsNeededForPlanksProduction(self,
                                         industrialLumberMillsCount: int
                                         ) -> float:
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

    # Goods Production Methods - Gear Workshop
    def getGearWorkshopsNeededForGears(self, gearsAmount: float) -> int:
        """
        Calculate the number of gear workshops needed to produce a given
        amount of gears per day.

        :param gearsAmount: Amount of gears needed per day.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.GEAR_WORKSHOP)

        # Production time is in hours, calculate daily production
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(gearsAmount / outputPerBuilding)

    def getPlanksNeededForGearsProduction(self,
                                          gearWorkshopsCount: int) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of gear workshops running.

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
        planksPerWorkshopPerDay = planksInput * cyclesPerDay

        return math.ceil(gearWorkshopsCount * planksPerWorkshopPerDay)

    # Wood Workshop Methods
    def getWoodWorkshopsNeededForTreatedPlanks(
            self, treatedPlanksAmount: float) -> int:
        """
        Calculate the number of wood workshops needed to produce a given
        amount of treated planks per day.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.WOOD_WORKSHOP)

        # Example: productionTime=3.0, outputQuantity=1, workers=2
        # Cycles per day = 24 / 3.0 = 8 cycles/day
        # Output per building = 1 * 8 * 2 = 16 treated planks/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(treatedPlanksAmount / outputPerBuilding)

    def getPineResinNeededForTreatedPlanksProduction(
            self, woodWorkshopsCount: int) -> int:
        """
        Calculate the number of pine resin needed per day to keep a given
        number of wood workshops running.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.WOOD_WORKSHOP)

        # Example: productionTime=3.0, pineResinInput=1, workers=2
        # Cycles per day = 24 / 3.0 = 8 cycles/day
        # Pine resin per workshop per day = 1 * 8 * 2 = 16
        cyclesPerDay = 24 / productionTime
        pineResinPerWorkshopPerDay = pineResinInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(woodWorkshopsCount * pineResinPerWorkshopPerDay)

    def getPlanksNeededForTreatedPlanksProduction(
            self, woodWorkshopsCount: int) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of wood workshops running.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.WOOD_WORKSHOP)

        # Example: productionTime=3.0, planksInput=1, workers=2
        # Cycles per day = 24 / 3.0 = 8 cycles/day
        # Planks per workshop per day = 1 * 8 * 2 = 16
        cyclesPerDay = 24 / productionTime
        planksPerWorkshopPerDay = planksInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(woodWorkshopsCount * planksPerWorkshopPerDay)

    # Smelter Methods
    def getSmeltersNeededForMetalBlocks(
            self, metalBlocksAmount: float) -> int:
        """
        Calculate the number of smelters needed to produce a given amount of
        metal blocks per day.
        """
        if metalBlocksAmount < 0:
            raise ValueError("Metal blocks amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.SMELTER,
                                 GoodsRecipeName.METAL_BLOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.SMELTER,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.SMELTER,
                                    recipeIndex)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.SMELTER)

        # Example: productionTime=2.0, outputQuantity=1, workers=1
        # Cycles per day = 24 / 2.0 = 12 cycles/day
        # Output per building = 1 * 12 * 1 = 12 metal blocks/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(metalBlocksAmount / outputPerBuilding)

    def getScrapMetalNeededForMetalBlocksProduction(
            self, smeltersCount: int) -> int:
        """
        Calculate the number of scrap metal needed per day to keep a given
        number of smelters running.
        """
        if smeltersCount < 0:
            raise ValueError("Smelters count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.SMELTER,
                                 GoodsRecipeName.METAL_BLOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.SMELTER,
                                    recipeIndex)
        scrapMetalInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.SMELTER,
                                   GoodsRecipeName.METAL_BLOCKS,
                                   GoodsRecipeName.SCRAP_METAL)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.SMELTER)

        # Example: productionTime=2.0, scrapMetalInput=1, workers=1
        # Cycles per day = 24 / 2.0 = 12 cycles/day
        # Scrap metal per smelter per day = 1 * 12 * 1 = 12
        cyclesPerDay = 24 / productionTime
        scrapMetalPerSmelterPerDay = scrapMetalInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(smeltersCount * scrapMetalPerSmelterPerDay)

    def getLogsNeededForMetalBlocksProduction(
            self, smeltersCount: int) -> int:
        """
        Calculate the number of logs needed per day to keep a given number of
        smelters running.
        """
        if smeltersCount < 0:
            raise ValueError("Smelters count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.SMELTER,
                                 GoodsRecipeName.METAL_BLOCKS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.SMELTER,
                                    recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.SMELTER,
                                   GoodsRecipeName.METAL_BLOCKS,
                                   HarvestName.LOGS)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.SMELTER)

        # Example: productionTime=2.0, logsInput=0.2, workers=1
        # Cycles per day = 24 / 2.0 = 12 cycles/day
        # Logs per smelter per day = 0.2 * 12 * 1 = 2.4
        cyclesPerDay = 24 / productionTime
        logsPerSmelterPerDay = logsInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(smeltersCount * logsPerSmelterPerDay)

    # Efficient Mine Methods
    def getEfficientMinesNeededForScrapMetal(self,
                                             scrapMetalAmount: float) -> int:
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

    def getTreatedPlanksNeededForScrapMetalProduction(self,
                                                      efficientMinesCount: int
                                                      ) -> int:
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

    # Grease Factory Methods
    def getGreaseFactoriesNeededForGrease(
            self, greaseAmount: float) -> int:
        """
        Calculate the number of grease factories needed to produce a given
        amount of grease per day.
        """
        if greaseAmount < 0:
            raise ValueError("Grease amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.GREASE_FACTORY,
                                 GoodsRecipeName.GREASE)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.GREASE_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.GREASE_FACTORY,
                                    recipeIndex)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.GREASE_FACTORY)

        # Example: productionTime=2.0, outputQuantity=2, workers=2
        # Cycles per day = 24 / 2.0 = 12 cycles/day
        # Output per building = 2 * 12 * 2 = 48 grease/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(greaseAmount / outputPerBuilding)

    def getExtractNeededForGreaseProduction(
            self, greaseFactoriesCount: int) -> int:
        """
        Calculate the number of extract needed per day to keep a given number
        of grease factories running.
        """
        if greaseFactoriesCount < 0:
            raise ValueError("Grease factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.GREASE_FACTORY,
                                 GoodsRecipeName.GREASE)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.GREASE_FACTORY,
                                    recipeIndex)
        extractInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.GREASE_FACTORY,
                                   GoodsRecipeName.GREASE,
                                   GoodsRecipeName.EXTRACT)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.GREASE_FACTORY)

        # Example: productionTime=2.0, extractInput=1, workers=2
        # Cycles per day = 24 / 2.0 = 12 cycles/day
        # Extract per factory per day = 1 * 12 * 2 = 24
        cyclesPerDay = 24 / productionTime
        extractPerFactoryPerDay = extractInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(greaseFactoriesCount * extractPerFactoryPerDay)

    def getCanolaOilNeededForGreaseProduction(
            self, greaseFactoriesCount: int) -> int:
        """
        Calculate the number of canola oil needed per day to keep a given
        number of grease factories running.
        """
        if greaseFactoriesCount < 0:
            raise ValueError("Grease factories count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.GREASE_FACTORY,
                                 GoodsRecipeName.GREASE)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.GREASE_FACTORY,
                                    recipeIndex)
        canolaOilInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.GREASE_FACTORY,
                                   GoodsRecipeName.GREASE,
                                   FoodRecipeName.CANOLA_OIL)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.GREASE_FACTORY)

        # Example: productionTime=2.0, canolaOilInput=1, workers=2
        # Cycles per day = 24 / 2.0 = 12 cycles/day
        # Canola oil per factory per day = 1 * 12 * 2 = 24
        cyclesPerDay = 24 / productionTime
        canolaOilPerFactoryPerDay = canolaOilInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(greaseFactoriesCount * canolaOilPerFactoryPerDay)

    # Bot Part Factory Methods
    def getBotPartFactoriesNeededForBotChassis(
            self, botChassisAmount: float) -> int:
        """
        Calculate the number of bot part factories needed to produce a given
        amount of bot chassis per day.
        """
        if botChassisAmount < 0:
            raise ValueError("Bot chassis amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_CHASSIS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, outputQuantity=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333... cycles/day
        # Output per building = 1 * 1.333... * 1 = 1.333... bot chassis/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botChassisAmount / outputPerBuilding)

    def getPlanksNeededForBotChassisProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of bot part factories running for bot chassis production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, planksInput=5, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Planks per factory per day = 5 * 1.333... * 1 = 6.666...
        cyclesPerDay = 24 / productionTime
        planksPerFactoryPerDay = planksInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * planksPerFactoryPerDay)

    def getMetalBlocksNeededForBotChassisProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of metal blocks needed per day to keep a given
        number of bot part factories running for bot chassis production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, metalBlocksInput=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Metal blocks per factory per day = 1 * 1.333... * 1 = 1.333...
        cyclesPerDay = 24 / productionTime
        metalBlocksPerFactoryPerDay = metalBlocksInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * metalBlocksPerFactoryPerDay)

    def getBiofuelNeededForBotChassisProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of biofuel needed per day to keep a given number
        of bot part factories running for bot chassis production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, biofuelInput=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Biofuel per factory per day = 1 * 1.333... * 1 = 1.333...
        cyclesPerDay = 24 / productionTime
        biofuelPerFactoryPerDay = biofuelInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * biofuelPerFactoryPerDay)

    def getBotPartFactoriesNeededForBotHeads(
            self, botHeadsAmount: float) -> int:
        """
        Calculate the number of bot part factories needed to produce a given
        amount of bot heads per day.
        """
        if botHeadsAmount < 0:
            raise ValueError("Bot heads amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_HEADS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, outputQuantity=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333... cycles/day
        # Output per building = 1 * 1.333... * 1 = 1.333... bot heads/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botHeadsAmount / outputPerBuilding)

    def getGearsNeededForBotHeadsProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of gears needed per day to keep a given number
        of bot part factories running for bot heads production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, gearsInput=3, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Gears per factory per day = 3 * 1.333... * 1 = 4
        cyclesPerDay = 24 / productionTime
        gearsPerFactoryPerDay = gearsInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * gearsPerFactoryPerDay)

    def getMetalBlocksNeededForBotHeadsProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of metal blocks needed per day to keep a given
        number of bot part factories running for bot heads production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, metalBlocksInput=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Metal blocks per factory per day = 1 * 1.333... * 1 = 1.333...
        cyclesPerDay = 24 / productionTime
        metalBlocksPerFactoryPerDay = metalBlocksInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * metalBlocksPerFactoryPerDay)

    def getPlanksNeededForBotHeadsProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of bot part factories running for bot heads production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, planksInput=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Planks per factory per day = 1 * 1.333... * 1 = 1.333...
        cyclesPerDay = 24 / productionTime
        planksPerFactoryPerDay = planksInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * planksPerFactoryPerDay)

    def getBotPartFactoriesNeededForBotLimbs(
            self, botLimbsAmount: float) -> int:
        """
        Calculate the number of bot part factories needed to produce a given
        amount of bot limbs per day.
        """
        if botLimbsAmount < 0:
            raise ValueError("Bot limbs amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.BOT_PART_FACTORY,
                                 GoodsRecipeName.BOT_LIMBS)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.BOT_PART_FACTORY,
                                    recipeIndex)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, outputQuantity=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333... cycles/day
        # Output per building = 1 * 1.333... * 1 = 1.333... bot limbs/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botLimbsAmount / outputPerBuilding)

    def getGearsNeededForBotLimbsProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of gears needed per day to keep a given number
        of bot part factories running for bot limbs production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, gearsInput=3, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Gears per factory per day = 3 * 1.333... * 1 = 4
        cyclesPerDay = 24 / productionTime
        gearsPerFactoryPerDay = gearsInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * gearsPerFactoryPerDay)

    def getPlanksNeededForBotLimbsProduction(
            self, botPartFactoriesCount: int) -> int:
        """
        Calculate the number of planks needed per day to keep a given number
        of bot part factories running for bot limbs production.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_PART_FACTORY)

        # Example: productionTime=18.0, planksInput=1, workers=1
        # Cycles per day = 24 / 18.0 = 1.333...
        # Planks per factory per day = 1 * 1.333... * 1 = 1.333...
        cyclesPerDay = 24 / productionTime
        planksPerFactoryPerDay = planksInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botPartFactoriesCount * planksPerFactoryPerDay)

    # Bot Assembler Methods
    def getBotAssemblersNeededForBots(self, botsAmount: float) -> int:
        """
        Calculate the number of bot assemblers needed to produce a given
        amount of bots per day.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_ASSEMBLER)

        # Example: productionTime=36.0, outputQuantity=1, workers=2
        # Cycles per day = 24 / 36.0 = 0.666... cycles/day
        # Output per building = 1 * 0.666... * 2 = 1.333... bots/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botsAmount / outputPerBuilding)

    def getBotChassisNeededForBotsProduction(
            self, botAssemblersCount: int) -> int:
        """
        Calculate the number of bot chassis needed per day to keep a given
        number of bot assemblers running.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_ASSEMBLER)

        # Example: productionTime=36.0, botChassisInput=1, workers=2
        # Cycles per day = 24 / 36.0 = 0.666...
        # Bot chassis per assembler per day = 1 * 0.666... * 2 = 1.333...
        cyclesPerDay = 24 / productionTime
        botChassisPerAssemblerPerDay = botChassisInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botAssemblersCount * botChassisPerAssemblerPerDay)

    def getBotHeadsNeededForBotsProduction(
            self, botAssemblersCount: int) -> int:
        """
        Calculate the number of bot heads needed per day to keep a given
        number of bot assemblers running.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_ASSEMBLER)

        # Example: productionTime=36.0, botHeadsInput=1, workers=2
        # Cycles per day = 24 / 36.0 = 0.666...
        # Bot heads per assembler per day = 1 * 0.666... * 2 = 1.333...
        cyclesPerDay = 24 / productionTime
        botHeadsPerAssemblerPerDay = botHeadsInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botAssemblersCount * botHeadsPerAssemblerPerDay)

    def getBotLimbsNeededForBotsProduction(
            self, botAssemblersCount: int) -> int:
        """
        Calculate the number of bot limbs needed per day to keep a given
        number of bot assemblers running.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.BOT_ASSEMBLER)

        # Example: productionTime=36.0, botLimbsInput=4, workers=2
        # Cycles per day = 24 / 36.0 = 0.666...
        # Bot limbs per assembler per day = 4 * 0.666... * 2 = 5.333...
        cyclesPerDay = 24 / productionTime
        botLimbsPerAssemblerPerDay = botLimbsInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(botAssemblersCount * botLimbsPerAssemblerPerDay)

    # Explosives Factory Methods
    def getExplosivesFactoriesNeededForExplosives(
            self, explosivesAmount: float) -> int:
        """
        Calculate the number of explosives factories needed to produce a given
        amount of explosives per day.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.EXPLOSIVES_FACTORY)

        # Example: productionTime=3.0, outputQuantity=1, workers=1
        # Cycles per day = 24 / 3.0 = 8 cycles/day
        # Output per building = 1 * 8 * 1 = 8 explosives/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(explosivesAmount / outputPerBuilding)

    def getBadwaterNeededForExplosivesProduction(
            self, explosivesFactoriesCount: int) -> int:
        """
        Calculate the number of badwater needed per day to keep a given number
        of explosives factories running.
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
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.EXPLOSIVES_FACTORY)

        # Example: productionTime=3.0, badwaterInput=5, workers=1
        # Cycles per day = 24 / 3.0 = 8 cycles/day
        # Badwater per factory per day = 5 * 8 * 1 = 40
        cyclesPerDay = 24 / productionTime
        badwaterPerFactoryPerDay = badwaterInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(explosivesFactoriesCount * badwaterPerFactoryPerDay)

    # Centrifuge Methods
    def getCentrifugesNeededForExtract(self, extractAmount: float) -> int:
        """
        Calculate the number of centrifuges needed to produce a given amount
        of extract per day.
        """
        if extractAmount < 0:
            raise ValueError("Extract amount cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.CENTRIFUGE,
                                 GoodsRecipeName.EXTRACT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.CENTRIFUGE,
                                    recipeIndex)
        outputQuantity = self.factionData \
            .getGoodsOutputQuantity(GoodsBuildingName.CENTRIFUGE,
                                    recipeIndex)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.CENTRIFUGE)

        # Example: productionTime=0.75, outputQuantity=1, workers=1
        # Cycles per day = 24 / 0.75 = 32 cycles/day
        # Output per building = 1 * 32 * 1 = 32 extract/day
        cyclesPerDay = 24 / productionTime
        outputPerBuilding = outputQuantity * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(extractAmount / outputPerBuilding)

    def getBadwaterNeededForExtractProduction(
            self, centrifugesCount: int) -> int:
        """
        Calculate the number of badwater needed per day to keep a given number
        of centrifuges running.
        """
        if centrifugesCount < 0:
            raise ValueError("Centrifuges count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.CENTRIFUGE,
                                 GoodsRecipeName.EXTRACT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.CENTRIFUGE,
                                    recipeIndex)
        badwaterInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.CENTRIFUGE,
                                   GoodsRecipeName.EXTRACT,
                                   HarvestName.BADWATER)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.CENTRIFUGE)

        # Example: productionTime=0.75, badwaterInput=4, workers=1
        # Cycles per day = 24 / 0.75 = 32 cycles/day
        # Badwater per centrifuge per day = 4 * 32 * 1 = 128
        cyclesPerDay = 24 / productionTime
        badwaterPerCentrifugePerDay = badwaterInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(centrifugesCount * badwaterPerCentrifugePerDay)

    def getLogsNeededForExtractProduction(self, centrifugesCount: int) -> int:
        """
        Calculate the number of logs needed per day to keep a given number of
        centrifuges running.
        """
        if centrifugesCount < 0:
            raise ValueError("Centrifuges count cannot be negative.")

        recipeIndex = self.factionData \
            .getGoodsRecipeIndex(GoodsBuildingName.CENTRIFUGE,
                                 GoodsRecipeName.EXTRACT)
        productionTime = self.factionData \
            .getGoodsProductionTime(GoodsBuildingName.CENTRIFUGE,
                                    recipeIndex)
        logsInput = self.factionData \
            .getGoodsInputQuantity(GoodsBuildingName.CENTRIFUGE,
                                   GoodsRecipeName.EXTRACT,
                                   HarvestName.LOGS)
        workersPerBuilding = self.factionData \
            .getGoodsWorkers(GoodsBuildingName.CENTRIFUGE)

        # Example: productionTime=0.75, logsInput=0.1, workers=1
        # Cycles per day = 24 / 0.75 = 32 cycles/day
        # Logs per centrifuge per day = 0.1 * 32 * 1 = 3.2
        cyclesPerDay = 24 / productionTime
        logsPerCentrifugePerDay = logsInput * cyclesPerDay * \
            workersPerBuilding

        return math.ceil(centrifugesCount * logsPerCentrifugePerDay)
