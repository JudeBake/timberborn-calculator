from ..data.emunerators import ConsumptionType, DifficultyLevel
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
