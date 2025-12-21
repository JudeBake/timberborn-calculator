from typing import Any

import yaml as yaml

from .enumerators import ConsumptionType, CropName, DifficultyLevel
from .enumerators import FoodProcessingBuildingName, FoodRecipeName
from .enumerators import GoodsBuildingName, GoodsRecipeName
from .enumerators import HarvestName, TreeName, WaterBuildingName
from .enumerators import DataKeys


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

    def _getWater(self,
                  waterBuildingName: WaterBuildingName) -> dict[str, Any]:
        """
        Private helper method to retrieve the water building dictionary.

        :param waterBuildingName: The water building to retrieve.
        :type waterBuildingName: WaterBuildingName

        :return: Dictionary containing all water building information.
        :rtype: dict[str, Any]

        :raises ValueError: If the specified water building is not found in
                            faction data.
        """
        for waterBuilding in self.water:
            if waterBuilding[DataKeys.NAME] == waterBuildingName.value:
                return waterBuilding
        raise ValueError(f"Water building '{waterBuildingName.value}' not "
                         f"found.")

    def getWaterWorkers(self, waterBuildingName: WaterBuildingName) -> int:
        """
        Get the number of workers for a specified water building.

        :param waterBuildingName: The water building to retrieve workers for.
        :type waterBuildingName: WaterBuildingName

        :return: Number of workers.
        :rtype: int

        :raises ValueError: If the specified water building is not found in
                            faction data.
        """
        waterBuilding = self._getWater(waterBuildingName)
        return waterBuilding[DataKeys.WORKERS]

    def getWaterRecipeName(self, waterBuildingName: WaterBuildingName) -> str:
        """
        Get the recipe name for a specified water building.

        :param waterBuildingName: The water building to retrieve recipe name
                                  for.
        :type waterBuildingName: WaterBuildingName

        :return: Recipe name.
        :rtype: str

        :raises ValueError: If the specified water building is not found in
                            faction data.
        """
        waterBuilding = self._getWater(waterBuildingName)
        return waterBuilding[DataKeys.RECIPES][0][DataKeys.NAME]

    def getWaterProductionTime(self,
                               waterBuildingName: WaterBuildingName) -> float:
        """
        Get the production time for a specified water building.

        :param waterBuildingName: The water building to retrieve production
                                  time for.
        :type waterBuildingName: WaterBuildingName

        :return: Production time.
        :rtype: float

        :raises ValueError: If the specified water building is not found in
                            faction data.
        """
        waterBuilding = self._getWater(waterBuildingName)
        return waterBuilding[DataKeys.RECIPES][0][DataKeys.PROD_TIME]

    def getWaterOutputQuantity(self,
                               waterBuildingName: WaterBuildingName) -> int:
        """
        Get the output quantity for a specified water building.

        :param waterBuildingName: The water building to retrieve output
                                  quantity for.
        :type waterBuildingName: WaterBuildingName

        :return: Output quantity.
        :rtype: int

        :raises ValueError: If the specified water building is not found in
                            faction data.
        """
        waterBuilding = self._getWater(waterBuildingName)
        return waterBuilding[DataKeys.RECIPES][0][DataKeys.OUT_QUANTITY]

    def _getFoodProcessing(self,
                           buildingName: FoodProcessingBuildingName
                           ) -> dict[str, Any]:
        """
        Private helper method to retrieve the food processing building
        dictionary.

        :param buildingName: The food processing building to retrieve.
        :type buildingName: FoodProcessingBuildingName

        :return: Dictionary containing all food processing building
                 information.
        :rtype: dict[str, Any]

        :raises ValueError: If the specified food processing building is not
                            found in faction data.
        """
        for building in self.foodProcessing:
            if building[DataKeys.NAME] == buildingName.value:
                return building
        raise ValueError(f"Food processing building '{buildingName.value}' "
                         f"not found.")

    def getFoodProcessingWorkers(self,
                                 buildingName: FoodProcessingBuildingName
                                 ) -> int:
        """
        Get the number of workers for a specified food processing building.

        :param buildingName: The food processing building to retrieve workers
                             for.
        :type buildingName: FoodProcessingBuildingName

        :return: Number of workers.
        :rtype: int

        :raises ValueError: If the specified food processing building is not
                            found in faction data.
        """
        building = self._getFoodProcessing(buildingName)
        return building[DataKeys.WORKERS]

    def getFoodProcessingRecipeCount(self,
                                     buildingName: FoodProcessingBuildingName
                                     ) -> int:
        """
        Get the number of recipes for a specified food processing building.

        :param buildingName: The food processing building to retrieve recipe
                             count for.
        :type buildingName: FoodProcessingBuildingName

        :return: Number of recipes.
        :rtype: int

        :raises ValueError: If the specified food processing building is not
                            found in faction data.
        """
        building = self._getFoodProcessing(buildingName)
        return len(building[DataKeys.RECIPES])

    def getFoodProcessingRecipeName(self,
                                    buildingName: FoodProcessingBuildingName,
                                    recipeIndex: int) -> str:
        """
        Get the recipe name for a specified food processing building and
        recipe index.

        :param buildingName: The food processing building to retrieve recipe
                             name for.
        :type buildingName: FoodProcessingBuildingName
        :param recipeIndex: The index of the recipe.
        :type recipeIndex: int

        :return: Recipe name.
        :rtype: str

        :raises ValueError: If the specified food processing building is not
                            found in faction data.
        :raises IndexError: If the recipe index is out of range.
        """
        building = self._getFoodProcessing(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.NAME]

    def getFoodProcessingProductionTime(self,
                                        buildingName:
                                        FoodProcessingBuildingName,
                                        recipeIndex: int) -> float:
        """
        Get the production time for a specified food processing building and
        recipe index.

        :param buildingName: The food processing building to retrieve
                             production time for.
        :type buildingName: FoodProcessingBuildingName
        :param recipeIndex: The index of the recipe.
        :type recipeIndex: int

        :return: Production time.
        :rtype: float

        :raises ValueError: If the specified food processing building is not
                            found in faction data.
        :raises IndexError: If the recipe index is out of range.
        """
        building = self._getFoodProcessing(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.PROD_TIME]

    def getFoodProcessingOutputQuantity(self,
                                        buildingName:
                                        FoodProcessingBuildingName,
                                        recipeIndex: int) -> int:
        """
        Get the output quantity for a specified food processing building and
        recipe index.

        :param buildingName: The food processing building to retrieve output
                             quantity for.
        :type buildingName: FoodProcessingBuildingName
        :param recipeIndex: The index of the recipe.
        :type recipeIndex: int

        :return: Output quantity.
        :rtype: int

        :raises ValueError: If the specified food processing building is not
                            found in faction data.
        :raises IndexError: If the recipe index is out of range.
        """
        building = self._getFoodProcessing(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.OUT_QUANTITY]

    def getFoodProcessingRecipeIndex(self,
                                     buildingName: FoodProcessingBuildingName,
                                     recipeName: FoodRecipeName) -> int:
        """
        Get the recipe index for a specified food processing building and
        recipe name.

        :param buildingName: The food processing building to search in.
        :type buildingName: FoodProcessingBuildingName
        :param recipeName: The recipe name to find.
        :type recipeName: FoodRecipeName

        :return: Recipe index.
        :rtype: int

        :raises ValueError: If the specified food processing building is not
                            found in faction data or if the recipe name is not
                            found.
        """
        building = self._getFoodProcessing(buildingName)
        for index, recipe in enumerate(building[DataKeys.RECIPES]):
            if recipe[DataKeys.NAME] == recipeName.value:
                return index
        raise ValueError(f"Recipe '{recipeName.value}' not found in "
                         f"'{buildingName.value}'.")

    def getFoodProcessingInputIndex(self,
                                    buildingName: FoodProcessingBuildingName,
                                    recipeName: FoodRecipeName,
                                    inputName: str) -> int:
        """
        Get the input index for a specified food processing building, recipe,
        and input name.

        :param buildingName: The food processing building to search in.
        :type buildingName: FoodProcessingBuildingName
        :param recipeName: The recipe to search in.
        :type recipeName: FoodRecipeName
        :param inputName: The input name to find.
        :type inputName: str

        :return: Input index.
        :rtype: int

        :raises ValueError: If the specified food processing building, recipe,
                            or input is not found in faction data.
        """
        recipeIndex = self.getFoodProcessingRecipeIndex(buildingName,
                                                        recipeName)
        building = self._getFoodProcessing(buildingName)
        inputs = building[DataKeys.RECIPES][recipeIndex][DataKeys.INPUTS]

        if inputs is None:
            raise ValueError(f"Recipe '{recipeName.value}' in "
                             f"'{buildingName.value}' has no inputs.")

        for index, input_item in enumerate(inputs):
            if input_item[DataKeys.NAME] == inputName:
                return index
        raise ValueError(f"Input '{inputName}' not found in recipe "
                         f"'{recipeName.value}' of '{buildingName.value}'.")

    def getFoodProcessingInputQuantity(self,
                                       buildingName:
                                       FoodProcessingBuildingName,
                                       recipeName: FoodRecipeName,
                                       inputName: str) -> float:
        """
        Get the input quantity for a specified food processing building,
        recipe, and input name.

        :param buildingName: The food processing building.
        :type buildingName: FoodProcessingBuildingName
        :param recipeName: The recipe.
        :type recipeName: FoodRecipeName
        :param inputName: The input name.
        :type inputName: str

        :return: Input quantity.
        :rtype: float

        :raises ValueError: If the specified food processing building, recipe,
                            or input is not found in faction data.
        """
        inputIndex = self.getFoodProcessingInputIndex(buildingName, recipeName,
                                                      inputName)
        recipeIndex = self.getFoodProcessingRecipeIndex(buildingName,
                                                        recipeName)
        building = self._getFoodProcessing(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.INPUTS][inputIndex][DataKeys.QUANTITY]  # noqa: %01

    def _getGoods(self, buildingName: GoodsBuildingName) -> dict[str, Any]:
        """
        Private helper method to retrieve the goods building dictionary.

        :param buildingName: The goods building to retrieve.
        :type buildingName: GoodsBuildingName

        :return: Dictionary containing all goods building information.
        :rtype: dict[str, Any]

        :raises ValueError: If the specified goods building is not found in
                            faction data.
        """
        for building in self.goods:
            if building[DataKeys.NAME] == buildingName.value:
                return building
        raise ValueError(f"Goods building '{buildingName.value}' not found.")

    def getGoodsWorkers(self, buildingName: GoodsBuildingName) -> int:
        """
        Get the number of workers for a specified goods building.

        :param buildingName: The goods building to retrieve workers for.
        :type buildingName: GoodsBuildingName

        :return: Number of workers.
        :rtype: int

        :raises ValueError: If the specified goods building is not found in
                            faction data.
        """
        building = self._getGoods(buildingName)
        return building[DataKeys.WORKERS]

    def getGoodsRecipeCount(self, buildingName: GoodsBuildingName) -> int:
        """
        Get the number of recipes for a specified goods building.

        :param buildingName: The goods building to retrieve recipe count for.
        :type buildingName: GoodsBuildingName

        :return: Number of recipes.
        :rtype: int

        :raises ValueError: If the specified goods building is not found in
                            faction data.
        """
        building = self._getGoods(buildingName)
        return len(building[DataKeys.RECIPES])

    def getGoodsRecipeName(self, buildingName: GoodsBuildingName,
                           recipeIndex: int) -> str:
        """
        Get the recipe name for a specified goods building and recipe index.

        :param buildingName: The goods building to retrieve recipe name for.
        :type buildingName: GoodsBuildingName
        :param recipeIndex: The index of the recipe.
        :type recipeIndex: int

        :return: Recipe name.
        :rtype: str

        :raises ValueError: If the specified goods building is not found in
                            faction data.
        :raises IndexError: If the recipe index is out of range.
        """
        building = self._getGoods(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.NAME]

    def getGoodsProductionTime(self, buildingName: GoodsBuildingName,
                               recipeIndex: int) -> float:
        """
        Get the production time for a specified goods building and recipe
        index.

        :param buildingName: The goods building to retrieve production time
                             for.
        :type buildingName: GoodsBuildingName
        :param recipeIndex: The index of the recipe.
        :type recipeIndex: int

        :return: Production time.
        :rtype: float

        :raises ValueError: If the specified goods building is not found in
                            faction data.
        :raises IndexError: If the recipe index is out of range.
        """
        building = self._getGoods(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.PROD_TIME]

    def getGoodsInputs(self, buildingName: GoodsBuildingName,
                       recipeIndex: int) -> list[dict[str, Any]] | None:
        """
        Get the inputs for a specified goods building and recipe index.

        :param buildingName: The goods building to retrieve inputs for.
        :type buildingName: GoodsBuildingName
        :param recipeIndex: The index of the recipe.
        :type recipeIndex: int

        :return: List of input dictionaries or None if no inputs required.
        :rtype: list[dict[str, Any]] | None

        :raises ValueError: If the specified goods building is not found in
                            faction data.
        :raises IndexError: If the recipe index is out of range.
        """
        building = self._getGoods(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.INPUTS]

    def getGoodsOutputQuantity(self, buildingName: GoodsBuildingName,
                               recipeIndex: int) -> int:
        """
        Get the output quantity for a specified goods building and recipe
        index.

        :param buildingName: The goods building to retrieve output quantity
                             for.
        :type buildingName: GoodsBuildingName
        :param recipeIndex: The index of the recipe.
        :type recipeIndex: int

        :return: Output quantity.
        :rtype: int

        :raises ValueError: If the specified goods building is not found in
                            faction data.
        :raises IndexError: If the recipe index is out of range.
        """
        building = self._getGoods(buildingName)
        return building[DataKeys.RECIPES][recipeIndex][DataKeys.OUT_QUANTITY]

    def getGoodsRecipeIndex(self, buildingName: GoodsBuildingName,
                            recipeName: GoodsRecipeName) -> int:
        """
        Find the recipe index for a given goods building and recipe name.

        :param buildingName: The goods building.
        :type buildingName: GoodsBuildingName
        :param recipeName: The recipe name to search for.
        :type recipeName: GoodsRecipeName

        :return: The index of the recipe.
        :rtype: int

        :raises ValueError: If the specified goods building is not found
                            or if the recipe is not found in the building.
        """
        building = self._getGoods(buildingName)
        recipes = building[DataKeys.RECIPES]

        for index, recipe in enumerate(recipes):
            if recipe[DataKeys.NAME] == recipeName.value:
                return index

        raise ValueError(f"Recipe '{recipeName.value}' not found in "
                         f"building '{buildingName.value}'.")

    def getGoodsInputQuantity(self, buildingName: GoodsBuildingName,
                              recipeName: 'GoodsRecipeName',
                              inputName: str) -> float:
        """
        Get the quantity of a specific input for a goods recipe.

        :param buildingName: The goods building.
        :type buildingName: GoodsBuildingName
        :param recipeName: The recipe name.
        :type recipeName: GoodsRecipeName
        :param inputName: The name of the input to get quantity for.
        :type inputName: str

        :return: The quantity of the specified input.
        :rtype: float

        :raises ValueError: If the specified building or recipe is not found,
                            or if the input is not found in the recipe.
        """
        recipeIndex = self.getGoodsRecipeIndex(buildingName, recipeName)
        inputs = self.getGoodsInputs(buildingName, recipeIndex)

        if inputs is None:
            raise ValueError(f"Recipe '{recipeName.value}' in building "
                             f"'{buildingName.value}' has no inputs.")

        for input_item in inputs:
            if input_item[DataKeys.NAME] == inputName:
                return input_item[DataKeys.QUANTITY]

        raise ValueError(f"Input '{inputName}' not found in recipe "
                         f"'{recipeName.value}' for building "
                         f"'{buildingName.value}'.")


if __name__ == '__main__':
    folktails = FactionData('./data/factions/folktails.yml')
    print(folktails.getFactionName())
