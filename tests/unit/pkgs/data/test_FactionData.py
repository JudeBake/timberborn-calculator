from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import yaml as yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.data.factionData import FactionData                   # noqa: E402
from pkgs.data.enumerators import ConsumptionType, CropName, \
    DifficultyLevel, FoodProcessingBuildingName, FoodRecipeName, \
    GoodsBuildingName, GoodsRecipeName, HarvestName, TreeName, \
    WaterBuildingName                                           # noqa: E402


class TestFolktails(TestCase):
    """
    FactionData class test cases.
    """
    def setUp(self) -> None:
        """
        Test setup.
        """
        testDataPath = "./tests/unit/pkgs/data/test.yml"
        with open(testDataPath, "r", encoding="utf-8") as file:
            self.fullTestData = yaml.safe_load(file)
            self.testData = self.fullTestData['faction_data']
        data = "data"
        with patch("builtins.open", mock_open(read_data=data)), \
                patch("yaml.safe_load") as mockedYamlLoad:
            mockedYamlLoad.return_value = self.fullTestData
            self.uut = FactionData('./data/non_existent_file.yml')

    def test_constructorErrorOpenFile(self) -> None:
        """
        The constructor must raise any error raised by opening the data file.
        """
        errMsg = "File not found."
        dataSrc = "./data/non_existent_file.yml"
        with patch("builtins.open", mock_open()) as mockedOpen, \
                self.assertRaises(IOError) as context:
            mockedOpen.side_effect = IOError(errMsg)
            FactionData(dataSrc)
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorErrorLoadYaml(self) -> None:
        """
        The constructor must raise any error raised by loading the YAML data.
        """
        data = "data"
        errMsg = "YAML error."
        dataSrc = "./data/non_existent_file.yml"
        with patch("builtins.open", mock_open(read_data=data)) as mockedOpen, \
                patch("yaml.safe_load") as mockedYamlLoad, \
                self.assertRaises(yaml.YAMLError) as context:
            mockedYamlLoad.side_effect = yaml.YAMLError(errMsg)
            FactionData(dataSrc)
            mockedYamlLoad.assert_called_once_with(mockedOpen())
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorSuccess(self) -> None:
        """
        The constructor must save internally the data when the load operation
        succeeds.
        """
        data = "data"
        dataSrc = "./data/non_existent_file.yml"
        with patch("builtins.open", mock_open(read_data=data)) as mockedOpen, \
                patch("yaml.safe_load") as mockedYamlLoad:
            mockedYamlLoad.return_value = self.fullTestData
            folktails = FactionData(dataSrc)
            mockedOpen.assert_called_once_with(dataSrc, 'r', encoding='utf-8')
            mockedYamlLoad.assert_called_once_with(mockedOpen())
        self.assertEqual(self.testData['name'], folktails.name)
        self.assertEqual(self.testData['difficulty'], folktails.difficulty)
        self.assertEqual(self.testData['consumption'], folktails.consumption)
        self.assertEqual(self.testData['production']['beehive'],
                         folktails.beehive)
        self.assertEqual(self.testData['production']['crops'],
                         folktails.crops)
        self.assertEqual(self.testData['production']['trees'],
                         folktails.trees)
        self.assertEqual(self.testData['production']['water'],
                         folktails.water)
        self.assertEqual(self.testData['production']['food_processing'],
                         folktails.foodProcessing)
        self.assertEqual(self.testData['production']['goods'],
                         folktails.goods)

    def test_getFactionName(self) -> None:
        """
        The getFactionName method must return the faction name.
        """
        name = 'test name'
        self.uut.name = name
        self.assertEqual(name, self.uut.getFactionName())

    def test_getDifficultyModifierValueError(self) -> None:
        """
        The getDifficultyModifier method must raise a ValueError when the
        requested difficulty level is not found.
        """
        difficultyLevel = Mock()
        difficultyLevel.value = 'non_existent_level'
        with self.assertRaises(ValueError) as context:
            self.uut.getDifficultyModifier(difficultyLevel)
        self.assertEqual(f"Difficulty level {difficultyLevel} not found.",
                         str(context.exception))

    def test_getDifficultyModifierSuccess(self) -> None:
        """
        The getDifficultyModifier method must return the correct modifier
        for a given difficulty level.
        """
        for diffLevel in DifficultyLevel:
            expectedDiffLevel = next((
                item for item in self.testData['difficulty']
                if item['name'] == diffLevel.value), None)['modifier']
            self.assertIsNotNone(expectedDiffLevel,
                                 f"Test data missing difficulty level "
                                 f"{diffLevel.value}.")
            modifier = self.uut.getDifficultyModifier(diffLevel)
            self.assertEqual(expectedDiffLevel, modifier)

    def test_getConsumptionValueError(self) -> None:
        """
        The getConsumption method must raise a ValueError when the requested
        consumption type is not found.
        """
        consumptionType = Mock()
        consumptionType.value = 'non_existent_type'
        with self.assertRaises(ValueError) as context:
            self.uut.getConsumption(consumptionType)
        self.assertEqual(f"Consumption type {consumptionType} not found.",
                         str(context.exception))

    def test_getConsumptionSuccess(self) -> None:
        """
        The getConsumption method must return the correct consumption value
        for a given consumption type.
        """
        for type in ConsumptionType:
            expectedConsumption = next((
                value for key, value in self.testData['consumption'].items()
                if key == type.value), None)
            self.assertIsNotNone(expectedConsumption,
                                 f"Test data missing consumption type "
                                 f"{type.value}.")
            value = self.uut.getConsumption(type)
            self.assertEqual(expectedConsumption, value)

    def test_getBeehiveModifierValueError(self) -> None:
        """
        The getBeehiveModifier method must raise a ValueError when the
        faction does not have access to beehives.
        """
        self.uut.beehive = None
        with self.assertRaises(ValueError) as context:
            self.uut.getBeehiveModifier()
        self.assertEqual("Faction does not have access to beehives.",
                         str(context.exception))

    def test_getBeehiveModifierSuccess(self) -> None:
        """
        The getBeehiveModifier method must return the correct beehive
        modifier value.
        """
        expectedModifier = self.testData['production']['beehive']['modifier']
        modifier = self.uut.getBeehiveModifier()
        self.assertEqual(expectedModifier, modifier)

    def test_getCropValueError(self) -> None:
        """
        The _getCrop private method must raise a ValueError when the
        requested crop is not found.
        """
        # Test with Iron Teeth crop on Folktails faction
        cropName = CropName.COFFEE_BUSH
        with self.assertRaises(ValueError) as context:
            self.uut._getCrop(cropName)
        self.assertEqual(f"Crop '{cropName.value}' not found.",
                         str(context.exception))

    def test_getCropSuccess(self) -> None:
        """
        The _getCrop private method must return the correct crop dictionary
        for a given crop name.
        """
        # Map of crop names from test data to CropName enum values
        cropNameMap = {
            'Berry Bush': CropName.BERRY_BUSH,
            'Dandelion Bush': CropName.DANDELION_BUSH,
            'Carrot Crop': CropName.CARROT_CROP,
            'Sunflower Crop': CropName.SUNFLOWER_CROP,
            'Potato Crop': CropName.POTATO_CROP,
            'Wheat Crop': CropName.WHEAT_CROP,
            'Cattail Crop': CropName.CATTAIL_CROP,
            'Spadderdock Crop': CropName.SPADDERDOCK_CROP,
        }

        for crop in self.testData['production']['crops']:
            cropNameStr = crop['name']
            cropNameEnum = cropNameMap[cropNameStr]
            cropDict = self.uut._getCrop(cropNameEnum)
            self.assertEqual(crop, cropDict)

    def test_getCropGrowthTimeValueError(self) -> None:
        """
        The getCropGrowthTime method must raise a ValueError when the
        requested crop is not found (via _getCrop).
        """
        cropName = CropName.COFFEE_BUSH
        with patch.object(self.uut, '_getCrop') as mockedGetCrop, \
                self.assertRaises(ValueError) as context:
            mockedGetCrop.side_effect = ValueError(
                f"Crop '{cropName.value}' not found.")
            self.uut.getCropGrowthTime(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
        self.assertEqual(f"Crop '{cropName.value}' not found.",
                         str(context.exception))

    def test_getCropGrowthTimeSuccess(self) -> None:
        """
        The getCropGrowthTime method must return the correct growth time
        for a given crop name.
        """
        cropName = CropName.BERRY_BUSH
        mockCropDict = {'growth_time': 12}
        with patch.object(self.uut, '_getCrop') as mockedGetCrop:
            mockedGetCrop.return_value = mockCropDict
            growthTime = self.uut.getCropGrowthTime(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
            self.assertEqual(12, growthTime)

    def test_getCropHarvestNameValueError(self) -> None:
        """
        The getCropHarvestName method must raise a ValueError when the
        requested crop is not found (via _getCrop).
        """
        cropName = CropName.COFFEE_BUSH
        with patch.object(self.uut, '_getCrop') as mockedGetCrop, \
                self.assertRaises(ValueError) as context:
            mockedGetCrop.side_effect = ValueError(
                f"Crop '{cropName.value}' not found.")
            self.uut.getCropHarvestName(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
        self.assertEqual(f"Crop '{cropName.value}' not found.",
                         str(context.exception))

    def test_getCropHarvestNameSuccess(self) -> None:
        """
        The getCropHarvestName method must return the correct harvest name
        as HarvestName enum for a given crop.
        """
        cropName = CropName.BERRY_BUSH
        mockCropDict = {'harvest': [{'name': 'Berries'}]}
        with patch.object(self.uut, '_getCrop') as mockedGetCrop:
            mockedGetCrop.return_value = mockCropDict
            harvestName = self.uut.getCropHarvestName(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
            self.assertEqual(HarvestName.BERRIES, harvestName)
            self.assertIsInstance(harvestName, HarvestName)

    def test_getCropHarvestTimeValueError(self) -> None:
        """
        The getCropHarvestTime method must raise a ValueError when the
        requested crop is not found (via _getCrop).
        """
        cropName = CropName.COFFEE_BUSH
        with patch.object(self.uut, '_getCrop') as mockedGetCrop, \
                self.assertRaises(ValueError) as context:
            mockedGetCrop.side_effect = ValueError(
                f"Crop '{cropName.value}' not found.")
            self.uut.getCropHarvestTime(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
        self.assertEqual(f"Crop '{cropName.value}' not found.",
                         str(context.exception))

    def test_getCropHarvestTimeSuccess(self) -> None:
        """
        The getCropHarvestTime method must return the correct harvest time
        for a given crop.
        """
        cropName = CropName.BERRY_BUSH
        mockCropDict = {'harvest': [{'time': 12}]}
        with patch.object(self.uut, '_getCrop') as mockedGetCrop:
            mockedGetCrop.return_value = mockCropDict
            harvestTime = self.uut.getCropHarvestTime(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
            self.assertEqual(12, harvestTime)

    def test_getCropHarvestYieldValueError(self) -> None:
        """
        The getCropHarvestYield method must raise a ValueError when the
        requested crop is not found (via _getCrop).
        """
        cropName = CropName.COFFEE_BUSH
        with patch.object(self.uut, '_getCrop') as mockedGetCrop, \
                self.assertRaises(ValueError) as context:
            mockedGetCrop.side_effect = ValueError(
                f"Crop '{cropName.value}' not found.")
            self.uut.getCropHarvestYield(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
        self.assertEqual(f"Crop '{cropName.value}' not found.",
                         str(context.exception))

    def test_getCropHarvestYieldSuccess(self) -> None:
        """
        The getCropHarvestYield method must return the correct harvest yield
        for a given crop.
        """
        cropName = CropName.BERRY_BUSH
        mockCropDict = {'harvest': [{'yield': 3}]}
        with patch.object(self.uut, '_getCrop') as mockedGetCrop:
            mockedGetCrop.return_value = mockCropDict
            harvestYield = self.uut.getCropHarvestYield(cropName)
            mockedGetCrop.assert_called_once_with(cropName)
            self.assertEqual(3, harvestYield)

    def test_getTreeValueError(self) -> None:
        """
        The _getTree private method must raise a ValueError when the
        requested tree is not found.
        """
        # Test with Iron Teeth tree on Folktails faction
        treeName = TreeName.MANGROVE_TREE
        with self.assertRaises(ValueError) as context:
            self.uut._getTree(treeName)
        self.assertEqual(f"Tree '{treeName.value}' not found.",
                         str(context.exception))

    def test_getTreeSuccess(self) -> None:
        """
        The _getTree private method must return the correct tree dictionary
        for a given tree name.
        """
        # Map of tree names from test data to TreeName enum values
        treeNameMap = {
            'Birch': TreeName.BIRCH,
            'Pine': TreeName.PINE,
            'Maple': TreeName.MAPLE,
            'Chestnut Tree': TreeName.CHESTNUT_TREE,
            'Oak': TreeName.OAK,
        }

        for tree in self.testData['production']['trees']:
            treeNameStr = tree['name']
            treeNameEnum = treeNameMap[treeNameStr]
            treeDict = self.uut._getTree(treeNameEnum)
            self.assertEqual(tree, treeDict)

    def test_getTreeGrowthTimeValueError(self) -> None:
        """
        The getTreeGrowthTime method must raise a ValueError when the
        requested tree is not found (via _getTree).
        """
        treeName = TreeName.MANGROVE_TREE
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.side_effect = ValueError(
                f"Tree '{treeName.value}' not found.")
            self.uut.getTreeGrowthTime(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' not found.",
                         str(context.exception))

    def test_getTreeGrowthTimeSuccess(self) -> None:
        """
        The getTreeGrowthTime method must return the correct growth time
        for a given tree.
        """
        treeName = TreeName.BIRCH
        mockTreeDict = {'growth_time': 7}
        with patch.object(self.uut, '_getTree') as mockedGetTree:
            mockedGetTree.return_value = mockTreeDict
            growthTime = self.uut.getTreeGrowthTime(treeName)
            mockedGetTree.assert_called_once_with(treeName)
            self.assertEqual(7, growthTime)

    def test_getTreeLogOutputValueError(self) -> None:
        """
        The getTreeLogOutput method must raise a ValueError when the
        requested tree is not found (via _getTree).
        """
        treeName = TreeName.MANGROVE_TREE
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.side_effect = ValueError(
                f"Tree '{treeName.value}' not found.")
            self.uut.getTreeLogOutput(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' not found.",
                         str(context.exception))

    def test_getTreeLogOutputSuccess(self) -> None:
        """
        The getTreeLogOutput method must return the correct log output
        for a given tree.
        """
        treeName = TreeName.BIRCH
        mockTreeDict = {'log_output': 1}
        with patch.object(self.uut, '_getTree') as mockedGetTree:
            mockedGetTree.return_value = mockTreeDict
            logOutput = self.uut.getTreeLogOutput(treeName)
            mockedGetTree.assert_called_once_with(treeName)
            self.assertEqual(1, logOutput)

    def test_getTreeHarvestNameValueErrorTreeNotFound(self) -> None:
        """
        The getTreeHarvestName method must raise a ValueError when the
        requested tree is not found (via _getTree).
        """
        treeName = TreeName.MANGROVE_TREE
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.side_effect = ValueError(
                f"Tree '{treeName.value}' not found.")
            self.uut.getTreeHarvestName(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' not found.",
                         str(context.exception))

    def test_getTreeHarvestNameValueErrorNoHarvest(self) -> None:
        """
        The getTreeHarvestName method must raise a ValueError when the
        tree does not produce a harvestable item.
        """
        treeName = TreeName.BIRCH
        mockTreeDict = {'harvest': None}
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.return_value = mockTreeDict
            self.uut.getTreeHarvestName(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' does not produce a "
                         f"harvestable item.",
                         str(context.exception))

    def test_getTreeHarvestNameSuccess(self) -> None:
        """
        The getTreeHarvestName method must return the correct harvest name
        as HarvestName enum for a given tree.
        """
        treeName = TreeName.PINE
        mockTreeDict = {'harvest': [{'name': 'Pine Resin'}]}
        with patch.object(self.uut, '_getTree') as mockedGetTree:
            mockedGetTree.return_value = mockTreeDict
            harvestName = self.uut.getTreeHarvestName(treeName)
            mockedGetTree.assert_called_once_with(treeName)
            self.assertEqual(HarvestName.PINE_RESIN, harvestName)
            self.assertIsInstance(harvestName, HarvestName)

    def test_getTreeHarvestTimeValueErrorTreeNotFound(self) -> None:
        """
        The getTreeHarvestTime method must raise a ValueError when the
        requested tree is not found (via _getTree).
        """
        treeName = TreeName.MANGROVE_TREE
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.side_effect = ValueError(
                f"Tree '{treeName.value}' not found.")
            self.uut.getTreeHarvestTime(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' not found.",
                         str(context.exception))

    def test_getTreeHarvestTimeValueErrorNoHarvest(self) -> None:
        """
        The getTreeHarvestTime method must raise a ValueError when the
        tree does not produce a harvestable item.
        """
        treeName = TreeName.BIRCH
        mockTreeDict = {'harvest': None}
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.return_value = mockTreeDict
            self.uut.getTreeHarvestTime(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' does not produce a "
                         f"harvestable item.",
                         str(context.exception))

    def test_getTreeHarvestTimeSuccess(self) -> None:
        """
        The getTreeHarvestTime method must return the correct harvest time
        for a given tree.
        """
        treeName = TreeName.PINE
        mockTreeDict = {'harvest': [{'time': 7}]}
        with patch.object(self.uut, '_getTree') as mockedGetTree:
            mockedGetTree.return_value = mockTreeDict
            harvestTime = self.uut.getTreeHarvestTime(treeName)
            mockedGetTree.assert_called_once_with(treeName)
            self.assertEqual(7, harvestTime)

    def test_getTreeHarvestYieldValueErrorTreeNotFound(self) -> None:
        """
        The getTreeHarvestYield method must raise a ValueError when the
        requested tree is not found (via _getTree).
        """
        treeName = TreeName.MANGROVE_TREE
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.side_effect = ValueError(
                f"Tree '{treeName.value}' not found.")
            self.uut.getTreeHarvestYield(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' not found.",
                         str(context.exception))

    def test_getTreeHarvestYieldValueErrorNoHarvest(self) -> None:
        """
        The getTreeHarvestYield method must raise a ValueError when the
        tree does not produce a harvestable item.
        """
        treeName = TreeName.BIRCH
        mockTreeDict = {'harvest': None}
        with patch.object(self.uut, '_getTree') as mockedGetTree, \
                self.assertRaises(ValueError) as context:
            mockedGetTree.return_value = mockTreeDict
            self.uut.getTreeHarvestYield(treeName)
            mockedGetTree.assert_called_once_with(treeName)
        self.assertEqual(f"Tree '{treeName.value}' does not produce a "
                         f"harvestable item.",
                         str(context.exception))

    def test_getTreeHarvestYieldSuccess(self) -> None:
        """
        The getTreeHarvestYield method must return the correct harvest yield
        for a given tree.
        """
        treeName = TreeName.PINE
        mockTreeDict = {'harvest': [{'yield': 2}]}
        with patch.object(self.uut, '_getTree') as mockedGetTree:
            mockedGetTree.return_value = mockTreeDict
            harvestYield = self.uut.getTreeHarvestYield(treeName)
            mockedGetTree.assert_called_once_with(treeName)
            self.assertEqual(2, harvestYield)

    def test_getWaterValueError(self) -> None:
        """
        The _getWater private method must raise a ValueError when the
        requested water building is not found.
        """
        # Test with Iron Teeth water building on Folktails faction
        waterBuildingName = WaterBuildingName.DEEP_WATER_PUMP
        with self.assertRaises(ValueError) as context:
            self.uut._getWater(waterBuildingName)
        self.assertEqual(f"Water building '{waterBuildingName.value}' not "
                         f"found.",
                         str(context.exception))

    def test_getWaterSuccess(self) -> None:
        """
        The _getWater private method must return the correct water building
        dictionary for a given water building name.
        """
        # Map of water building names from test data to WaterBuildingName enum
        waterBuildingNameMap = {
            'Water Pump': WaterBuildingName.WATER_PUMP,
            'Large Water Pump': WaterBuildingName.LARGE_WATER_PUMP,
            'Badwater Pump': WaterBuildingName.BADWATER_PUMP,
        }

        for waterBuilding in self.testData['production']['water']:
            waterBuildingNameStr = waterBuilding['name']
            waterBuildingNameEnum = waterBuildingNameMap[waterBuildingNameStr]
            waterBuildingDict = self.uut._getWater(waterBuildingNameEnum)
            self.assertEqual(waterBuilding, waterBuildingDict)

    def test_getWaterWorkersValueError(self) -> None:
        """
        The getWaterWorkers method must raise a ValueError when the
        requested water building is not found (via _getWater).
        """
        waterBuildingName = WaterBuildingName.DEEP_WATER_PUMP
        with patch.object(self.uut, '_getWater') as mockedGetWater, \
                self.assertRaises(ValueError) as context:
            mockedGetWater.side_effect = ValueError(
                f"Water building '{waterBuildingName.value}' not found.")
            self.uut.getWaterWorkers(waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
        self.assertEqual(f"Water building '{waterBuildingName.value}' not "
                         f"found.",
                         str(context.exception))

    def test_getWaterWorkersSuccess(self) -> None:
        """
        The getWaterWorkers method must return the correct number of workers
        for a given water building.
        """
        waterBuildingName = WaterBuildingName.WATER_PUMP
        mockWaterDict = {'workers': 1}
        with patch.object(self.uut, '_getWater') as mockedGetWater:
            mockedGetWater.return_value = mockWaterDict
            workers = self.uut.getWaterWorkers(waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
            self.assertEqual(1, workers)

    def test_getWaterRecipeNameValueError(self) -> None:
        """
        The getWaterRecipeName method must raise a ValueError when the
        requested water building is not found (via _getWater).
        """
        waterBuildingName = WaterBuildingName.DEEP_WATER_PUMP
        with patch.object(self.uut, '_getWater') as mockedGetWater, \
                self.assertRaises(ValueError) as context:
            mockedGetWater.side_effect = ValueError(
                f"Water building '{waterBuildingName.value}' not found.")
            self.uut.getWaterRecipeName(waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
        self.assertEqual(f"Water building '{waterBuildingName.value}' not "
                         f"found.",
                         str(context.exception))

    def test_getWaterRecipeNameSuccess(self) -> None:
        """
        The getWaterRecipeName method must return the correct recipe name
        for a given water building.
        """
        waterBuildingName = WaterBuildingName.WATER_PUMP
        mockWaterDict = {'recipes': [{'name': 'Water'}]}
        with patch.object(self.uut, '_getWater') as mockedGetWater:
            mockedGetWater.return_value = mockWaterDict
            recipeName = self.uut.getWaterRecipeName(waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
            self.assertEqual('Water', recipeName)

    def test_getWaterProductionTimeValueError(self) -> None:
        """
        The getWaterProductionTime method must raise a ValueError when the
        requested water building is not found (via _getWater).
        """
        waterBuildingName = WaterBuildingName.DEEP_WATER_PUMP
        with patch.object(self.uut, '_getWater') as mockedGetWater, \
                self.assertRaises(ValueError) as context:
            mockedGetWater.side_effect = ValueError(
                f"Water building '{waterBuildingName.value}' not found.")
            self.uut.getWaterProductionTime(waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
        self.assertEqual(f"Water building '{waterBuildingName.value}' not "
                         f"found.",
                         str(context.exception))

    def test_getWaterProductionTimeSuccess(self) -> None:
        """
        The getWaterProductionTime method must return the correct production
        time for a given water building.
        """
        waterBuildingName = WaterBuildingName.WATER_PUMP
        mockWaterDict = {'recipes': [{'production_time': 0.33}]}
        with patch.object(self.uut, '_getWater') as mockedGetWater:
            mockedGetWater.return_value = mockWaterDict
            productionTime = self.uut.getWaterProductionTime(
                waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
            self.assertEqual(0.33, productionTime)

    def test_getWaterOutputQuantityValueError(self) -> None:
        """
        The getWaterOutputQuantity method must raise a ValueError when the
        requested water building is not found (via _getWater).
        """
        waterBuildingName = WaterBuildingName.DEEP_WATER_PUMP
        with patch.object(self.uut, '_getWater') as mockedGetWater, \
                self.assertRaises(ValueError) as context:
            mockedGetWater.side_effect = ValueError(
                f"Water building '{waterBuildingName.value}' not found.")
            self.uut.getWaterOutputQuantity(waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
        self.assertEqual(f"Water building '{waterBuildingName.value}' not "
                         f"found.",
                         str(context.exception))

    def test_getWaterOutputQuantitySuccess(self) -> None:
        """
        The getWaterOutputQuantity method must return the correct output
        quantity for a given water building.
        """
        waterBuildingName = WaterBuildingName.WATER_PUMP
        mockWaterDict = {'recipes': [{'output_quantity': 1}]}
        with patch.object(self.uut, '_getWater') as mockedGetWater:
            mockedGetWater.return_value = mockWaterDict
            outputQuantity = self.uut.getWaterOutputQuantity(
                waterBuildingName)
            mockedGetWater.assert_called_once_with(waterBuildingName)
            self.assertEqual(1, outputQuantity)

    def test_getFoodProcessingValueError(self) -> None:
        """
        The _getFoodProcessing private method must raise a ValueError when
        the requested food processing building is not found.
        """
        # Test with Iron Teeth building on Folktails faction
        buildingName = FoodProcessingBuildingName.COFFEE_BREWERY
        with self.assertRaises(ValueError) as context:
            self.uut._getFoodProcessing(buildingName)
        self.assertEqual(f"Food processing building '{buildingName.value}' "
                         f"not found.",
                         str(context.exception))

    def test_getFoodProcessingSuccess(self) -> None:
        """
        The _getFoodProcessing private method must return the correct food
        processing building dictionary for a given building name.
        """
        # Map of building names from test data to FoodProcessingBuildingName
        buildingNameMap = {
            'Grill': FoodProcessingBuildingName.GRILL,
            'Gristmill': FoodProcessingBuildingName.GRISTMILL,
            'Bakery': FoodProcessingBuildingName.BAKERY,
        }

        for building in self.testData['production']['food_processing']:
            buildingNameStr = building['name']
            buildingNameEnum = buildingNameMap[buildingNameStr]
            buildingDict = self.uut._getFoodProcessing(buildingNameEnum)
            self.assertEqual(building, buildingDict)

    def test_getFoodProcessingWorkersValueError(self) -> None:
        """
        The getFoodProcessingWorkers method must raise a ValueError when the
        requested food processing building is not found (via
        _getFoodProcessing).
        """
        buildingName = FoodProcessingBuildingName.COFFEE_BREWERY
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGet.side_effect = ValueError(
                f"Food processing building '{buildingName.value}' not found.")
            self.uut.getFoodProcessingWorkers(buildingName)
            mockedGet.assert_called_once_with(buildingName)
        self.assertEqual(f"Food processing building '{buildingName.value}' "
                         f"not found.",
                         str(context.exception))

    def test_getFoodProcessingWorkersSuccess(self) -> None:
        """
        The getFoodProcessingWorkers method must return the correct number
        of workers for a given food processing building.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        mockBuildingDict = {'workers': 1}
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGet.return_value = mockBuildingDict
            workers = self.uut.getFoodProcessingWorkers(buildingName)
            mockedGet.assert_called_once_with(buildingName)
            self.assertEqual(1, workers)

    def test_getFoodProcessingRecipeCountValueError(self) -> None:
        """
        The getFoodProcessingRecipeCount method must raise a ValueError when
        the requested food processing building is not found (via
        _getFoodProcessing).
        """
        buildingName = FoodProcessingBuildingName.COFFEE_BREWERY
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGet.side_effect = ValueError(
                f"Food processing building '{buildingName.value}' not found.")
            self.uut.getFoodProcessingRecipeCount(buildingName)
            mockedGet.assert_called_once_with(buildingName)
        self.assertEqual(f"Food processing building '{buildingName.value}' "
                         f"not found.",
                         str(context.exception))

    def test_getFoodProcessingRecipeCountSuccess(self) -> None:
        """
        The getFoodProcessingRecipeCount method must return the correct
        number of recipes for a given food processing building.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        mockBuildingDict = {'recipes': [{}, {}, {}]}
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGet.return_value = mockBuildingDict
            recipeCount = self.uut.getFoodProcessingRecipeCount(buildingName)
            mockedGet.assert_called_once_with(buildingName)
            self.assertEqual(3, recipeCount)

    def test_getFoodProcessingRecipeNameValueError(self) -> None:
        """
        The getFoodProcessingRecipeName method must raise a ValueError when
        the requested food processing building is not found (via
        _getFoodProcessing).
        """
        buildingName = FoodProcessingBuildingName.COFFEE_BREWERY
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGet.side_effect = ValueError(
                f"Food processing building '{buildingName.value}' not found.")
            self.uut.getFoodProcessingRecipeName(buildingName, 0)
            mockedGet.assert_called_once_with(buildingName)
        self.assertEqual(f"Food processing building '{buildingName.value}' "
                         f"not found.",
                         str(context.exception))

    def test_getFoodProcessingRecipeNameSuccess(self) -> None:
        """
        The getFoodProcessingRecipeName method must return the correct recipe
        name for a given food processing building and recipe index.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        mockBuildingDict = {'recipes': [{'name': 'Grilled Potatoes'}]}
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGet.return_value = mockBuildingDict
            recipeName = self.uut.getFoodProcessingRecipeName(buildingName, 0)
            mockedGet.assert_called_once_with(buildingName)
            self.assertEqual('Grilled Potatoes', recipeName)

    def test_getFoodProcessingProductionTimeValueError(self) -> None:
        """
        The getFoodProcessingProductionTime method must raise a ValueError
        when the requested food processing building is not found (via
        _getFoodProcessing).
        """
        buildingName = FoodProcessingBuildingName.COFFEE_BREWERY
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGet.side_effect = ValueError(
                f"Food processing building '{buildingName.value}' not found.")
            self.uut.getFoodProcessingProductionTime(buildingName, 0)
            mockedGet.assert_called_once_with(buildingName)
        self.assertEqual(f"Food processing building '{buildingName.value}' "
                         f"not found.",
                         str(context.exception))

    def test_getFoodProcessingProductionTimeSuccess(self) -> None:
        """
        The getFoodProcessingProductionTime method must return the correct
        production time for a given food processing building and recipe index.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        mockBuildingDict = {'recipes': [{'production_time': 0.52}]}
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGet.return_value = mockBuildingDict
            productionTime = self.uut.getFoodProcessingProductionTime(
                buildingName, 0)
            mockedGet.assert_called_once_with(buildingName)
            self.assertEqual(0.52, productionTime)

    def test_getFoodProcessingOutputQuantityValueError(self) -> None:
        """
        The getFoodProcessingOutputQuantity method must raise a ValueError
        when the requested food processing building is not found (via
        _getFoodProcessing).
        """
        buildingName = FoodProcessingBuildingName.COFFEE_BREWERY
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGet.side_effect = ValueError(
                f"Food processing building '{buildingName.value}' not found.")
            self.uut.getFoodProcessingOutputQuantity(buildingName, 0)
            mockedGet.assert_called_once_with(buildingName)
        self.assertEqual(f"Food processing building '{buildingName.value}' "
                         f"not found.",
                         str(context.exception))

    def test_getFoodProcessingOutputQuantitySuccess(self) -> None:
        """
        The getFoodProcessingOutputQuantity method must return the correct
        output quantity for a given food processing building and recipe index.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        mockBuildingDict = {'recipes': [{'output_quantity': 4}]}
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGet.return_value = mockBuildingDict
            outputQuantity = self.uut.getFoodProcessingOutputQuantity(
                buildingName, 0)
            mockedGet.assert_called_once_with(buildingName)
            self.assertEqual(4, outputQuantity)

    def test_getFoodProcessingRecipeIndexBuildingNotFound(self) -> None:
        """
        The getFoodProcessingRecipeIndex method must raise a ValueError when
        the requested food processing building is not found (via
        _getFoodProcessing).
        """
        buildingName = FoodProcessingBuildingName.COFFEE_BREWERY
        recipeName = FoodRecipeName.GRILLED_POTATOES
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGet.side_effect = ValueError(
                f"Food processing building '{buildingName.value}' not found.")
            self.uut.getFoodProcessingRecipeIndex(buildingName, recipeName)
            mockedGet.assert_called_once_with(buildingName)
        self.assertEqual(f"Food processing building '{buildingName.value}' "
                         f"not found.",
                         str(context.exception))

    def test_getFoodProcessingRecipeIndexRecipeNotFound(self) -> None:
        """
        The getFoodProcessingRecipeIndex method must raise a ValueError when
        the requested recipe is not found.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        recipeName = FoodRecipeName.GRILLED_POTATOES
        mockBuildingDict = {
            'recipes': [
                {'name': 'Grilled Chestnuts'},
                {'name': 'Grilled Spadderdocks'}
            ]
        }
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGet.return_value = mockBuildingDict
            self.uut.getFoodProcessingRecipeIndex(buildingName, recipeName)
            mockedGet.assert_called_once_with(buildingName)
        self.assertEqual(f"Recipe '{recipeName.value}' not found in "
                         f"'{buildingName.value}'.",
                         str(context.exception))

    def test_getFoodProcessingRecipeIndexSuccess(self) -> None:
        """
        The getFoodProcessingRecipeIndex method must return the correct recipe
        index for a given food processing building and recipe name.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        recipeName = FoodRecipeName.GRILLED_POTATOES
        mockBuildingDict = {
            'recipes': [
                {'name': 'Grilled Potatoes'},
                {'name': 'Grilled Chestnuts'},
                {'name': 'Grilled Spadderdocks'}
            ]
        }
        with patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGet.return_value = mockBuildingDict
            recipeIndex = self.uut.getFoodProcessingRecipeIndex(
                buildingName, recipeName)
            mockedGet.assert_called_once_with(buildingName)
            self.assertEqual(0, recipeIndex)

    def test_getFoodProcessingInputIndexRecipeNotFound(self) -> None:
        """
        The getFoodProcessingInputIndex method must raise a ValueError when
        the recipe is not found (via getFoodProcessingRecipeIndex).
        """
        buildingName = FoodProcessingBuildingName.GRILL
        recipeName = FoodRecipeName.GRILLED_POTATOES
        inputName = "Potatoes"
        with patch.object(self.uut, 'getFoodProcessingRecipeIndex') \
                as mockedGet, self.assertRaises(ValueError) as context:
            mockedGet.side_effect = ValueError(
                f"Recipe '{recipeName.value}' not found in "
                f"'{buildingName.value}'.")
            self.uut.getFoodProcessingInputIndex(buildingName, recipeName,
                                                 inputName)
            mockedGet.assert_called_once_with(buildingName, recipeName)
        self.assertEqual(f"Recipe '{recipeName.value}' not found in "
                         f"'{buildingName.value}'.",
                         str(context.exception))

    def test_getFoodProcessingInputIndexNoInputs(self) -> None:
        """
        The getFoodProcessingInputIndex method must raise a ValueError when
        the recipe has no inputs.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        recipeName = FoodRecipeName.GRILLED_POTATOES
        inputName = "Potatoes"
        mockBuildingDict = {
            'recipes': [
                {'name': 'Grilled Potatoes', 'inputs': None}
            ]
        }
        with patch.object(self.uut, 'getFoodProcessingRecipeIndex') \
                as mockedGetRecipe, \
                patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGetRecipe.return_value = 0
            mockedGet.return_value = mockBuildingDict
            self.uut.getFoodProcessingInputIndex(buildingName, recipeName,
                                                 inputName)
        self.assertEqual(f"Recipe '{recipeName.value}' in "
                         f"'{buildingName.value}' has no inputs.",
                         str(context.exception))

    def test_getFoodProcessingInputIndexInputNotFound(self) -> None:
        """
        The getFoodProcessingInputIndex method must raise a ValueError when
        the input is not found.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        recipeName = FoodRecipeName.GRILLED_POTATOES
        inputName = "Carrots"
        mockBuildingDict = {
            'recipes': [
                {
                    'name': 'Grilled Potatoes',
                    'inputs': [
                        {'name': 'Potatoes', 'quantity': 1},
                        {'name': 'Logs', 'quantity': 0.1}
                    ]
                }
            ]
        }
        with patch.object(self.uut, 'getFoodProcessingRecipeIndex') \
                as mockedGetRecipe, \
                patch.object(self.uut, '_getFoodProcessing') as mockedGet, \
                self.assertRaises(ValueError) as context:
            mockedGetRecipe.return_value = 0
            mockedGet.return_value = mockBuildingDict
            self.uut.getFoodProcessingInputIndex(buildingName, recipeName,
                                                 inputName)
        self.assertEqual(f"Input '{inputName}' not found in recipe "
                         f"'{recipeName.value}' of '{buildingName.value}'.",
                         str(context.exception))

    def test_getFoodProcessingInputIndexSuccess(self) -> None:
        """
        The getFoodProcessingInputIndex method must return the correct input
        index.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        recipeName = FoodRecipeName.GRILLED_POTATOES
        inputName = "Logs"
        mockBuildingDict = {
            'recipes': [
                {
                    'name': 'Grilled Potatoes',
                    'inputs': [
                        {'name': 'Potatoes', 'quantity': 1},
                        {'name': 'Logs', 'quantity': 0.1}
                    ]
                }
            ]
        }
        with patch.object(self.uut, 'getFoodProcessingRecipeIndex') \
                as mockedGetRecipe, \
                patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGetRecipe.return_value = 0
            mockedGet.return_value = mockBuildingDict
            inputIndex = self.uut.getFoodProcessingInputIndex(
                buildingName, recipeName, inputName)
            self.assertEqual(1, inputIndex)

    def test_getFoodProcessingInputQuantitySuccess(self) -> None:
        """
        The getFoodProcessingInputQuantity method must return the correct
        input quantity.
        """
        buildingName = FoodProcessingBuildingName.GRILL
        recipeName = FoodRecipeName.GRILLED_POTATOES
        inputName = "Potatoes"
        mockBuildingDict = {
            'recipes': [
                {
                    'name': 'Grilled Potatoes',
                    'inputs': [
                        {'name': 'Potatoes', 'quantity': 1},
                        {'name': 'Logs', 'quantity': 0.1}
                    ]
                }
            ]
        }
        with patch.object(self.uut, 'getFoodProcessingInputIndex') \
                as mockedGetInput, \
                patch.object(self.uut, 'getFoodProcessingRecipeIndex') \
                as mockedGetRecipe, \
                patch.object(self.uut, '_getFoodProcessing') as mockedGet:
            mockedGetInput.return_value = 0
            mockedGetRecipe.return_value = 0
            mockedGet.return_value = mockBuildingDict
            quantity = self.uut.getFoodProcessingInputQuantity(
                buildingName, recipeName, inputName)
            self.assertEqual(1, quantity)

    def test_getGoodsValueError(self) -> None:
        """
        The _getGoods method must raise a ValueError when the requested
        goods building is not found in the faction data.
        """
        buildingName = GoodsBuildingName.INDUSTRIAL_LUMBER_MILL
        with self.assertRaises(ValueError) as context:
            self.uut._getGoods(buildingName)
        self.assertEqual(f"Goods building '{buildingName.value}' not found.",
                         str(context.exception))

    def test_getGoodsSuccess(self) -> None:
        """
        The _getGoods method must return the correct goods building dictionary
        for a given goods building name.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        building = self.uut._getGoods(buildingName)
        self.assertEqual('Lumber Mill', building['name'])
        self.assertEqual(1, building['workers'])

    def test_getGoodsWorkersValueError(self) -> None:
        """
        The getGoodsWorkers method must raise a ValueError when the requested
        goods building is not found (via _getGoods).
        """
        buildingName = GoodsBuildingName.INDUSTRIAL_LUMBER_MILL
        with patch.object(self.uut, '_getGoods') as mockedGetGoods, \
                self.assertRaises(ValueError) as context:
            mockedGetGoods.side_effect = ValueError(
                f"Goods building '{buildingName.value}' not found.")
            self.uut.getGoodsWorkers(buildingName)
            mockedGetGoods.assert_called_once_with(buildingName)
        self.assertEqual(f"Goods building '{buildingName.value}' not found.",
                         str(context.exception))

    def test_getGoodsWorkersSuccess(self) -> None:
        """
        The getGoodsWorkers method must return the correct number of workers
        for a given goods building.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        mockBuildingDict = {'workers': 1}
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            workers = self.uut.getGoodsWorkers(buildingName)
            mockedGetGoods.assert_called_once_with(buildingName)
            self.assertEqual(1, workers)

    def test_getGoodsRecipeCountValueError(self) -> None:
        """
        The getGoodsRecipeCount method must raise a ValueError when the
        requested goods building is not found (via _getGoods).
        """
        buildingName = GoodsBuildingName.INDUSTRIAL_LUMBER_MILL
        with patch.object(self.uut, '_getGoods') as mockedGetGoods, \
                self.assertRaises(ValueError) as context:
            mockedGetGoods.side_effect = ValueError(
                f"Goods building '{buildingName.value}' not found.")
            self.uut.getGoodsRecipeCount(buildingName)
            mockedGetGoods.assert_called_once_with(buildingName)
        self.assertEqual(f"Goods building '{buildingName.value}' not found.",
                         str(context.exception))

    def test_getGoodsRecipeCountSuccess(self) -> None:
        """
        The getGoodsRecipeCount method must return the correct number of
        recipes for a given goods building.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        mockBuildingDict = {'recipes': [{'name': 'Planks'}]}
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            recipeCount = self.uut.getGoodsRecipeCount(buildingName)
            mockedGetGoods.assert_called_once_with(buildingName)
            self.assertEqual(1, recipeCount)

    def test_getGoodsRecipeNameValueError(self) -> None:
        """
        The getGoodsRecipeName method must raise a ValueError when the
        requested goods building is not found (via _getGoods).
        """
        buildingName = GoodsBuildingName.INDUSTRIAL_LUMBER_MILL
        with patch.object(self.uut, '_getGoods') as mockedGetGoods, \
                self.assertRaises(ValueError) as context:
            mockedGetGoods.side_effect = ValueError(
                f"Goods building '{buildingName.value}' not found.")
            self.uut.getGoodsRecipeName(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
        self.assertEqual(f"Goods building '{buildingName.value}' not found.",
                         str(context.exception))

    def test_getGoodsRecipeNameSuccess(self) -> None:
        """
        The getGoodsRecipeName method must return the correct recipe name
        for a given goods building and recipe index.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        mockBuildingDict = {'recipes': [{'name': 'Planks'}]}
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            recipeName = self.uut.getGoodsRecipeName(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
            self.assertEqual('Planks', recipeName)

    def test_getGoodsProductionTimeValueError(self) -> None:
        """
        The getGoodsProductionTime method must raise a ValueError when the
        requested goods building is not found (via _getGoods).
        """
        buildingName = GoodsBuildingName.INDUSTRIAL_LUMBER_MILL
        with patch.object(self.uut, '_getGoods') as mockedGetGoods, \
                self.assertRaises(ValueError) as context:
            mockedGetGoods.side_effect = ValueError(
                f"Goods building '{buildingName.value}' not found.")
            self.uut.getGoodsProductionTime(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
        self.assertEqual(f"Goods building '{buildingName.value}' not found.",
                         str(context.exception))

    def test_getGoodsProductionTimeSuccess(self) -> None:
        """
        The getGoodsProductionTime method must return the correct production
        time for a given goods building and recipe index.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        mockBuildingDict = {'recipes': [{'production_time': 1.3}]}
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            productionTime = self.uut.getGoodsProductionTime(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
            self.assertEqual(1.3, productionTime)

    def test_getGoodsInputsValueError(self) -> None:
        """
        The getGoodsInputs method must raise a ValueError when the requested
        goods building is not found (via _getGoods).
        """
        buildingName = GoodsBuildingName.INDUSTRIAL_LUMBER_MILL
        with patch.object(self.uut, '_getGoods') as mockedGetGoods, \
                self.assertRaises(ValueError) as context:
            mockedGetGoods.side_effect = ValueError(
                f"Goods building '{buildingName.value}' not found.")
            self.uut.getGoodsInputs(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
        self.assertEqual(f"Goods building '{buildingName.value}' not found.",
                         str(context.exception))

    def test_getGoodsInputsSuccess(self) -> None:
        """
        The getGoodsInputs method must return the correct inputs for a given
        goods building and recipe index.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        mockInputs = [{'name': 'Logs', 'quantity': 1}]
        mockBuildingDict = {'recipes': [{'inputs': mockInputs}]}
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            inputs = self.uut.getGoodsInputs(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
            self.assertEqual(mockInputs, inputs)

    def test_getGoodsOutputQuantityValueError(self) -> None:
        """
        The getGoodsOutputQuantity method must raise a ValueError when the
        requested goods building is not found (via _getGoods).
        """
        buildingName = GoodsBuildingName.INDUSTRIAL_LUMBER_MILL
        with patch.object(self.uut, '_getGoods') as mockedGetGoods, \
                self.assertRaises(ValueError) as context:
            mockedGetGoods.side_effect = ValueError(
                f"Goods building '{buildingName.value}' not found.")
            self.uut.getGoodsOutputQuantity(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
        self.assertEqual(f"Goods building '{buildingName.value}' not found.",
                         str(context.exception))

    def test_getGoodsOutputQuantitySuccess(self) -> None:
        """
        The getGoodsOutputQuantity method must return the correct output
        quantity for a given goods building and recipe index.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        mockBuildingDict = {'recipes': [{'output_quantity': 1}]}
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            outputQuantity = self.uut.getGoodsOutputQuantity(buildingName, 0)
            mockedGetGoods.assert_called_once_with(buildingName)
            self.assertEqual(1, outputQuantity)

    def test_getGoodsRecipeIndexRecipeNotFound(self) -> None:
        """
        The getGoodsRecipeIndex method must raise ValueError if the
        specified recipe is not found in the building.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        recipeName = GoodsRecipeName.GEARS
        mockBuildingDict = {
            'recipes': [
                {'name': 'Planks'},
                {'name': 'Paper'}
            ]
        }
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            with self.assertRaises(ValueError) as context:
                self.uut.getGoodsRecipeIndex(buildingName, recipeName)
            self.assertEqual(
                "Recipe 'Gears' not found in building 'Lumber Mill'.",
                str(context.exception))

    def test_getGoodsRecipeIndexSuccess(self) -> None:
        """
        The getGoodsRecipeIndex method must return the correct recipe index
        for a given goods building and recipe name.
        """
        buildingName = GoodsBuildingName.PRINTING_PRESS
        recipeName = GoodsRecipeName.PUNCHCARDS
        mockBuildingDict = {
            'recipes': [
                {'name': 'Books'},
                {'name': 'Punchcards'}
            ]
        }
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            recipeIndex = self.uut.getGoodsRecipeIndex(buildingName,
                                                       recipeName)
            mockedGetGoods.assert_called_once_with(buildingName)
            self.assertEqual(1, recipeIndex)

    def test_getGoodsInputQuantityNoInputs(self) -> None:
        """
        The getGoodsInputQuantity method must raise ValueError if the
        recipe has no inputs.
        """
        buildingName = GoodsBuildingName.LUMBER_MILL
        recipeName = GoodsRecipeName.PLANKS
        inputName = "Logs"
        mockBuildingDict = {
            'recipes': [
                {'name': 'Planks', 'inputs': None}
            ]
        }
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            with self.assertRaises(ValueError) as context:
                self.uut.getGoodsInputQuantity(buildingName, recipeName,
                                               inputName)
            self.assertEqual(
                "Recipe 'Planks' in building 'Lumber Mill' has no inputs.",
                str(context.exception))

    def test_getGoodsInputQuantityInputNotFound(self) -> None:
        """
        The getGoodsInputQuantity method must raise ValueError if the
        specified input is not found in the recipe.
        """
        buildingName = GoodsBuildingName.GEAR_WORKSHOP
        recipeName = GoodsRecipeName.GEARS
        inputName = "Logs"
        mockBuildingDict = {
            'recipes': [
                {
                    'name': 'Gears',
                    'inputs': [
                        {'name': 'Planks', 'quantity': 1}
                    ]
                }
            ]
        }
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            with self.assertRaises(ValueError) as context:
                self.uut.getGoodsInputQuantity(buildingName, recipeName,
                                               inputName)
            self.assertEqual("Input 'Logs' not found in recipe 'Gears' for "
                             "building 'Gear Workshop'.",
                             str(context.exception))

    def test_getGoodsInputQuantitySuccess(self) -> None:
        """
        The getGoodsInputQuantity method must return the correct input
        quantity for a given goods building, recipe, and input name.
        """
        buildingName = GoodsBuildingName.SMELTER
        recipeName = GoodsRecipeName.METAL_BLOCKS
        inputName = "Logs"
        mockBuildingDict = {
            'recipes': [
                {
                    'name': 'Metal Blocks',
                    'inputs': [
                        {'name': 'Scrap Metal', 'quantity': 1},
                        {'name': 'Logs', 'quantity': 0.2}
                    ]
                }
            ]
        }
        with patch.object(self.uut, '_getGoods') as mockedGetGoods:
            mockedGetGoods.return_value = mockBuildingDict
            inputQuantity = self.uut.getGoodsInputQuantity(
                buildingName, recipeName, inputName)
            mockedGetGoods.assert_called_with(buildingName)
            self.assertEqual(0.2, inputQuantity)
