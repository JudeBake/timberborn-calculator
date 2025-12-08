from typing import Any

import yaml as yaml

from .emunerators import ConsumptionType, CropName, DifficultyLevel
from .emunerators import HarvestName, TreeName
from .emunerators import DataKeys


class FactionData:
    """
    Faction data class for Timberborn.

    This class loads faction-specific data from YAML configuration files and
    provides methods to get related to faction attributes, difficulty
    modifiers, resource consumption, and production capabilities.
    """
    def __init__(self, dataSrc: str) -> None:
        """
        Initialize FactionData by loading faction configuration from a YAML
        file.

        This constructor reads a YAML file containing faction-specific data and
        initializes instance variables for faction name, difficulty levels,
        consumption rates, and production data (beehive, crops, trees, water,
        food processing, and goods).

        :param dataSrc: Path to the YAML file containing faction data.
        :type dataSrc: str

        :raises FileNotFoundError: If the specified YAML file does not exist.
        :raises yaml.YAMLError: If the YAML file is malformed or cannot be
                                parsed.
        :raises KeyError: If required keys are missing in the YAML structure.
        """
        with open(dataSrc, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)[DataKeys.FACTION_DATA]
            self.name = data[DataKeys.NAME]
            self.difficulty = data[DataKeys.DIFFICULTY]
            self.consumption = data[DataKeys.CONSUMPTION]
            self.beehive = data[DataKeys.PRODUCTION][DataKeys.BEEHIVE]
            self.crops = data[DataKeys.PRODUCTION][DataKeys.CROPS]
            self.trees = data[DataKeys.PRODUCTION][DataKeys.TREES]
            self.water = data[DataKeys.PRODUCTION][DataKeys.WATER]
            self.foodProcessing = \
                data[DataKeys.PRODUCTION][DataKeys.FOOD_PROCESSING]
            self.goods = data[DataKeys.PRODUCTION][DataKeys.GOODS]

    def getFactionName(self) -> str:
        """
        Get the faction name.

        :return: Faction name.
        :rtype: str
        """
        return self.name

    def getDifficultyModifier(self, difficulty: DifficultyLevel) -> float:
        """
        Get the difficulty modifier for a given difficulty level.

        :param difficulty: Difficulty level.
        :type difficulty: DifficultyLevel

        :return: Difficulty modifier.
        :rtype: float

        :raises ValueError: If the specified difficulty level is not found in
                            faction data.
        """
        for diffLevel in self.difficulty:
            if diffLevel[DataKeys.NAME] == difficulty.value:
                return diffLevel[DataKeys.MODIFIER]
        raise ValueError(f"Difficulty level {difficulty} not found.")

    def getConsumption(self, consumptionType: ConsumptionType) -> float:
        """
        Get the consumption value for a given consumption type.

        :param consumptionType: Consumption type (food or water).
        :type consumptionType: ConsumptionType

        :return: Consumption value.
        :rtype: float

        :raises ValueError: If the specified consumption type is not found in
                            faction data.
        """
        if consumptionType.value in self.consumption:
            return self.consumption[consumptionType.value]
        raise ValueError(f"Consumption type {consumptionType} not found.")

    def getBeehiveModifier(self) -> float:
        """
        Get the beehive production modifier for this faction.

        :return: Beehive production modifier.
        :rtype: float

        :raises ValueError: If the faction does not have access to beehives.
        """
        if self.beehive is None:
            raise ValueError("Faction does not have access to beehives.")
        return self.beehive[DataKeys.MODIFIER]

    def _getCrop(self, cropName: CropName) -> dict[str, Any]:
        """
        Private helper method to retrieve the crop dictionary for a given crop.

        :param cropName: The crop to retrieve.
        :type cropName: CropName

        :return: Dictionary containing all crop information.
        :rtype: dict[str, Any]

        :raises ValueError: If the specified crop is not found in faction data.
        """
        for crop in self.crops:
            if crop[DataKeys.NAME] == cropName.value:
                return crop
        raise ValueError(f"Crop '{cropName.value}' not found.")

    def getCropGrowthTime(self, cropName: CropName) -> int | None:
        """
        Get the growth time for a specified crop.

        :param cropName: The crop to retrieve growth time for.
        :type cropName: CropName

        :return: Growth time in days, or None if the crop doesn't require
                 initial growth.
        :rtype: int | None

        :raises ValueError: If the specified crop is not found in faction data.
        """
        crop = self._getCrop(cropName)
        return crop[DataKeys.GROWTH_TIME]

    def getCropHarvestName(self, cropName: CropName) -> HarvestName:
        """
        Get the harvest item name for a specified crop.

        :param cropName: The crop to retrieve harvest name for.
        :type cropName: CropName

        :return: The harvest item name as HarvestName enum.
        :rtype: HarvestName

        :raises ValueError: If the specified crop is not found in faction data.
        """
        crop = self._getCrop(cropName)
        harvestName = crop[DataKeys.HARVEST][0][DataKeys.NAME]
        return HarvestName(harvestName)

    def getCropHarvestTime(self, cropName: CropName) -> int:
        """
        Get the harvest time for a specified crop.

        :param cropName: The crop to retrieve harvest time for.
        :type cropName: CropName

        :return: Harvest time in days.
        :rtype: int

        :raises ValueError: If the specified crop is not found in faction data.
        """
        crop = self._getCrop(cropName)
        return crop[DataKeys.HARVEST][0][DataKeys.TIME]

    def getCropHarvestYield(self, cropName: CropName) -> int:
        """
        Get the harvest yield for a specified crop.

        :param cropName: The crop to retrieve harvest yield for.
        :type cropName: CropName

        :return: Harvest yield quantity.
        :rtype: int

        :raises ValueError: If the specified crop is not found in faction data.
        """
        crop = self._getCrop(cropName)
        return crop[DataKeys.HARVEST][0][DataKeys.YIELD]

    def _getTree(self, treeName: TreeName) -> dict[str, Any]:
        """
        Private helper method to retrieve the tree dictionary for a given tree.

        :param treeName: The tree to retrieve.
        :type treeName: TreeName

        :return: Dictionary containing all tree information.
        :rtype: dict[str, Any]

        :raises ValueError: If the specified tree is not found in faction data.
        """
        for tree in self.trees:
            if tree[DataKeys.NAME] == treeName.value:
                return tree
        raise ValueError(f"Tree '{treeName.value}' not found.")

    def getTreeGrowthTime(self, treeName: TreeName) -> int:
        """
        Get the growth time for a specified tree.

        :param treeName: The tree to retrieve growth time for.
        :type treeName: TreeName

        :return: Growth time in days.
        :rtype: int

        :raises ValueError: If the specified tree is not found in faction data.
        """
        tree = self._getTree(treeName)
        return tree[DataKeys.GROWTH_TIME]

    def getTreeLogOutput(self, treeName: TreeName) -> int:
        """
        Get the log output for a specified tree.

        :param treeName: The tree to retrieve log output for.
        :type treeName: TreeName

        :return: Log output quantity.
        :rtype: int

        :raises ValueError: If the specified tree is not found in faction data.
        """
        tree = self._getTree(treeName)
        return tree[DataKeys.LOG_OUTPUT]

    def getTreeHarvestName(self, treeName: TreeName) -> HarvestName:
        """
        Get the harvest item name for a specified tree.

        :param treeName: The tree to retrieve harvest name for.
        :type treeName: TreeName

        :return: The harvest item name as HarvestName enum.
        :rtype: HarvestName

        :raises ValueError: If the specified tree is not found in faction data
                            or if the tree does not produce a harvestable item.
        """
        tree = self._getTree(treeName)
        if tree[DataKeys.HARVEST] is None:
            raise ValueError(f"Tree '{treeName.value}' does not produce a "
                             f"harvestable item.")
        harvestName = tree[DataKeys.HARVEST][0][DataKeys.NAME]
        return HarvestName(harvestName)

    def getTreeHarvestTime(self, treeName: TreeName) -> int:
        """
        Get the harvest time for a specified tree.

        :param treeName: The tree to retrieve harvest time for.
        :type treeName: TreeName

        :return: Harvest time in days.
        :rtype: int

        :raises ValueError: If the specified tree is not found in faction data
                            or if the tree does not produce a harvestable item.
        """
        tree = self._getTree(treeName)
        if tree[DataKeys.HARVEST] is None:
            raise ValueError(f"Tree '{treeName.value}' does not produce a "
                             f"harvestable item.")
        return tree[DataKeys.HARVEST][0][DataKeys.TIME]

    def getTreeHarvestYield(self, treeName: TreeName) -> int:
        """
        Get the harvest yield for a specified tree.

        :param treeName: The tree to retrieve harvest yield for.
        :type treeName: TreeName

        :return: Harvest yield quantity.
        :rtype: int

        :raises ValueError: If the specified tree is not found in faction data
                            or if the tree does not produce a harvestable item.
        """
        tree = self._getTree(treeName)
        if tree[DataKeys.HARVEST] is None:
            raise ValueError(f"Tree '{treeName.value}' does not produce a "
                             f"harvestable item.")
        return tree[DataKeys.HARVEST][0][DataKeys.YIELD]


if __name__ == '__main__':
    folktails = FactionData('./data/factions/folktails.yml')
    print(folktails.getFactionName())
