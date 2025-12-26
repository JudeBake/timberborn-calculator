from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.factions.folktail import Folktail                     # noqa: E402
from pkgs.data.enumerators import ConsumptionType               # noqa: E402
from pkgs.data.enumerators import CropName                      # noqa: E402
from pkgs.data.enumerators import DifficultyLevel               # noqa: E402
from pkgs.data.enumerators import FoodProcessingBuildingName    # noqa: E402
from pkgs.data.enumerators import FoodRecipeName                # noqa: E402
from pkgs.data.enumerators import GoodsBuildingName             # noqa: E402
from pkgs.data.enumerators import GoodsRecipeName               # noqa: E402
from pkgs.data.enumerators import HarvestName                   # noqa: E402
from pkgs.data.enumerators import TreeName                      # noqa: E402
from pkgs.data.enumerators import WaterBuildingName             # noqa: E402


class TestFolktail(TestCase):
    """
    Folktail class test cases.
    """

    def setUp(self) -> None:
        with patch('pkgs.factions.folktail.FactionData'):
            self.uut = Folktail()
        self.uut.factionData = Mock()

    def test_constructorFileNotFound(self) -> None:
        """
        The constructor must raise FileNotFoundError if the folktails.yml
        file does not exist.
        """
        errMsg = "File not found."
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData, \
                self.assertRaises(FileNotFoundError) as context:
            MockFactionData.side_effect = FileNotFoundError(errMsg)
            Folktail()
            MockFactionData.assert_called_once_with('./data/folktails.yml')
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorYAMLError(self) -> None:
        """
        The constructor must raise any YAML parsing errors from FactionData.
        """
        import yaml
        errMsg = "YAML parsing error."
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData, \
                self.assertRaises(yaml.YAMLError) as context:
            MockFactionData.side_effect = yaml.YAMLError(errMsg)
            Folktail()
            MockFactionData.assert_called_once_with('./data/folktails.yml')
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorSuccess(self) -> None:
        """
        The constructor must successfully instantiate FactionData with the
        folktails.yml file.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()

            MockFactionData.assert_called_once_with('./data/folktails.yml')
            self.assertEqual(mockFactionDataInstance, folktail.factionData)

    def test_getDailyFoodConsumptionNegativePopulation(self) -> None:
        """
        The getDailyFoodConsumption method must raise ValueError if
        population is negative.
        """
        errMsg = "Population cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getDailyFoodConsumption(-1, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDailyFoodConsumptionSuccess(self) -> None:
        """
        The getDailyFoodConsumption method must correctly calculate daily
        food consumption based on population and difficulty.
        """
        self.uut.factionData.getConsumption.return_value = 2.75
        self.uut.factionData.getDifficultyModifier.return_value = 1.0

        result = self.uut.getDailyFoodConsumption(100, DifficultyLevel.NORMAL)

        self.assertEqual(275.0, result)
        self.uut.factionData.getConsumption \
            .assert_called_once_with(ConsumptionType.FOOD)
        self.uut.factionData.getDifficultyModifier \
            .assert_called_once_with(DifficultyLevel.NORMAL)

    def test_getDailyWaterConsumptionNegativePopulation(self) -> None:
        """
        The getDailyWaterConsumption method must raise ValueError if
        population is negative.
        """
        errMsg = "Population cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getDailyWaterConsumption(-1, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDailyWaterConsumptionSuccess(self) -> None:
        """
        The getDailyWaterConsumption method must correctly calculate daily
        water consumption based on population and difficulty.
        """
        self.uut.factionData.getConsumption.return_value = 2.25
        self.uut.factionData.getDifficultyModifier.return_value = 1.0

        result = self.uut.getDailyWaterConsumption(100, DifficultyLevel.NORMAL)

        self.assertEqual(225.0, result)
        self.uut.factionData.getConsumption \
            .assert_called_once_with(ConsumptionType.WATER)
        self.uut.factionData.getDifficultyModifier \
            .assert_called_once_with(DifficultyLevel.NORMAL)

    def test_getFoodPerTypeNegativePopulation(self) -> None:
        """
        The getFoodPerType method must raise ValueError if population is
        negative.
        """
        errMsg = "Population cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodPerType(-1, 5, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodPerTypeZeroFoodTypeCount(self) -> None:
        """
        The getFoodPerType method must raise ValueError if foodTypeCount is
        zero.
        """
        errMsg = "Food type count must be positive."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodPerType(100, 0, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodPerTypeNegativeFoodTypeCount(self) -> None:
        """
        The getFoodPerType method must raise ValueError if foodTypeCount is
        negative.
        """
        errMsg = "Food type count must be positive."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodPerType(100, -5, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodPerTypeSuccess(self) -> None:
        """
        The getFoodPerType method must correctly calculate food per type by
        dividing total food consumption by the number of food types.
        """
        self.uut.factionData.getConsumption.return_value = 2.75
        self.uut.factionData.getDifficultyModifier.return_value = 1.0

        result = self.uut.getFoodPerType(100, 5, DifficultyLevel.NORMAL)

        # 100 * 2.75 * 1.0 = 275.0 / 5 = ceil(55.0) = 55
        self.assertEqual(55, result)
        self.uut.factionData.getConsumption \
            .assert_called_once_with(ConsumptionType.FOOD)
        self.uut.factionData.getDifficultyModifier \
            .assert_called_once_with(DifficultyLevel.NORMAL)

    def test_getBerryTilesNeededNegativeAmount(self) -> None:
        """
        The getBerryTilesNeeded method must raise ValueError if berry
        amount is negative.
        """
        errMsg = "Berry amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBerryTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBerryTilesNeededSuccess(self) -> None:
        """
        The getBerryTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 12
        self.uut.factionData.getCropHarvestYield.return_value = 3

        result = self.uut.getBerryTilesNeeded(30.0)

        # Production per tile = 3 / 12 = 0.25
        # Tiles needed = ceil(30.0 / 0.25) = 120
        self.assertEqual(120, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.BERRY_BUSH)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.BERRY_BUSH)

    def test_getDandelionTilesNeededNegativeAmount(self) -> None:
        """
        The getDandelionTilesNeeded method must raise ValueError if dandelion
        amount is negative.
        """
        errMsg = "Dandelion amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getDandelionTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDandelionTilesNeededSuccess(self) -> None:
        """
        The getDandelionTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 3
        self.uut.factionData.getCropHarvestYield.return_value = 1

        result = self.uut.getDandelionTilesNeeded(10.0)

        # Production per tile = 1 / 3 = 0.333...
        # Tiles needed = ceil(10.0 / 0.333...) = ceil(30) = 30
        self.assertEqual(30, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.DANDELION_BUSH)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.DANDELION_BUSH)

    def test_getCarrotTilesNeededNegativeAmount(self) -> None:
        """
        The getCarrotTilesNeeded method must raise ValueError if carrot
        amount is negative.
        """
        errMsg = "Carrot amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCarrotTilesNeeded(-10.0, False)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCarrotTilesNeededWithoutBeehive(self) -> None:
        """
        The getCarrotTilesNeeded method must correctly calculate tiles
        needed without beehive modifier.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 4
        self.uut.factionData.getCropHarvestYield.return_value = 3

        result = self.uut.getCarrotTilesNeeded(30.0, False)

        # Production per tile = 3 / 4 = 0.75
        # Tiles needed = ceil(30.0 / 0.75) = 40
        self.assertEqual(40, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.CARROT_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.CARROT_CROP)

    def test_getCarrotTilesNeededWithBeehive(self) -> None:
        """
        The getCarrotTilesNeeded method must correctly calculate tiles
        needed with beehive modifier applied.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 4
        self.uut.factionData.getCropHarvestYield.return_value = 3
        self.uut.factionData.getBeehiveModifier.return_value = 1.43

        result = self.uut.getCarrotTilesNeeded(30.0, True)

        # Production per tile = 3 / 4 = 0.75
        # With beehive = 0.75 * 1.43 = 1.0725
        # Tiles needed = ceil(30.0 / 1.0725) = ceil(27.972...) = 28
        self.assertEqual(28, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.CARROT_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.CARROT_CROP)
        self.uut.factionData.getBeehiveModifier.assert_called_once()

    def test_getSunflowerTilesNeededNegativeAmount(self) -> None:
        """
        The getSunflowerTilesNeeded method must raise ValueError if
        sunflower seed amount is negative.
        """
        errMsg = "Sunflower seed amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getSunflowerTilesNeeded(-10.0, False)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSunflowerTilesNeededWithoutBeehive(self) -> None:
        """
        The getSunflowerTilesNeeded method must correctly calculate tiles
        needed without beehive modifier.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 5
        self.uut.factionData.getCropHarvestYield.return_value = 2

        result = self.uut.getSunflowerTilesNeeded(20.0, False)

        # Production per tile = 2 / 5 = 0.4
        # Tiles needed = ceil(20.0 / 0.4) = 50
        self.assertEqual(50, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.SUNFLOWER_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.SUNFLOWER_CROP)

    def test_getSunflowerTilesNeededWithBeehive(self) -> None:
        """
        The getSunflowerTilesNeeded method must correctly calculate tiles
        needed with beehive modifier applied.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 5
        self.uut.factionData.getCropHarvestYield.return_value = 2
        self.uut.factionData.getBeehiveModifier.return_value = 1.43

        result = self.uut.getSunflowerTilesNeeded(20.0, True)

        # Production per tile = 2 / 5 = 0.4
        # With beehive = 0.4 * 1.43 = 0.572
        # Tiles needed = ceil(20.0 / 0.572) = ceil(34.965...) = 35
        self.assertEqual(35, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.SUNFLOWER_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.SUNFLOWER_CROP)
        self.uut.factionData.getBeehiveModifier.assert_called_once()

    def test_getPotatoTilesNeededNegativeAmount(self) -> None:
        """
        The getPotatoTilesNeeded method must raise ValueError if potato
        amount is negative.
        """
        errMsg = "Potato amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPotatoTilesNeeded(-10.0, False)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPotatoTilesNeededWithoutBeehive(self) -> None:
        """
        The getPotatoTilesNeeded method must correctly calculate tiles
        needed without beehive modifier.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 6
        self.uut.factionData.getCropHarvestYield.return_value = 1

        result = self.uut.getPotatoTilesNeeded(30.0, False)

        # Production per tile = 1 / 6 = 0.16666...
        # Tiles needed = ceil(30.0 / 0.16666...) = 180
        self.assertEqual(180, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.POTATO_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.POTATO_CROP)

    def test_getPotatoTilesNeededWithBeehive(self) -> None:
        """
        The getPotatoTilesNeeded method must correctly calculate tiles
        needed with beehive modifier applied.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 6
        self.uut.factionData.getCropHarvestYield.return_value = 1
        self.uut.factionData.getBeehiveModifier.return_value = 1.43

        result = self.uut.getPotatoTilesNeeded(30.0, True)

        # Production per tile = 1 / 6 = 0.16666...
        # With beehive = 0.16666... * 1.43 = 0.238333...
        # Tiles needed = ceil(30.0 / 0.238333...) = ceil(125.874...) = 126
        self.assertEqual(126, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.POTATO_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.POTATO_CROP)
        self.uut.factionData.getBeehiveModifier.assert_called_once()

    def test_getWheatTilesNeededNegativeAmount(self) -> None:
        """
        The getWheatTilesNeeded method must raise ValueError if wheat
        amount is negative.
        """
        errMsg = "Wheat amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWheatTilesNeeded(-10.0, False)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWheatTilesNeededWithoutBeehive(self) -> None:
        """
        The getWheatTilesNeeded method must correctly calculate tiles
        needed without beehive.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 10
        self.uut.factionData.getCropHarvestYield.return_value = 3

        result = self.uut.getWheatTilesNeeded(30.0, False)

        # Production per tile = 3 / 10 = 0.3
        # Tiles needed = ceil(30.0 / 0.3) = 100
        self.assertEqual(100, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.WHEAT_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.WHEAT_CROP)

    def test_getWheatTilesNeededWithBeehive(self) -> None:
        """
        The getWheatTilesNeeded method must correctly calculate tiles
        needed with beehive.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 10
        self.uut.factionData.getCropHarvestYield.return_value = 3
        self.uut.factionData.getBeehiveModifier.return_value = 1.43

        result = self.uut.getWheatTilesNeeded(30.0, True)

        # Production per tile = 3 / 10 = 0.3
        # With beehive = 0.3 * 1.43 = 0.429
        # Tiles needed = ceil(30.0 / 0.429) = ceil(69.930...) = 70
        self.assertEqual(70, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.WHEAT_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.WHEAT_CROP)
        self.uut.factionData.getBeehiveModifier.assert_called_once()

    def test_getCattailTilesNeededNegativeAmount(self) -> None:
        """
        The getCattailTilesNeeded method must raise ValueError if cattail
        root amount is negative.
        """
        errMsg = "Cattail root amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCattailTilesNeeded(-10.0, False)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCattailTilesNeededWithoutBeehive(self) -> None:
        """
        The getCattailTilesNeeded method must correctly calculate tiles
        needed without beehive.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 8
        self.uut.factionData.getCropHarvestYield.return_value = 3

        result = self.uut.getCattailTilesNeeded(30.0, False)

        # Production per tile = 3 / 8 = 0.375
        # Tiles needed = ceil(30.0 / 0.375) = 80
        self.assertEqual(80, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.CATTAIL_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.CATTAIL_CROP)

    def test_getCattailTilesNeededWithBeehive(self) -> None:
        """
        The getCattailTilesNeeded method must correctly calculate tiles
        needed with beehive.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 8
        self.uut.factionData.getCropHarvestYield.return_value = 3
        self.uut.factionData.getBeehiveModifier.return_value = 1.43

        result = self.uut.getCattailTilesNeeded(30.0, True)

        # Production per tile = 3 / 8 = 0.375
        # With beehive = 0.375 * 1.43 = 0.53625
        # Tiles needed = ceil(30.0 / 0.53625) = ceil(55.944...) = 56
        self.assertEqual(56, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.CATTAIL_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.CATTAIL_CROP)
        self.uut.factionData.getBeehiveModifier.assert_called_once()

    def test_getSpadderdockTilesNeededNegativeAmount(self) -> None:
        """
        The getSpadderdockTilesNeeded method must raise ValueError if
        spadderdock amount is negative.
        """
        errMsg = "Spadderdock amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getSpadderdockTilesNeeded(-10.0, False)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSpadderdockTilesNeededWithoutBeehive(self) -> None:
        """
        The getSpadderdockTilesNeeded method must correctly calculate tiles
        needed without beehive.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 12
        self.uut.factionData.getCropHarvestYield.return_value = 3

        result = self.uut.getSpadderdockTilesNeeded(30.0, False)

        # Production per tile = 3 / 12 = 0.25
        # Tiles needed = ceil(30.0 / 0.25) = 120
        self.assertEqual(120, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.SPADDERDOCK_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.SPADDERDOCK_CROP)

    def test_getSpadderdockTilesNeededWithBeehive(self) -> None:
        """
        The getSpadderdockTilesNeeded method must correctly calculate tiles
        needed with beehive.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 12
        self.uut.factionData.getCropHarvestYield.return_value = 3
        self.uut.factionData.getBeehiveModifier.return_value = 1.43

        result = self.uut.getSpadderdockTilesNeeded(30.0, True)

        # Production per tile = 3 / 12 = 0.25
        # With beehive = 0.25 * 1.43 = 0.3575
        # Tiles needed = ceil(30.0 / 0.3575) = ceil(83.916...) = 84
        self.assertEqual(84, result)
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.SPADDERDOCK_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.SPADDERDOCK_CROP)
        self.uut.factionData.getBeehiveModifier.assert_called_once()

    def test_getLogPerTypeNegativeTotalLogAmount(self) -> None:
        """
        The getLogPerType method must raise ValueError if total log amount
        is negative.
        """
        errMsg = "Total log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogPerType(-100.0, 3)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogPerTypeZeroTreeTypeCount(self) -> None:
        """
        The getLogPerType method must raise ValueError if tree type count
        is zero.
        """
        errMsg = "Tree type count must be positive."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogPerType(100.0, 0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogPerTypeNegativeTreeTypeCount(self) -> None:
        """
        The getLogPerType method must raise ValueError if tree type count
        is negative.
        """
        errMsg = "Tree type count must be positive."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogPerType(100.0, -3)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogPerTypeSuccess(self) -> None:
        """
        The getLogPerType method must correctly calculate logs per tree type
        by dividing total log amount by the number of tree types.
        """
        with patch('pkgs.factions.folktail.FactionData'):
            result = self.uut.getLogPerType(100.0, 3)

            # Logs per type = ceil(100.0 / 3) = ceil(33.333...) = 34
            self.assertEqual(34, result)

    def test_getBirchLogTilesNeededNegativeAmount(self) -> None:
        """
        The getBirchLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        errMsg = "Log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBirchLogTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBirchLogTilesNeededSuccess(self) -> None:
        """
        The getBirchLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeGrowthTime.return_value = 15
        self.uut.factionData.getTreeLogOutput.return_value = 5

        result = self.uut.getBirchLogTilesNeeded(30.0)

        # Production per tile = 5 / 15 = 0.333...
        # Tiles needed = ceil(30.0 / 0.333...) = ceil(90.0) = 90
        self.assertEqual(90, result)
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.BIRCH)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.BIRCH)

    def test_getPineLogTilesNeededNegativeAmount(self) -> None:
        """
        The getPineLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        errMsg = "Log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPineLogTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPineLogTilesNeededSuccess(self) -> None:
        """
        The getPineLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeGrowthTime.return_value = 12
        self.uut.factionData.getTreeLogOutput.return_value = 4

        result = self.uut.getPineLogTilesNeeded(30.0)

        # Production per tile = 4 / 12 = 0.333...
        # Tiles needed = ceil(30.0 / 0.333...) = ceil(90.0) = 90
        self.assertEqual(90, result)
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.PINE)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.PINE)

    def test_getPineResinTilesNeededNegativeAmount(self) -> None:
        """
        The getPineResinTilesNeeded method must raise ValueError if pine
        resin amount is negative.
        """
        errMsg = "Pine resin amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPineResinTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPineResinTilesNeededSuccess(self) -> None:
        """
        The getPineResinTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeHarvestTime.return_value = 8
        self.uut.factionData.getTreeHarvestYield.return_value = 2

        result = self.uut.getPineResinTilesNeeded(30.0)

        # Production per tile = 2 / 8 = 0.25
        # Tiles needed = ceil(30.0 / 0.25) = 120
        self.assertEqual(120, result)
        self.uut.factionData.getTreeHarvestTime \
            .assert_called_once_with(TreeName.PINE)
        self.uut.factionData.getTreeHarvestYield \
            .assert_called_once_with(TreeName.PINE)

    def test_getMapleLogTilesNeededNegativeAmount(self) -> None:
        """
        The getMapleLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        errMsg = "Log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMapleLogTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMapleLogTilesNeededSuccess(self) -> None:
        """
        The getMapleLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeGrowthTime.return_value = 18
        self.uut.factionData.getTreeLogOutput.return_value = 6

        result = self.uut.getMapleLogTilesNeeded(30.0)

        # Production per tile = 6 / 18 = 0.333...
        # Tiles needed = ceil(30.0 / 0.333...) = ceil(90.0) = 90
        self.assertEqual(90, result)
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.MAPLE)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.MAPLE)

    def test_getMapleSyrupTilesNeededNegativeAmount(self) -> None:
        """
        The getMapleSyrupTilesNeeded method must raise ValueError if maple
        syrup amount is negative.
        """
        errMsg = "Maple syrup amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMapleSyrupTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMapleSyrupTilesNeededSuccess(self) -> None:
        """
        The getMapleSyrupTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeHarvestTime.return_value = 10
        self.uut.factionData.getTreeHarvestYield.return_value = 2

        result = self.uut.getMapleSyrupTilesNeeded(30.0)

        # Production per tile = 2 / 10 = 0.2
        # Tiles needed = ceil(30.0 / 0.2) = 150
        self.assertEqual(150, result)
        self.uut.factionData.getTreeHarvestTime \
            .assert_called_once_with(TreeName.MAPLE)
        self.uut.factionData.getTreeHarvestYield \
            .assert_called_once_with(TreeName.MAPLE)

    def test_getChestnutLogTilesNeededNegativeAmount(self) -> None:
        """
        The getChestnutLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        errMsg = "Log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getChestnutLogTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getChestnutLogTilesNeededSuccess(self) -> None:
        """
        The getChestnutLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeGrowthTime.return_value = 20
        self.uut.factionData.getTreeLogOutput.return_value = 5

        result = self.uut.getChestnutLogTilesNeeded(30.0)

        # Production per tile = 5 / 20 = 0.25
        # Tiles needed = ceil(30.0 / 0.25) = 120
        self.assertEqual(120, result)
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.CHESTNUT_TREE)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.CHESTNUT_TREE)

    def test_getChestnutTilesNeededNegativeAmount(self) -> None:
        """
        The getChestnutTilesNeeded method must raise ValueError if chestnut
        amount is negative.
        """
        errMsg = "Chestnut amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getChestnutTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getChestnutTilesNeededSuccess(self) -> None:
        """
        The getChestnutTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeHarvestTime.return_value = 8
        self.uut.factionData.getTreeHarvestYield.return_value = 3

        result = self.uut.getChestnutTilesNeeded(30.0)

        # Production per tile = 3 / 8 = 0.375
        # Tiles needed = ceil(30.0 / 0.375) = 80
        self.assertEqual(80, result)
        self.uut.factionData.getTreeHarvestTime \
            .assert_called_once_with(TreeName.CHESTNUT_TREE)
        self.uut.factionData.getTreeHarvestYield \
            .assert_called_once_with(TreeName.CHESTNUT_TREE)

    def test_getOakLogTilesNeededNegativeAmount(self) -> None:
        """
        The getOakLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        errMsg = "Log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getOakLogTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getOakLogTilesNeededSuccess(self) -> None:
        """
        The getOakLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeGrowthTime.return_value = 25
        self.uut.factionData.getTreeLogOutput.return_value = 8

        result = self.uut.getOakLogTilesNeeded(30.0)

        # Production per tile = 8 / 25 = 0.32
        # Tiles needed = ceil(30.0 / 0.32) = ceil(93.75) = 94
        self.assertEqual(94, result)
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.OAK)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.OAK)

    def test_getWaterPumpsNeededNegativeAmount(self) -> None:
        """
        The getWaterPumpsNeeded method must raise ValueError if water
        amount is negative.
        """
        errMsg = "Water amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWaterPumpsNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWaterPumpsNeededSuccess(self) -> None:
        """
        The getWaterPumpsNeeded method must correctly calculate water pumps
        needed.
        """
        self.uut.factionData.getWaterProductionTime.return_value = 2.0
        self.uut.factionData.getWaterOutputQuantity.return_value = 24

        result = self.uut.getWaterPumpsNeeded(50.0)

        # Production per pump per day = (24 / 2.0) * 24 = 288.0
        # Pumps needed = ceil(50.0 / 288.0) = ceil(0.173...) = 1
        self.assertEqual(1, result)
        self.uut.factionData.getWaterProductionTime \
            .assert_called_once_with(WaterBuildingName.WATER_PUMP)
        self.uut.factionData.getWaterOutputQuantity \
            .assert_called_once_with(WaterBuildingName.WATER_PUMP)

    def test_getLargeWaterPumpsNeededNegativeWaterAmount(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must raise ValueError if water
        amount is negative.
        """
        errMsg = "Water amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLargeWaterPumpsNeeded(-10.0, 2)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLargeWaterPumpsNeededNegativeWorkersCount(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must raise ValueError if workers
        count is negative.
        """
        errMsg = "Workers count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLargeWaterPumpsNeeded(50.0, -1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLargeWaterPumpsNeededExceedsMaxWorkers(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must raise ValueError if workers
        count exceeds maximum.
        """
        self.uut.factionData.getWaterWorkers.return_value = 2

        errMsg = "Workers count cannot exceed 2."
        with self.assertRaises(ValueError) as context:
            self.uut.getLargeWaterPumpsNeeded(50.0, 5)
        self.assertEqual(errMsg, str(context.exception))
        self.uut.factionData.getWaterWorkers \
            .assert_called_once_with(WaterBuildingName.LARGE_WATER_PUMP)

    def test_getLargeWaterPumpsNeededSuccessFullWorkers(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must correctly calculate pumps
        needed with full workers.
        """
        self.uut.factionData.getWaterWorkers.return_value = 2
        self.uut.factionData.getWaterProductionTime.return_value = 2.0
        self.uut.factionData.getWaterOutputQuantity.return_value = 48

        result = self.uut.getLargeWaterPumpsNeeded(50.0, 2)

        # Effective output = 48 * (2 / 2) = 48
        # Production per pump per day = (48 / 2.0) * 24 = 576.0
        # Pumps needed = ceil(50.0 / 576.0) = ceil(0.086...) = 1
        self.assertEqual(1, result)
        self.uut.factionData.getWaterWorkers \
            .assert_called_once_with(WaterBuildingName.LARGE_WATER_PUMP)
        self.uut.factionData.getWaterProductionTime \
            .assert_called_once_with(WaterBuildingName.LARGE_WATER_PUMP)
        self.uut.factionData.getWaterOutputQuantity \
            .assert_called_once_with(WaterBuildingName.LARGE_WATER_PUMP)

    def test_getLargeWaterPumpsNeededSuccessReducedWorkers(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must correctly calculate pumps
        needed with reduced workers.
        """
        self.uut.factionData.getWaterWorkers.return_value = 2
        self.uut.factionData.getWaterProductionTime.return_value = 2.0
        self.uut.factionData.getWaterOutputQuantity.return_value = 48

        result = self.uut.getLargeWaterPumpsNeeded(50.0, 1)

        # Effective output = 48 * (1 / 2) = 24
        # Production per pump per day = (24 / 2.0) * 24 = 288.0
        # Pumps needed = ceil(50.0 / 288.0) = ceil(0.173...) = 1
        self.assertEqual(1, result)
        self.uut.factionData.getWaterWorkers \
            .assert_called_once_with(WaterBuildingName.LARGE_WATER_PUMP)
        self.uut.factionData.getWaterProductionTime \
            .assert_called_once_with(WaterBuildingName.LARGE_WATER_PUMP)
        self.uut.factionData.getWaterOutputQuantity \
            .assert_called_once_with(WaterBuildingName.LARGE_WATER_PUMP)

    def test_getBadwaterPumpsNeededNegativeAmount(self) -> None:
        """
        The getBadwaterPumpsNeeded method must raise ValueError if water
        amount is negative.
        """
        errMsg = "Water amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBadwaterPumpsNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBadwaterPumpsNeededSuccess(self) -> None:
        """
        The getBadwaterPumpsNeeded method must correctly calculate badwater
        pumps needed.
        """
        self.uut.factionData.getWaterProductionTime.return_value = 3.0
        self.uut.factionData.getWaterOutputQuantity.return_value = 18

        result = self.uut.getBadwaterPumpsNeeded(40.0)

        # Production per pump per day = (18 / 3.0) * 24 = 144.0
        # Pumps needed = ceil(40.0 / 144.0) = ceil(0.277...) = 1
        self.assertEqual(1, result)
        self.uut.factionData.getWaterProductionTime \
            .assert_called_once_with(WaterBuildingName.BADWATER_PUMP)
        self.uut.factionData.getWaterOutputQuantity \
            .assert_called_once_with(WaterBuildingName.BADWATER_PUMP)

    def test_getGrillsNeededForPotatoesNegativeAmount(self) -> None:
        """
        The getGrillsNeededForPotatoes method must raise ValueError if
        grilled potato amount is negative.
        """
        errMsg = "Grilled potato amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGrillsNeededForPotatoes(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGrillsNeededForPotatoesSuccess(self) -> None:
        """
        The getGrillsNeededForPotatoes method must correctly calculate grills
        needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.52
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 4

        result = self.uut.getGrillsNeededForPotatoes(200.0)

        # Production per grill per day = (4 / 0.52) * 24 = 184.615...
        # Grills needed = ceil(200.0 / 184.615...) = ceil(1.083...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_POTATOES
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                0
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                0
            )

    def test_getPotatoesNeededForGrilledPotatoesProductionNegativeCount(self) -> None:
        """
        The getPotatoesNeededForGrilledPotatoesProduction method must raise ValueError if
        grills count is negative.
        """
        errMsg = "Grills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPotatoesNeededForGrilledPotatoesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPotatoesNeededForGrilledPotatoesProductionSuccess(self) -> None:
        """
        The getPotatoesNeededForGrilledPotatoesProduction method must correctly calculate
        potatoes needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.52
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getPotatoesNeededForGrilledPotatoesProduction(3)

        # Cycles per day = 24 / 0.52 = 46.153...
        # Potatoes per grill per day = 1 * 46.153... = 46.153...
        # Total potatoes = 3 * 46.153... = 138.461...
        # Ceiling = 139
        self.assertEqual(139, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_POTATOES
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                0
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_POTATOES,
                HarvestName.POTATOES
            )

    def test_getLogsNeededForGrilledPotatoesProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForGrilledPotatoesProduction method must raise ValueError
        if grills count is negative.
        """
        errMsg = "Grills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForGrilledPotatoesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForGrilledPotatoesProductionSuccess(self) -> None:
        """
        The getLogsNeededForGrilledPotatoesProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.52
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForGrilledPotatoesProduction(3)

        # Cycles per day = 24 / 0.52 = 46.153...
        # Logs per grill per day = 0.1 * 46.153... = 4.615...
        # Total logs = 3 * 4.615... = 13.846...
        self.assertAlmostEqual(13.846153846153847, result, places=10)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_POTATOES
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                0
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_POTATOES,
                HarvestName.LOGS
            )

    def test_getGrillsNeededForChestnutsNegativeAmount(self) -> None:
        """
        The getGrillsNeededForChestnuts method must raise ValueError if
        grilled chestnut amount is negative.
        """
        errMsg = "Grilled chestnut amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGrillsNeededForChestnuts(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGrillsNeededForChestnutsSuccess(self) -> None:
        """
        The getGrillsNeededForChestnuts method must correctly calculate
        grills needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.33
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 5

        result = self.uut.getGrillsNeededForChestnuts(400.0)

        # Production per grill per day = (5 / 0.33) * 24 = 363.636...
        # Grills needed = ceil(400.0 / 363.636...) = ceil(1.1) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_CHESTNUTS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                1
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                1
            )

    def test_getChestnutsNeededForGrilledChestnutsProductionNegativeCount(self) -> None:
        """
        The getChestnutsNeededForGrilledChestnutsProduction method must raise ValueError if
        grills count is negative.
        """
        errMsg = "Grills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getChestnutsNeededForGrilledChestnutsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getChestnutsNeededForGrilledChestnutsProductionSuccess(self) -> None:
        """
        The getChestnutsNeededForGrilledChestnutsProduction method must correctly calculate
        chestnuts needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.33
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getChestnutsNeededForGrilledChestnutsProduction(3)

        # Cycles per day = 24 / 0.33 = 72.727...
        # Chestnuts per grill per day = 1 * 72.727... = 72.727...
        # Total chestnuts = 3 * 72.727... = 218.181...
        # Ceiling = 219
        self.assertEqual(219, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_CHESTNUTS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                1
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_CHESTNUTS,
                HarvestName.CHESTNUTS
            )

    def test_getLogsNeededForGrilledChestnutsProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForGrilledChestnutsProduction method must raise ValueError
        if grills count is negative.
        """
        errMsg = "Grills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForGrilledChestnutsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForGrilledChestnutsProductionSuccess(self) -> None:
        """
        The getLogsNeededForGrilledChestnutsProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.33
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForGrilledChestnutsProduction(3)

        # Cycles per day = 24 / 0.33 = 72.727...
        # Logs per grill per day = 0.1 * 72.727... = 7.272...
        # Total logs = 3 * 7.272... = 21.818...
        self.assertAlmostEqual(21.818181818181817, result, places=10)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_CHESTNUTS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                1
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_CHESTNUTS,
                HarvestName.LOGS
            )

    def test_getGrillsNeededForSpadderdocksNegativeAmount(self) -> None:
        """
        The getGrillsNeededForSpadderdocks method must raise ValueError if
        grilled spadderdock amount is negative.
        """
        errMsg = "Grilled spadderdock amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGrillsNeededForSpadderdocks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGrillsNeededForSpadderdocksSuccess(self) -> None:
        """
        The getGrillsNeededForSpadderdocks method must correctly calculate
        grills needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 3

        result = self.uut.getGrillsNeededForSpadderdocks(300.0)

        # Production per grill per day = (3 / 0.25) * 24 = 288.0
        # Grills needed = ceil(300.0 / 288.0) = ceil(1.041...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_SPADDERDOCKS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                2
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                2
            )

    def test_getSpadderdocksNeededForGrilledSpadderdocksProductionNegativeCount(self) -> None:
        """
        The getSpadderdocksNeededForGrilledSpadderdocksProduction method must raise ValueError if
        grills count is negative.
        """
        errMsg = "Grills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getSpadderdocksNeededForGrilledSpadderdocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSpadderdocksNeededForGrilledSpadderdocksProductionSuccess(self) -> None:
        """
        The getSpadderdocksNeededForGrilledSpadderdocksProduction method must correctly calculate
        spadderdocks needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 2

        result = self.uut.getSpadderdocksNeededForGrilledSpadderdocksProduction(3)

        # Cycles per day = 24 / 0.25 = 96.0
        # Spadderdocks per grill per day = 2 * 96.0 = 192.0
        # Total spadderdocks = 3 * 192.0 = 576.0
        # Ceiling = 576
        self.assertEqual(576, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_SPADDERDOCKS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                2
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_SPADDERDOCKS,
                HarvestName.SPADDERDOCKS
            )

    def test_getLogsNeededForGrilledSpadderdocksProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForGrilledSpadderdocksProduction method must raise
        ValueError if grills count is negative.
        """
        errMsg = "Grills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForGrilledSpadderdocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForGrilledSpadderdocksProductionSuccess(self) -> None:
        """
        The getLogsNeededForGrilledSpadderdocksProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.15

        result = self.uut.getLogsNeededForGrilledSpadderdocksProduction(3)

        # Cycles per day = 24 / 0.25 = 96.0
        # Logs per grill per day = 0.15 * 96.0 = 14.4
        # Total logs = 3 * 14.4 = 43.2
        self.assertAlmostEqual(43.2, result, places=10)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_SPADDERDOCKS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                2
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRILL,
                FoodRecipeName.GRILLED_SPADDERDOCKS,
                HarvestName.LOGS
            )

    def test_getGristmillsNeededForWheatFlourNegativeAmount(self) -> None:
        """
        The getGristmillsNeededForWheatFlour method must raise ValueError if
        wheat flour amount is negative.
        """
        errMsg = "Wheat flour amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGristmillsNeededForWheatFlour(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGristmillsNeededForWheatFlourSuccess(self) -> None:
        """
        The getGristmillsNeededForWheatFlour method must correctly calculate
        gristmills needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 1

        result = self.uut.getGristmillsNeededForWheatFlour(50.0)

        # Production per gristmill per day = (1 / 0.5) * 24 = 48.0
        # Gristmills needed = ceil(50.0 / 48.0) = ceil(1.041...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                FoodRecipeName.WHEAT_FLOUR
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                0
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                0
            )

    def test_getWheatNeededForWheatFlourProductionNegativeCount(self) -> None:
        """
        The getWheatNeededForWheatFlourProduction method must raise ValueError if
        gristmills count is negative.
        """
        errMsg = "Gristmills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWheatNeededForWheatFlourProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWheatNeededForWheatFlourProductionSuccess(self) -> None:
        """
        The getWheatNeededForWheatFlourProduction method must correctly calculate wheat
        needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getWheatNeededForWheatFlourProduction(3)

        # Cycles per day = 24 / 0.5 = 48.0
        # Wheat per gristmill per day = 1 * 48.0 = 48.0
        # Total wheat = 3 * 48.0 = 144.0
        # Ceiling = 144
        self.assertEqual(144, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                FoodRecipeName.WHEAT_FLOUR
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                0
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                FoodRecipeName.WHEAT_FLOUR,
                HarvestName.WHEAT
            )

    def test_getGristmillsNeededForCattailFlourNegativeAmount(self) -> None:
        """
        The getGristmillsNeededForCattailFlour method must raise ValueError if
        cattail flour amount is negative.
        """
        errMsg = "Cattail flour amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGristmillsNeededForCattailFlour(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGristmillsNeededForCattailFlourSuccess(self) -> None:
        """
        The getGristmillsNeededForCattailFlour method must correctly calculate
        gristmills needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 1

        result = self.uut.getGristmillsNeededForCattailFlour(100.0)

        # Production per gristmill per day = (1 / 0.25) * 24 = 96.0
        # Gristmills needed = ceil(100.0 / 96.0) = ceil(1.041...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                FoodRecipeName.CATTAIL_FLOUR
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                1
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                1
            )

    def test_getCattailRootsNeededForCattailFlourProductionNegativeCount(self) -> None:
        """
        The getCattailRootsNeededForCattailFlourProduction method must raise ValueError if
        gristmills count is negative.
        """
        errMsg = "Gristmills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCattailRootsNeededForCattailFlourProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCattailRootsNeededForCattailFlourProductionSuccess(self) -> None:
        """
        The getCattailRootsNeededForCattailFlourProduction method must correctly calculate
        cattail roots needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getCattailRootsNeededForCattailFlourProduction(3)

        # Cycles per day = 24 / 0.25 = 96.0
        # Cattail roots per gristmill per day = 1 * 96.0 = 96.0
        # Total cattail roots = 3 * 96.0 = 288.0
        # Ceiling = 288
        self.assertEqual(288, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                FoodRecipeName.CATTAIL_FLOUR
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                1
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.GRISTMILL,
                FoodRecipeName.CATTAIL_FLOUR,
                HarvestName.CATTAIL_ROOTS
            )

    def test_getBakeriesNeededForBreadsNegativeAmount(self) -> None:
        """
        The getBakeriesNeededForBreads method must raise ValueError if breads
        amount is negative.
        """
        errMsg = "Breads amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBakeriesNeededForBreads(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBakeriesNeededForBreadsSuccess(self) -> None:
        """
        The getBakeriesNeededForBreads method must correctly calculate
        bakeries needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.42
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 5

        result = self.uut.getBakeriesNeededForBreads(300.0)

        # Production per bakery per day = (5 / 0.42) * 24 = 285.714...
        # Bakeries needed = ceil(300.0 / 285.714...) = ceil(1.05) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.BREADS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                0
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                0
            )

    def test_getWheatFlourNeededForBreadsProductionNegativeCount(self) -> None:   # noqa: E501
        """
        The getWheatFlourNeededForBreadsProduction method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWheatFlourNeededForBreadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWheatFlourNeededForBreadsProductionSuccess(self) -> None:
        """
        The getWheatFlourNeededForBreadsProduction method must correctly
        calculate wheat flour needed.
        """

        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.42
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getWheatFlourNeededForBreadsProduction(3)

        # Cycles per day = 24 / 0.42 = 57.142...
        # Wheat flour per bakery per day = 1 * 57.142... = 57.142...
        # Total wheat flour = 3 * 57.142... = 171.428...
        # Ceiling = 172
        self.assertEqual(172, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.BREADS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                0
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.BREADS,
                FoodRecipeName.WHEAT_FLOUR
            )

    def test_getLogsNeededForBreadsProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForBreadsProduction method must raise ValueError
        if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForBreadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForBreadsProductionSuccess(self) -> None:
        """
        The getLogsNeededForBreadsProduction method must correctly calculate
        logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.42
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForBreadsProduction(3)

        # Cycles per day = 24 / 0.42 = 57.142...
        # Logs per bakery per day = 0.1 * 57.142... = 5.714...
        # Total logs = 3 * 5.714... = 17.142...
        self.assertAlmostEqual(17.142857142857142, result, places=10)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.BREADS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                0
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.BREADS,
                HarvestName.LOGS
            )

    def test_getBakeriesNeededForCattailCrackersNegativeAmount(self) -> None:
        """
        The getBakeriesNeededForCattailCrackers method must raise ValueError
        if cattail crackers amount is negative.
        """
        errMsg = "Cattail crackers amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBakeriesNeededForCattailCrackers(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBakeriesNeededForCattailCrackersSuccess(self) -> None:
        """
        The getBakeriesNeededForCattailCrackers method must correctly
        calculate bakeries needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 4

        result = self.uut.getBakeriesNeededForCattailCrackers(200.0)

        # Production per bakery per day = (4 / 0.5) * 24 = 192.0
        # Bakeries needed = ceil(200.0 / 192.0) = ceil(1.041...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.CATTAIL_CRACKERS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                1
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                1
            )

    def test_getCattailFlourNeededForCattailCrackersProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getCattailFlourNeededForCattailCrackersProduction method must
        raise ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCattailFlourNeededForCattailCrackersProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCattailFlourNeededForCattailCrackersProductionSuccess(self) -> None:  # noqa: E501
        """
        The getCattailFlourNeededForCattailCrackersProduction method must
        correctly calculate cattail flour needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut \
            .getCattailFlourNeededForCattailCrackersProduction(3)

        # Cycles per day = 24 / 0.5 = 48.0
        # Cattail flour per bakery per day = 1 * 48.0 = 48.0
        # Total cattail flour = 3 * 48.0 = 144.0
        # Ceiling = 144
        self.assertEqual(144, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.CATTAIL_CRACKERS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                1
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.CATTAIL_CRACKERS,
                FoodRecipeName.CATTAIL_FLOUR
            )

    def test_getLogsNeededForCattailCrackersProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getLogsNeededForCattailCrackersProduction method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForCattailCrackersProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForCattailCrackersProductionSuccess(self) -> None:
        """
        The getLogsNeededForCattailCrackersProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForCattailCrackersProduction(3)

        # Cycles per day = 24 / 0.5 = 48.0
        # Logs per bakery per day = 0.1 * 48.0 = 4.8
        # Total logs = 3 * 4.8 = 14.4
        self.assertAlmostEqual(14.4, result, places=10)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.CATTAIL_CRACKERS
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                1
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.CATTAIL_CRACKERS,
                HarvestName.LOGS
            )

    def test_getBakeriesNeededForMaplePastriesNegativeAmount(self) -> None:
        """
        The getBakeriesNeededForMaplePastries method must raise ValueError
        if maple pastries amount is negative.
        """
        errMsg = "Maple pastries amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBakeriesNeededForMaplePastries(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBakeriesNeededForMaplePastriesSuccess(self) -> None:
        """
        The getBakeriesNeededForMaplePastries method must correctly calculate
        bakeries needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.55
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 3

        result = self.uut.getBakeriesNeededForMaplePastries(140.0)

        # Production per bakery per day = (3 / 0.55) * 24 = 130.909...
        # Bakeries needed = ceil(140.0 / 130.909...) = ceil(1.069...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.MAPLE_PASTRIES
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                2
            )
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                2
            )

    def test_getWheatFlourNeededForMaplePastriesProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getWheatFlourNeededForMaplePastriesProduction method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWheatFlourNeededForMaplePastriesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWheatFlourNeededForMaplePastriesProductionSuccess(self) -> None:  # noqa: E501
        """
        The getWheatFlourNeededForMaplePastriesProduction method must
        correctly calculate wheat flour needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.55
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getWheatFlourNeededForMaplePastriesProduction(3)

        # Cycles per day = 24 / 0.55 = 43.636...
        # Wheat flour per bakery per day = 1 * 43.636... = 43.636...
        # Total wheat flour = 3 * 43.636... = 130.909...
        # Ceiling = 131
        self.assertEqual(131, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.MAPLE_PASTRIES
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                2
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.MAPLE_PASTRIES,
                FoodRecipeName.WHEAT_FLOUR
            )

    def test_getMapleSyrupNeededForMaplePastriesProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getMapleSyrupNeededForMaplePastriesProduction method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMapleSyrupNeededForMaplePastriesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMapleSyrupNeededForMaplePastriesProductionSuccess(self) -> None:  # noqa: E501
        """
        The getMapleSyrupNeededForMaplePastriesProduction method must
        correctly calculate maple syrup needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.55
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getMapleSyrupNeededForMaplePastriesProduction(3)

        # Cycles per day = 24 / 0.55 = 43.636...
        # Maple syrup per bakery per day = 1 * 43.636... = 43.636...
        # Total maple syrup = 3 * 43.636... = 130.909...
        # Ceiling = 131
        self.assertEqual(131, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.MAPLE_PASTRIES
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                2
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.MAPLE_PASTRIES,
                HarvestName.MAPLE_SYRUP
            )

    def test_getLogsNeededForMaplePastriesProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getLogsNeededForMaplePastriesProduction method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForMaplePastriesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForMaplePastriesProductionSuccess(self) -> None:
        """
        The getLogsNeededForMaplePastriesProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.55
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForMaplePastriesProduction(3)

        # Cycles per day = 24 / 0.55 = 43.636...
        # Logs per bakery per day = 0.1 * 43.636... = 4.363...
        # Total logs = 3 * 4.363... = 13.090...
        self.assertAlmostEqual(13.090909090909092, result, places=10)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.MAPLE_PASTRIES
            )
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                2
            )
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once_with(
                FoodProcessingBuildingName.BAKERY,
                FoodRecipeName.MAPLE_PASTRIES,
                HarvestName.LOGS
            )

    def test_getLumberMillsNeededForPlanksNegativeAmount(self) -> None:
        """
        The getLumberMillsNeededForPlanks method must raise ValueError if
        planks amount is negative.
        """
        errMsg = "Planks amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLumberMillsNeededForPlanks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLumberMillsNeededForPlanksSuccess(self) -> None:
        """
        The getLumberMillsNeededForPlanks method must correctly calculate
        lumber mills needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.3
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getLumberMillsNeededForPlanks(20.0)

        # Production per lumber mill per day = (1 / 1.3) * 24 = 18.461...
        # Lumber mills needed = ceil(20.0 / 18.461...) = ceil(1.083...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.LUMBER_MILL,
            GoodsRecipeName.PLANKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.LUMBER_MILL,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.LUMBER_MILL,
            0
        )

    def test_getLogsNeededForPlanksProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForPlanksProduction method must raise ValueError if
        lumber mills count is negative.
        """
        errMsg = "Lumber mills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForPlanksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForPlanksProductionSuccess(self) -> None:
        """
        The getLogsNeededForPlanksProduction method must correctly calculate logs
        needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.3
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getLogsNeededForPlanksProduction(3)

        # Cycles per day = 24 / 1.3 = 18.461...
        # Logs per lumber mill per day = 1 * 18.461... = 18.461...
        # Total logs = 3 * 18.461... = 55.384...
        # Ceiling = 56
        self.assertEqual(56, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.LUMBER_MILL,
            GoodsRecipeName.PLANKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.LUMBER_MILL,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.LUMBER_MILL,
            GoodsRecipeName.PLANKS,
            HarvestName.LOGS
        )

    # Test Cases for Gear Workshop
    def test_getGearWorkshopsNeededForGearsNegativeAmount(self) -> None:
        """
        The getGearWorkshopsNeededForGears method must raise ValueError if
        gears amount is negative.
        """
        errMsg = "Gears amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGearWorkshopsNeededForGears(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGearWorkshopsNeededForGearsSuccess(self) -> None:
        """
        The getGearWorkshopsNeededForGears method must correctly calculate
        gear workshops needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getGearWorkshopsNeededForGears(50.0)

        # Production per gear workshop per day = (1 / 3.0) * 24 = 8
        # Gear workshops needed = ceil(50.0 / 8) = ceil(6.25) = 7
        self.assertEqual(7, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.GEAR_WORKSHOP,
            GoodsRecipeName.GEARS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.GEAR_WORKSHOP,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.GEAR_WORKSHOP,
            0
        )

    def test_getPlanksNeededForGearsProductionNegativeCount(self) -> None:
        """
        The getPlanksNeededForGearsProduction method must raise ValueError if
        gear workshops count is negative.
        """
        errMsg = "Gear workshops count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForGearsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForGearsProductionSuccess(self) -> None:
        """
        The getPlanksNeededForGearsProduction method must correctly calculate
        planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPlanksNeededForGearsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Planks per gear workshop per day = 1 * 8 = 8
        # Total planks = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.GEAR_WORKSHOP,
            GoodsRecipeName.GEARS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.GEAR_WORKSHOP,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.GEAR_WORKSHOP,
            GoodsRecipeName.GEARS,
            GoodsRecipeName.PLANKS
        )

    # Test Cases for Paper Mill
    def test_getPaperMillsNeededForPaperNegativeAmount(self) -> None:
        """
        The getPaperMillsNeededForPaper method must raise ValueError if
        paper amount is negative.
        """
        errMsg = "Paper amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPaperMillsNeededForPaper(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPaperMillsNeededForPaperSuccess(self) -> None:
        """
        The getPaperMillsNeededForPaper method must correctly calculate
        paper mills needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.6
        self.uut.factionData.getGoodsOutputQuantity.return_value = 2

        result = self.uut.getPaperMillsNeededForPaper(100.0)

        # Production per paper mill per day = (2 / 1.6) * 24 = 30
        # Paper mills needed = ceil(100.0 / 30) = ceil(3.333...) = 4
        self.assertEqual(4, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.PAPER_MILL,
            GoodsRecipeName.PAPER
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.PAPER_MILL,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.PAPER_MILL,
            0
        )

    def test_getLogsNeededForPaperProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForPaperProduction method must raise ValueError if
        paper mills count is negative.
        """
        errMsg = "Paper mills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForPaperProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForPaperProductionSuccess(self) -> None:
        """
        The getLogsNeededForPaperProduction method must correctly calculate
        logs needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.6
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getLogsNeededForPaperProduction(2)

        # Cycles per day = 24 / 1.6 = 15
        # Logs per paper mill per day = 1 * 15 = 15
        # Total logs = 2 * 15 = 30
        self.assertEqual(30, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.PAPER_MILL,
            GoodsRecipeName.PAPER
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.PAPER_MILL,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.PAPER_MILL,
            GoodsRecipeName.PAPER,
            HarvestName.LOGS
        )

    # Test Cases for Printing Press - Books
    def test_getPrintingPressesNeededForBooksNegativeAmount(self) -> None:
        """
        The getPrintingPressesNeededForBooks method must raise ValueError if
        books amount is negative.
        """
        errMsg = "Books amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPrintingPressesNeededForBooks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPrintingPressesNeededForBooksSuccess(self) -> None:
        """
        The getPrintingPressesNeededForBooks method must correctly calculate
        printing presses needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.5
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getPrintingPressesNeededForBooks(20.0)

        # Production per printing press per day = (1 / 1.5) * 24 = 16
        # Printing presses needed = ceil(20.0 / 16) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.BOOKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            0
        )

    def test_getPaperNeededForBooksProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getPaperNeededForBooksProduction method must raise
        ValueError if printing presses count is negative.
        """
        errMsg = "Printing presses count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPaperNeededForBooksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPaperNeededForBooksProductionSuccess(self) -> None:
        """
        The getPaperNeededForBooksProduction method must correctly
        calculate paper needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.5
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getPaperNeededForBooksProduction(2)

        # Cycles per day = 24 / 1.5 = 16
        # Paper per printing press per day = 2 * 16 = 32
        # Total paper = 2 * 32 = 64
        self.assertEqual(64, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.BOOKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.BOOKS,
            GoodsRecipeName.PAPER
        )

    # Test Cases for Printing Press - Punchcards
    def test_getPrintingPressesNeededForPunchcardsNegativeAmount(self) -> None:     # noqa: E501
        """
        The getPrintingPressesNeededForPunchcards method must raise ValueError
        if punchcards amount is negative.
        """
        errMsg = "Punchcards amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPrintingPressesNeededForPunchcards(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPrintingPressesNeededForPunchcardsSuccess(self) -> None:
        """
        The getPrintingPressesNeededForPunchcards method must correctly
        calculate printing presses needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 0.75
        self.uut.factionData.getGoodsOutputQuantity.return_value = 2

        result = self.uut.getPrintingPressesNeededForPunchcards(50.0)

        # Production per printing press per day = (2 / 0.75) * 24 = 64
        # Printing presses needed = ceil(50.0 / 64) = ceil(0.78125) = 1
        self.assertEqual(1, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.PUNCHCARDS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            1
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            1
        )

    def test_getPaperNeededForPunchcardsProductionNegativeCount(self) -> None:     # noqa: E501
        """
        The getPaperNeededForPunchcardsProduction method must raise
        ValueError if printing presses count is negative.
        """
        errMsg = "Printing presses count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPaperNeededForPunchcardsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPaperNeededForPunchcardsProductionSuccess(self) -> None:   # noqa: E501
        """
        The getPaperNeededForPunchcardsProduction method must
        correctly calculate paper needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 0.75
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getPaperNeededForPunchcardsProduction(2)

        # Cycles per day = 24 / 0.75 = 32
        # Paper per printing press per day = 2 * 32 = 64
        # Total paper = 2 * 64 = 128
        self.assertEqual(128, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.PUNCHCARDS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            1
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.PUNCHCARDS,
            GoodsRecipeName.PAPER
        )

    def test_getPlanksNeededForPunchcardsProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getPlanksNeededForPunchcardsProduction method must raise
        ValueError if printing presses count is negative.
        """
        errMsg = "Printing presses count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForPunchcardsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForPunchcardsProductionSuccess(self) -> None:  # noqa: E501
        """
        The getPlanksNeededForPunchcardsProduction method must
        correctly calculate planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 0.75
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPlanksNeededForPunchcardsProduction(2)

        # Cycles per day = 24 / 0.75 = 32
        # Planks per printing press per day = 1 * 32 = 32
        # Total planks = 2 * 32 = 64
        self.assertEqual(64, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.PUNCHCARDS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            1
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.PRINTING_PRESS,
            GoodsRecipeName.PUNCHCARDS,
            GoodsRecipeName.PLANKS
        )

    # Test Cases for Wood Workshop
    def test_getWoodWorkshopsNeededForTreatedPlanksNegativeAmount(self) -> None:    # noqa: E501
        """
        The getWoodWorkshopsNeededForTreatedPlanks method must raise ValueError
        if treated planks amount is negative.
        """
        errMsg = "Treated planks amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWoodWorkshopsNeededForTreatedPlanks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWoodWorkshopsNeededForTreatedPlanksSuccess(self) -> None:
        """
        The getWoodWorkshopsNeededForTreatedPlanks method must correctly
        calculate wood workshops needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getWoodWorkshopsNeededForTreatedPlanks(30.0)

        # Production per wood workshop per day = (1 / 3.0) * 24 = 8
        # Wood workshops needed = ceil(30.0 / 8) = ceil(3.75) = 4
        self.assertEqual(4, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            GoodsRecipeName.TREATED_PLANKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            0
        )

    def test_getPineResinNeededForTreatedPlanksProductionNegativeCount(self) -> None:
        """
        The getPineResinNeededForTreatedPlanksProduction method must raise ValueError if
        wood workshops count is negative.
        """
        errMsg = "Wood workshops count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPineResinNeededForTreatedPlanksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPineResinNeededForTreatedPlanksProductionSuccess(self) -> None:
        """
        The getPineResinNeededForTreatedPlanksProduction method must correctly calculate
        pine resin needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPineResinNeededForTreatedPlanksProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Pine resin per wood workshop per day = 1 * 8 = 8
        # Total pine resin = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            GoodsRecipeName.TREATED_PLANKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            GoodsRecipeName.TREATED_PLANKS,
            HarvestName.PINE_RESIN
        )

    def test_getPlanksNeededForTreatedPlanksProductionNegativeCount(self) -> None:
        """
        The getPlanksNeededForTreatedPlanksProduction method must raise ValueError if
        wood workshops count is negative.
        """
        errMsg = "Wood workshops count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForTreatedPlanksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForTreatedPlanksProductionSuccess(self) -> None:
        """
        The getPlanksNeededForTreatedPlanksProduction method must correctly calculate
        planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPlanksNeededForTreatedPlanksProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Planks per wood workshop per day = 1 * 8 = 8
        # Total planks = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            GoodsRecipeName.TREATED_PLANKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.WOOD_WORKSHOP,
            GoodsRecipeName.TREATED_PLANKS,
            GoodsRecipeName.PLANKS
        )

    # Test Cases for Smelter
    def test_getSmeltersNeededForMetalBlocksNegativeAmount(self) -> None:
        """
        The getSmeltersNeededForMetalBlocks method must raise ValueError if
        metal blocks amount is negative.
        """
        errMsg = "Metal blocks amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getSmeltersNeededForMetalBlocks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSmeltersNeededForMetalBlocksSuccess(self) -> None:
        """
        The getSmeltersNeededForMetalBlocks method must correctly calculate
        smelters needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getSmeltersNeededForMetalBlocks(15.0)

        # Production per smelter per day = (1 / 2.0) * 24 = 12
        # Smelters needed = ceil(15.0 / 12) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            GoodsRecipeName.METAL_BLOCKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            0
        )

    def test_getScrapMetalNeededForMetalBlocksProductionNegativeCount(self) -> None:
        """
        The getScrapMetalNeededForMetalBlocksProduction method must raise ValueError if
        smelters count is negative.
        """
        errMsg = "Smelters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getScrapMetalNeededForMetalBlocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getScrapMetalNeededForMetalBlocksProductionSuccess(self) -> None:
        """
        The getScrapMetalNeededForMetalBlocksProduction method must correctly calculate
        scrap metal needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getScrapMetalNeededForMetalBlocksProduction(2)

        # Cycles per day = 24 / 2.0 = 12
        # Scrap metal per smelter per day = 1 * 12 = 12
        # Total scrap metal = 2 * 12 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            GoodsRecipeName.METAL_BLOCKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            GoodsRecipeName.METAL_BLOCKS,
            GoodsRecipeName.SCRAP_METAL
        )

    def test_getLogsNeededForMetalBlocksProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForMetalBlocksProduction method must raise ValueError if
        smelters count is negative.
        """
        errMsg = "Smelters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForMetalBlocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForMetalBlocksProductionSuccess(self) -> None:
        """
        The getLogsNeededForMetalBlocksProduction method must correctly calculate
        logs needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 0.2

        result = self.uut.getLogsNeededForMetalBlocksProduction(2)

        # Cycles per day = 24 / 2.0 = 12
        # Logs per smelter per day = 0.2 * 12 = 2.4
        # Total logs = 2 * 2.4 = 4.8
        self.assertAlmostEqual(4.8, result, places=5)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            GoodsRecipeName.METAL_BLOCKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.SMELTER,
            GoodsRecipeName.METAL_BLOCKS,
            HarvestName.LOGS
        )

    # Test Cases for Mine
    def test_getMinesNeededForScrapMetalNegativeAmount(self) -> None:
        """
        The getMinesNeededForScrapMetal method must raise ValueError if
        scrap metal amount is negative.
        """
        errMsg = "Scrap metal amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMinesNeededForScrapMetal(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMinesNeededForScrapMetalSuccess(self) -> None:
        """
        The getMinesNeededForScrapMetal method must correctly calculate
        mines needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.8
        self.uut.factionData.getGoodsOutputQuantity.return_value = 5

        result = self.uut.getMinesNeededForScrapMetal(100.0)

        # Production per mine per day = (5 / 1.8) * 24 = 66.666...
        # Mines needed = ceil(100.0 / 66.666...) = ceil(1.5) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.MINE,
            GoodsRecipeName.SCRAP_METAL
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.MINE,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.MINE,
            0
        )

    def test_getTreatedPlanksNeededForScrapMetalProductionNegativeCount(self) -> None:
        """
        The getTreatedPlanksNeededForScrapMetalProduction method must raise ValueError if
        mines count is negative.
        """
        errMsg = "Mines count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getTreatedPlanksNeededForScrapMetalProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getTreatedPlanksNeededForScrapMetalProductionSuccess(self) -> None:
        """
        The getTreatedPlanksNeededForScrapMetalProduction method must correctly calculate
        treated planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.8
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getTreatedPlanksNeededForScrapMetalProduction(3)

        # Cycles per day = 24 / 1.8 = 13.333...
        # Treated planks per mine per day = 1 * 13.333... = 13.333...
        # Total treated planks = 3 * 13.333... = 40
        self.assertEqual(40, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.MINE,
            GoodsRecipeName.SCRAP_METAL
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.MINE,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.MINE,
            GoodsRecipeName.SCRAP_METAL,
            GoodsRecipeName.TREATED_PLANKS
        )

    def test_getRefineriesNeededForBiofuelCarrotsNegativeAmount(self) -> None:
        """
        The getRefineriesNeededForBiofuelCarrots method must raise ValueError
        if biofuel carrots amount is negative.
        """
        errMsg = "Biofuel Carrots amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getRefineriesNeededForBiofuelCarrots(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getRefineriesNeededForBiofuelCarrotsSuccess(self) -> None:
        """
        The getRefineriesNeededForBiofuelCarrots method must correctly
        calculate refineries needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 5

        result = self.uut.getRefineriesNeededForBiofuelCarrots(100.0)

        # Production per refinery per day = (5 / 3.0) * 24 = 40
        # Refineries needed = ceil(100.0 / 40) = ceil(2.5) = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_CARROTS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            0
        )

    def test_getCarrotsNeededForBiofuelCarrotsProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getCarrotsNeededForBiofuelCarrotsProduction method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCarrotsNeededForBiofuelCarrotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCarrotsNeededForBiofuelCarrotsProductionSuccess(self) -> None:  # noqa: E501
        """
        The getCarrotsNeededForBiofuelCarrotsProduction method must
        correctly calculate carrots needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getCarrotsNeededForBiofuelCarrotsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Carrots per refinery per day = 2 * 8 = 16
        # Total carrots = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_CARROTS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_CARROTS,
            HarvestName.CARROTS
        )

    def test_getWaterNeededForBiofuelCarrotsProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getWaterNeededForBiofuelCarrotsProduction method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWaterNeededForBiofuelCarrotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWaterNeededForBiofuelCarrotsProductionSuccess(self) -> None:    # noqa: E501
        """
        The getWaterNeededForBiofuelCarrotsProduction method must
        correctly calculate water needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getWaterNeededForBiofuelCarrotsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Water per refinery per day = 2 * 8 = 16
        # Total water = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_CARROTS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_CARROTS,
            HarvestName.WATER
        )

    def test_getRefineriesNeededForBiofuelPotatoesNegativeAmount(self) -> None:     # noqa: E501
        """
        The getRefineriesNeededForBiofuelPotatoes method must raise ValueError
        if biofuel potatoes amount is negative.
        """
        errMsg = "Biofuel Potatoes amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getRefineriesNeededForBiofuelPotatoes(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getRefineriesNeededForBiofuelPotatoesSuccess(self) -> None:
        """
        The getRefineriesNeededForBiofuelPotatoes method must correctly
        calculate refineries needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 30

        result = self.uut.getRefineriesNeededForBiofuelPotatoes(250.0)

        # Production per refinery per day = (30 / 3.0) * 24 = 240
        # Refineries needed = ceil(250.0 / 240) = ceil(1.0416...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_POTATOES
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            1
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            1
        )

    def test_getPotatoesNeededForBiofuelPotatoesProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getPotatoesNeededForBiofuelPotatoesProduction method must
        raise ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPotatoesNeededForBiofuelPotatoesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPotatoesNeededForBiofuelPotatoesProductionSuccess(self) -> None:    # noqa: E501
        """
        The getPotatoesNeededForBiofuelPotatoesProduction method must
        correctly calculate potatoes needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getPotatoesNeededForBiofuelPotatoesProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Potatoes per refinery per day = 2 * 8 = 16
        # Total potatoes = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_POTATOES
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            1
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_POTATOES,
            HarvestName.POTATOES
        )

    def test_getWaterNeededForBiofuelPotatoesProductionNegativeCount(self) -> None:     # noqa: E501
        """
        The getWaterNeededForBiofuelPotatoesProduction method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWaterNeededForBiofuelPotatoesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWaterNeededForBiofuelPotatoesProductionSuccess(self) -> None:   # noqa: E501
        """
        The getWaterNeededForBiofuelPotatoesProduction method must
        correctly calculate water needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getWaterNeededForBiofuelPotatoesProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Water per refinery per day = 2 * 8 = 16
        # Total water = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_POTATOES
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            1
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_POTATOES,
            HarvestName.WATER
        )

    def test_getRefineriesNeededForBiofuelSpadderdocksNegativeAmount(self) -> None:     # noqa: E501
        """
        The getRefineriesNeededForBiofuelSpadderdocks method must raise
        ValueError if biofuel spadderdocks amount is negative.
        """
        errMsg = "Biofuel Spadderdocks amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getRefineriesNeededForBiofuelSpadderdocks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getRefineriesNeededForBiofuelSpadderdocksSuccess(self) -> None:
        """
        The getRefineriesNeededForBiofuelSpadderdocks method must correctly
        calculate refineries needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 25

        result = self.uut.getRefineriesNeededForBiofuelSpadderdocks(220.0)

        # Production per refinery per day = (25 / 3.0) * 24 = 200
        # Refineries needed = ceil(220.0 / 200) = ceil(1.1) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_SPADDERDOCKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            2
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            2
        )

    def test_getSpadderdocksNeededForBiofuelSpadderdocksProductionNegativeCount(self) -> None:      # noqa: E501
        """
        The getSpadderdocksNeededForBiofuelSpadderdocksProduction method
        must raise ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut \
                .getSpadderdocksNeededForBiofuelSpadderdocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSpadderdocksNeededForBiofuelSpadderdocksProductionSuccess(self) -> None:    # noqa: E501
        """
        The getSpadderdocksNeededForBiofuelSpadderdocksProduction method
        must correctly calculate spadderdocks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut \
            .getSpadderdocksNeededForBiofuelSpadderdocksProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Spadderdocks per refinery per day = 2 * 8 = 16
        # Total spadderdocks = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_SPADDERDOCKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            2
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_SPADDERDOCKS,
            HarvestName.SPADDERDOCKS
        )

    def test_getWaterNeededForBiofuelSpadderdocksProductionNegativeCount(self) -> None:     # noqa: E501
        """
        The getWaterNeededForBiofuelSpadderdocksProduction method must
        raise ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWaterNeededForBiofuelSpadderdocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWaterNeededForBiofuelSpadderdocksProductionSuccess(self) -> None:   # noqa: E501
        """
        The getWaterNeededForBiofuelSpadderdocksProduction method must
        correctly calculate water needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getWaterNeededForBiofuelSpadderdocksProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Water per refinery per day = 2 * 8 = 16
        # Total water = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_SPADDERDOCKS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            2
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.BIOFUEL_SPADDERDOCKS,
            HarvestName.WATER
        )

    def test_getRefineriesNeededForCatalystNegativeAmount(self) -> None:
        """
        The getRefineriesNeededForCatalyst method must raise ValueError if
        catalyst amount is negative.
        """
        errMsg = "Catalyst amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getRefineriesNeededForCatalyst(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getRefineriesNeededForCatalystSuccess(self) -> None:
        """
        The getRefineriesNeededForCatalyst method must correctly calculate
        refineries needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 3
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getRefineriesNeededForCatalyst(15.0)

        # Production per refinery per day = (1 / 2.0) * 24 = 12
        # Refineries needed = ceil(15.0 / 12) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.CATALYST
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            3
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            3
        )

    def test_getMapleSyrupNeededForCatalystProductionNegativeCount(self) -> None:   # noqa: E501
        """
        The getMapleSyrupNeededForCatalystProduction method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMapleSyrupNeededForCatalystProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMapleSyrupNeededForCatalystProductionSuccess(self) -> None:
        """
        The getMapleSyrupNeededForCatalystProduction method must correctly
        calculate maple syrup needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 3
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getMapleSyrupNeededForCatalystProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Maple syrup per refinery per day = 1 * 12 = 12
        # Total maple syrup = 3 * 12 = 36
        self.assertEqual(36, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.CATALYST
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            3
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.CATALYST,
            HarvestName.MAPLE_SYRUP
        )

    def test_getExtractNeededForCatalystProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getExtractNeededForCatalystProduction method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getExtractNeededForCatalystProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getExtractNeededForCatalystProductionSuccess(self) -> None:
        """
        The getExtractNeededForCatalystProduction method must correctly
        calculate extract needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 3
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getExtractNeededForCatalystProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Extract per refinery per day = 1 * 12 = 12
        # Total extract = 3 * 12 = 36
        self.assertEqual(36, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.CATALYST
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            3
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.REFINERY,
            GoodsRecipeName.CATALYST,
            GoodsRecipeName.EXTRACT
        )

    # Test Cases for Bot Part Factory
    def test_getBotPartFactoriesNeededForBotChassisNegativeAmount(self) -> None:    # noqa: E501
        """
        The getBotPartFactoriesNeededForBotChassis method must raise
        ValueError if bot chassis amount is negative.
        """
        errMsg = "Bot Chassis amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotPartFactoriesNeededForBotChassis(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotPartFactoriesNeededForBotChassisSuccess(self) -> None:
        """
        The getBotPartFactoriesNeededForBotChassis method must correctly
        calculate bot part factories needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 4.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getBotPartFactoriesNeededForBotChassis(8.0)

        # Production per bot part factory per day = (1 / 4.0) * 24 = 6
        # Bot part factories needed = ceil(8.0 / 6) = ceil(1.333...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_CHASSIS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            0
        )

    def test_getPlanksNeededForBotChassisProductionNegativeCount(self) -> None:   # noqa: E501
        """
        The getPlanksNeededForBotChassisProduction method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForBotChassisProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForBotChassisProductionSuccess(self) -> None:     # noqa: E501
        """
        The getPlanksNeededForBotChassisProduction method must
        correctly calculate planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 4.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getPlanksNeededForBotChassisProduction(3)

        # Cycles per day = 24 / 4.0 = 6
        # Planks per bot part factory per day = 2 * 6 = 12
        # Total planks = 3 * 12 = 36
        self.assertEqual(36, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_CHASSIS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_CHASSIS,
            GoodsRecipeName.PLANKS
        )

    def test_getMetalBlocksNeededForBotChassisProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getMetalBlocksNeededForBotChassisProduction method must
        raise ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMetalBlocksNeededForBotChassisProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMetalBlocksNeededForBotChassisProductionSuccess(self) -> None:    # noqa: E501
        """
        The getMetalBlocksNeededForBotChassisProduction method must
        correctly calculate metal blocks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 4.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut \
            .getMetalBlocksNeededForBotChassisProduction(3)

        # Cycles per day = 24 / 4.0 = 6
        # Metal blocks per bot part factory per day = 1 * 6 = 6
        # Total metal blocks = 3 * 6 = 18
        self.assertEqual(18, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_CHASSIS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_CHASSIS,
            GoodsRecipeName.METAL_BLOCKS
        )

    def test_getBiofuelNeededForBotChassisProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getBiofuelNeededForBotChassisProduction method must
        raise ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBiofuelNeededForBotChassisProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBiofuelNeededForBotChassisProductionSuccess(self) -> None:    # noqa: E501
        """
        The getBiofuelNeededForBotChassisProduction method must
        correctly calculate biofuel needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 4.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getBiofuelNeededForBotChassisProduction(3)

        # Cycles per day = 24 / 4.0 = 6
        # Biofuel per bot part factory per day = 1 * 6 = 6
        # Total biofuel = 3 * 6 = 18
        self.assertEqual(18, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_CHASSIS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_CHASSIS,
            GoodsRecipeName.BIOFUEL
        )

    def test_getBotPartFactoriesNeededForBotHeadsNegativeAmount(self) -> None:
        """
        The getBotPartFactoriesNeededForBotHeads method must raise ValueError
        if bot heads amount is negative.
        """
        errMsg = "Bot Heads amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotPartFactoriesNeededForBotHeads(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotPartFactoriesNeededForBotHeadsSuccess(self) -> None:
        """
        The getBotPartFactoriesNeededForBotHeads method must correctly
        calculate bot part factories needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getBotPartFactoriesNeededForBotHeads(10.0)

        # Production per bot part factory per day = (1 / 3.0) * 24 = 8
        # Bot part factories needed = ceil(10.0 / 8) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_HEADS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            1
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            1
        )

    def test_getGearsNeededForBotHeadsProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getGearsNeededForBotHeadsProduction method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGearsNeededForBotHeadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGearsNeededForBotHeadsProductionSuccess(self) -> None:    # noqa: E501
        """
        The getGearsNeededForBotHeadsProduction method must
        correctly calculate gears needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getGearsNeededForBotHeadsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Gears per bot part factory per day = 1 * 8 = 8
        # Total gears = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_HEADS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            1
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_HEADS,
            GoodsRecipeName.GEARS
        )

    def test_getMetalBlocksNeededForBotHeadsProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getMetalBlocksNeededForBotHeadsProduction method must
        raise ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMetalBlocksNeededForBotHeadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMetalBlocksNeededForBotHeadsProductionSuccess(self) -> None:  # noqa: E501
        """
        The getMetalBlocksNeededForBotHeadsProduction method must
        correctly calculate metal blocks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut \
            .getMetalBlocksNeededForBotHeadsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Metal blocks per bot part factory per day = 1 * 8 = 8
        # Total metal blocks = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_HEADS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            1
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_HEADS,
            GoodsRecipeName.METAL_BLOCKS
        )

    def test_getPlanksNeededForBotHeadsProductionNegativeCount(self) -> None:     # noqa: E501
        """
        The getPlanksNeededForBotHeadsProduction method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForBotHeadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForBotHeadsProductionSuccess(self) -> None:   # noqa: E501
        """
        The getPlanksNeededForBotHeadsProduction method must
        correctly calculate planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPlanksNeededForBotHeadsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Planks per bot part factory per day = 1 * 8 = 8
        # Total planks = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_HEADS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            1
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_HEADS,
            GoodsRecipeName.PLANKS
        )

    def test_getBotPartFactoriesNeededForBotLimbsNegativeAmount(self) -> None:
        """
        The getBotPartFactoriesNeededForBotLimbs method must raise ValueError
        if bot limbs amount is negative.
        """
        errMsg = "Bot Limbs amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotPartFactoriesNeededForBotLimbs(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotPartFactoriesNeededForBotLimbsSuccess(self) -> None:
        """
        The getBotPartFactoriesNeededForBotLimbs method must correctly
        calculate bot part factories needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 2

        result = self.uut.getBotPartFactoriesNeededForBotLimbs(20.0)

        # Production per bot part factory per day = (2 / 3.0) * 24 = 16
        # Bot part factories needed = ceil(20.0 / 16) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_LIMBS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            2
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            2
        )

    def test_getGearsNeededForBotLimbsProductionNegativeCount(self) -> None:  # noqa: E501
        """
        The getGearsNeededForBotLimbsProduction method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGearsNeededForBotLimbsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGearsNeededForBotLimbsProductionSuccess(self) -> None:    # noqa: E501
        """
        The getGearsNeededForBotLimbsProduction method must
        correctly calculate gears needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getGearsNeededForBotLimbsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Gears per bot part factory per day = 2 * 8 = 16
        # Total gears = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_LIMBS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            2
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_LIMBS,
            GoodsRecipeName.GEARS
        )

    def test_getPlanksNeededForBotLimbsProductionNegativeCount(self) -> None:     # noqa: E501
        """
        The getPlanksNeededForBotLimbsProduction method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForBotLimbsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForBotLimbsProductionSuccess(self) -> None:   # noqa: E501
        """
        The getPlanksNeededForBotLimbsProduction method must
        correctly calculate planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPlanksNeededForBotLimbsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Planks per bot part factory per day = 1 * 8 = 8
        # Total planks = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_LIMBS
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            2
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_PART_FACTORY,
            GoodsRecipeName.BOT_LIMBS,
            GoodsRecipeName.PLANKS
        )

    # Test Cases for Bot Assembler
    def test_getBotAssemblersNeededForBotsNegativeAmount(self) -> None:
        """
        The getBotAssemblersNeededForBots method must raise ValueError if
        bots amount is negative.
        """
        errMsg = "Bots amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotAssemblersNeededForBots(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotAssemblersNeededForBotsSuccess(self) -> None:
        """
        The getBotAssemblersNeededForBots method must correctly calculate
        bot assemblers needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 6.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getBotAssemblersNeededForBots(5.0)

        # Production per bot assembler per day = (1 / 6.0) * 24 = 4
        # Bot assemblers needed = ceil(5.0 / 4) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            GoodsRecipeName.BOT
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            0
        )

    def test_getBotChassisNeededForBotsProductionNegativeCount(self) -> None:
        """
        The getBotChassisNeededForBotsProduction method must raise ValueError
        if bot assemblers count is negative.
        """
        errMsg = "Bot assemblers count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotChassisNeededForBotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotChassisNeededForBotsProductionSuccess(self) -> None:
        """
        The getBotChassisNeededForBotsProduction method must correctly
        calculate bot chassis needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 6.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getBotChassisNeededForBotsProduction(3)

        # Cycles per day = 24 / 6.0 = 4
        # Bot chassis per bot assembler per day = 1 * 4 = 4
        # Total bot chassis = 3 * 4 = 12
        self.assertEqual(12, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            GoodsRecipeName.BOT
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            GoodsRecipeName.BOT,
            GoodsRecipeName.BOT_CHASSIS
        )

    def test_getBotHeadsNeededForBotsProductionNegativeCount(self) -> None:
        """
        The getBotHeadsNeededForBotsProduction method must raise ValueError
        if bot assemblers count is negative.
        """
        errMsg = "Bot assemblers count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotHeadsNeededForBotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotHeadsNeededForBotsProductionSuccess(self) -> None:
        """
        The getBotHeadsNeededForBotsProduction method must correctly calculate
        bot heads needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 6.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getBotHeadsNeededForBotsProduction(3)

        # Cycles per day = 24 / 6.0 = 4
        # Bot heads per bot assembler per day = 1 * 4 = 4
        # Total bot heads = 3 * 4 = 12
        self.assertEqual(12, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            GoodsRecipeName.BOT
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            GoodsRecipeName.BOT,
            GoodsRecipeName.BOT_HEADS
        )

    def test_getBotLimbsNeededForBotsProductionNegativeCount(self) -> None:
        """
        The getBotLimbsNeededForBotsProduction method must raise ValueError
        if bot assemblers count is negative.
        """
        errMsg = "Bot assemblers count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotLimbsNeededForBotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotLimbsNeededForBotsProductionSuccess(self) -> None:
        """
        The getBotLimbsNeededForBotsProduction method must correctly calculate
        bot limbs needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 6.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getBotLimbsNeededForBotsProduction(3)

        # Cycles per day = 24 / 6.0 = 4
        # Bot limbs per bot assembler per day = 1 * 4 = 4
        # Total bot limbs = 3 * 4 = 12
        self.assertEqual(12, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            GoodsRecipeName.BOT
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.BOT_ASSEMBLER,
            GoodsRecipeName.BOT,
            GoodsRecipeName.BOT_LIMBS
        )

    # Test Cases for Explosives Factory
    def test_getExplosivesFactoriesNeededForExplosivesNegativeAmount(self) -> None:     # noqa: E501
        """
        The getExplosivesFactoriesNeededForExplosives method must raise
        ValueError if explosives amount is negative.
        """
        errMsg = "Explosives amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getExplosivesFactoriesNeededForExplosives(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getExplosivesFactoriesNeededForExplosivesSuccess(self) -> None:
        """
        The getExplosivesFactoriesNeededForExplosives method must correctly
        calculate explosives factories needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getExplosivesFactoriesNeededForExplosives(15.0)

        # Production per explosives factory per day = (1 / 2.0) * 24 = 12
        # Explosives factories needed = ceil(15.0 / 12) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.EXPLOSIVES_FACTORY,
            GoodsRecipeName.EXPLOSIVES
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.EXPLOSIVES_FACTORY,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.EXPLOSIVES_FACTORY,
            0
        )

    def test_getBadwaterNeededForExplosivesProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getBadwaterNeededForExplosivesProduction method must raise
        ValueError if explosives factories count is negative.
        """
        errMsg = "Explosives factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBadwaterNeededForExplosivesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBadwaterNeededForExplosivesProductionSuccess(self) -> None:
        """
        The getBadwaterNeededForExplosivesProduction method must correctly
        calculate badwater needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 5

        result = self.uut.getBadwaterNeededForExplosivesProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Badwater per explosives factory per day = 5 * 12 = 60
        # Total badwater = 3 * 60 = 180
        self.assertEqual(180, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.EXPLOSIVES_FACTORY,
            GoodsRecipeName.EXPLOSIVES
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.EXPLOSIVES_FACTORY,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.EXPLOSIVES_FACTORY,
            GoodsRecipeName.EXPLOSIVES,
            HarvestName.BADWATER
        )

    # Test Cases for Centrifuge
    def test_getCentrifugesNeededForExtractNegativeAmount(self) -> None:
        """
        The getCentrifugesNeededForExtract method must raise ValueError if
        extract amount is negative.
        """
        errMsg = "Extract amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCentrifugesNeededForExtract(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCentrifugesNeededForExtractSuccess(self) -> None:
        """
        The getCentrifugesNeededForExtract method must correctly calculate
        centrifuges needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getCentrifugesNeededForExtract(10.0)

        # Production per centrifuge per day = (1 / 3.0) * 24 = 8
        # Centrifuges needed = ceil(10.0 / 8) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            GoodsRecipeName.EXTRACT
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            0
        )

    def test_getBadwaterNeededForExtractProductionNegativeCount(self) -> None:
        """
        The getBadwaterNeededForExtractProduction method must raise ValueError if
        centrifuges count is negative.
        """
        errMsg = "Centrifuges count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBadwaterNeededForExtractProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBadwaterNeededForExtractProductionSuccess(self) -> None:
        """
        The getBadwaterNeededForExtractProduction method must correctly calculate
        badwater needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 5

        result = self.uut.getBadwaterNeededForExtractProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Badwater per centrifuge per day = 5 * 8 = 40
        # Total badwater = 3 * 40 = 120
        self.assertEqual(120, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            GoodsRecipeName.EXTRACT
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            GoodsRecipeName.EXTRACT,
            HarvestName.BADWATER
        )

    def test_getLogsNeededForExtractProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForExtractProduction method must raise ValueError if
        centrifuges count is negative.
        """
        errMsg = "Centrifuges count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForExtractProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForExtractProductionSuccess(self) -> None:
        """
        The getLogsNeededForExtractProduction method must correctly calculate logs
        needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getLogsNeededForExtractProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Logs per centrifuge per day = 2 * 8 = 16
        # Total logs = 3 * 16 = 48
        self.assertAlmostEqual(48.0, result, places=5)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            GoodsRecipeName.EXTRACT
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.CENTRIFUGE,
            GoodsRecipeName.EXTRACT,
            HarvestName.LOGS
        )

    # Test Cases for Herbalist
    def test_getHerbalistsNeededForAntidoteNegativeAmount(self) -> None:
        """
        The getHerbalistsNeededForAntidote method must raise ValueError if
        antidote amount is negative.
        """
        errMsg = "Antidote amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getHerbalistsNeededForAntidote(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getHerbalistsNeededForAntidoteSuccess(self) -> None:
        """
        The getHerbalistsNeededForAntidote method must correctly calculate
        herbalists needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getHerbalistsNeededForAntidote(15.0)

        # Production per herbalist per day = (1 / 2.0) * 24 = 12
        # Herbalists needed = ceil(15.0 / 12) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            GoodsRecipeName.ANTIDOTE
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            0
        )
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            0
        )

    def test_getDandelionsNeededForAntidoteProductionNegativeCount(self) -> None:
        """
        The getDandelionsNeededForAntidoteProduction method must raise ValueError if
        herbalists count is negative.
        """
        errMsg = "Herbalists count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getDandelionsNeededForAntidoteProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDandelionsNeededForAntidoteProductionSuccess(self) -> None:
        """
        The getDandelionsNeededForAntidoteProduction method must correctly calculate
        dandelions needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 2

        result = self.uut.getDandelionsNeededForAntidoteProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Dandelions per herbalist per day = 2 * 12 = 24
        # Total dandelions = 3 * 24 = 72
        self.assertEqual(72, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            GoodsRecipeName.ANTIDOTE
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            GoodsRecipeName.ANTIDOTE,
            HarvestName.DANDELIONS
        )

    def test_getBerriesNeededForAntidoteProductionNegativeCount(self) -> None:
        """
        The getBerriesNeededForAntidoteProduction method must raise ValueError if
        herbalists count is negative.
        """
        errMsg = "Herbalists count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBerriesNeededForAntidoteProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBerriesNeededForAntidoteProductionSuccess(self) -> None:
        """
        The getBerriesNeededForAntidoteProduction method must correctly calculate
        berries needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 3

        result = self.uut.getBerriesNeededForAntidoteProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Berries per herbalist per day = 3 * 12 = 36
        # Total berries = 3 * 36 = 108
        self.assertEqual(108, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            GoodsRecipeName.ANTIDOTE
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            0
        )
        self.uut.factionData.getGoodsInputQuantity.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            GoodsRecipeName.ANTIDOTE,
            HarvestName.BERRIES
        )

    def test_getPapersNeededForAntidoteProductionNegativeCount(self) -> None:
        """
        The getPapersNeededForAntidoteProduction method must raise ValueError if
        herbalists count is negative.
        """
        errMsg = "Herbalists count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPapersNeededForAntidoteProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPapersNeededForAntidoteProductionSuccess(self) -> None:
        """
        The getPapersNeededForAntidoteProduction method must correctly calculate logs
        needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPapersNeededForAntidoteProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Logs per herbalist per day = 1 * 12 = 12
        # Total logs = 3 * 12 = 36
        self.assertAlmostEqual(36.0, result, places=5)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            GoodsRecipeName.ANTIDOTE
        )
        self.uut.factionData.getGoodsProductionTime.assert_called_once_with(
            GoodsBuildingName.HERBALIST,
            0
        )
        self.uut.factionData.getGoodsInputQuantity \
            .assert_called_once_with(GoodsBuildingName.HERBALIST,
                                     GoodsRecipeName.ANTIDOTE,
                                     GoodsRecipeName.PAPER)
