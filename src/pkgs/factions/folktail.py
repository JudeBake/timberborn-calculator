import math

from ..data.emunerators import ConsumptionType, CropName, DifficultyLevel
from ..data.emunerators import TreeName
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
