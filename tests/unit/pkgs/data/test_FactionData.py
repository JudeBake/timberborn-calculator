from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import yaml as yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.data.factionData import FactionData                   # noqa: E402
from pkgs.data.emunerators import ConsumptionType, CropName, \
    DifficultyLevel, HarvestName, TreeName                      # noqa: E402


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
