from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.factions.folktail import Folktail                     # noqa: E402
from pkgs.data.emunerators import DifficultyLevel               # noqa: E402


class TestFolktail(TestCase):
    """
    Folktail class test cases.
    """

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
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getDailyFoodConsumption(-1, DifficultyLevel.NORMAL)
        self.assertEqual("Population cannot be negative.",
                         str(context.exception))

    def test_getDailyFoodConsumptionSuccess(self) -> None:
        """
        The getDailyFoodConsumption method must correctly calculate daily
        food consumption based on population and difficulty.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getConsumption.return_value = 2.75
            mockFactionDataInstance.getDifficultyModifier.return_value = 1.0
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getDailyFoodConsumption(100,
                                                      DifficultyLevel.NORMAL)

            self.assertEqual(275.0, result)
            mockFactionDataInstance.getDifficultyModifier.assert_called_once_with(
                DifficultyLevel.NORMAL)

    def test_getDailyWaterConsumptionNegativePopulation(self) -> None:
        """
        The getDailyWaterConsumption method must raise ValueError if
        population is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getDailyWaterConsumption(-1, DifficultyLevel.NORMAL)
        self.assertEqual("Population cannot be negative.",
                         str(context.exception))

    def test_getDailyWaterConsumptionSuccess(self) -> None:
        """
        The getDailyWaterConsumption method must correctly calculate daily
        water consumption based on population and difficulty.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getConsumption.return_value = 2.25
            mockFactionDataInstance.getDifficultyModifier.return_value = 1.0
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getDailyWaterConsumption(100,
                                                       DifficultyLevel.NORMAL)

            self.assertEqual(225.0, result)
            mockFactionDataInstance.getDifficultyModifier.assert_called_once_with(
                DifficultyLevel.NORMAL)

    def test_getFoodPerTypeNegativePopulation(self) -> None:
        """
        The getFoodPerType method must raise ValueError if population is
        negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getFoodPerType(-1, 5, DifficultyLevel.NORMAL)
        self.assertEqual("Population cannot be negative.",
                         str(context.exception))

    def test_getFoodPerTypeZeroFoodTypeCount(self) -> None:
        """
        The getFoodPerType method must raise ValueError if foodTypeCount is
        zero.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getFoodPerType(100, 0, DifficultyLevel.NORMAL)
        self.assertEqual("Food type count must be positive.",
                         str(context.exception))

    def test_getFoodPerTypeNegativeFoodTypeCount(self) -> None:
        """
        The getFoodPerType method must raise ValueError if foodTypeCount is
        negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getFoodPerType(100, -5, DifficultyLevel.NORMAL)
        self.assertEqual("Food type count must be positive.",
                         str(context.exception))

    def test_getFoodPerTypeSuccess(self) -> None:
        """
        The getFoodPerType method must correctly calculate food per type by
        dividing total food consumption by the number of food types.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getConsumption.return_value = 2.75
            mockFactionDataInstance.getDifficultyModifier.return_value = 1.0
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getFoodPerType(100, 5, DifficultyLevel.NORMAL)

            # 100 * 2.75 * 1.0 = 275.0 / 5 = 55.0
            self.assertEqual(55.0, result)

    def test_getBerryTilesNeededNegativeAmount(self) -> None:
        """
        The getBerryTilesNeeded method must raise ValueError if berry
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBerryTilesNeeded(-10.0)
        self.assertEqual("Berry amount cannot be negative.",
                         str(context.exception))

    def test_getBerryTilesNeededSuccess(self) -> None:
        """
        The getBerryTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 12
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBerryTilesNeeded(30.0)

            # Production per tile = 3 / 12 = 0.25
            # Tiles needed = 30.0 / 0.25 = 120.0
            self.assertEqual(120.0, result)

    def test_getCarrotTilesNeededNegativeAmount(self) -> None:
        """
        The getCarrotTilesNeeded method must raise ValueError if carrot
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCarrotTilesNeeded(-10.0, False)
        self.assertEqual("Carrot amount cannot be negative.",
                         str(context.exception))

    def test_getCarrotTilesNeededWithoutBeehive(self) -> None:
        """
        The getCarrotTilesNeeded method must correctly calculate tiles
        needed without beehive modifier.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 4
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getCarrotTilesNeeded(30.0, False)

            # Production per tile = 3 / 4 = 0.75
            # Tiles needed = 30.0 / 0.75 = 40.0
            self.assertEqual(40.0, result)

    def test_getCarrotTilesNeededWithBeehive(self) -> None:
        """
        The getCarrotTilesNeeded method must correctly calculate tiles
        needed with beehive modifier applied.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 4
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            mockFactionDataInstance.getBeehiveModifier.return_value = 1.43
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getCarrotTilesNeeded(30.0, True)

            # Production per tile = 3 / 4 = 0.75
            # With beehive = 0.75 * 1.43 = 1.0725
            # Tiles needed = 30.0 / 1.0725 = 27.972027972027973
            self.assertAlmostEqual(27.972027972027973, result)
            mockFactionDataInstance.getBeehiveModifier.assert_called_once()

    def test_getSunflowerTilesNeededNegativeAmount(self) -> None:
        """
        The getSunflowerTilesNeeded method must raise ValueError if
        sunflower seed amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getSunflowerTilesNeeded(-10.0, False)
        self.assertEqual("Sunflower seed amount cannot be negative.",
                         str(context.exception))

    def test_getSunflowerTilesNeededWithoutBeehive(self) -> None:
        """
        The getSunflowerTilesNeeded method must correctly calculate tiles
        needed without beehive modifier.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 5
            mockFactionDataInstance.getCropHarvestYield.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getSunflowerTilesNeeded(20.0, False)

            # Production per tile = 2 / 5 = 0.4
            # Tiles needed = 20.0 / 0.4 = 50.0
            self.assertEqual(50.0, result)

    def test_getSunflowerTilesNeededWithBeehive(self) -> None:
        """
        The getSunflowerTilesNeeded method must correctly calculate tiles
        needed with beehive modifier applied.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 5
            mockFactionDataInstance.getCropHarvestYield.return_value = 2
            mockFactionDataInstance.getBeehiveModifier.return_value = 1.43
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getSunflowerTilesNeeded(20.0, True)

            # Production per tile = 2 / 5 = 0.4
            # With beehive = 0.4 * 1.43 = 0.572
            # Tiles needed = 20.0 / 0.572 = 34.965034965034967
            self.assertAlmostEqual(34.965034965034967, result)
            mockFactionDataInstance.getBeehiveModifier.assert_called_once()

    def test_getPotatoTilesNeededNegativeAmount(self) -> None:
        """
        The getPotatoTilesNeeded method must raise ValueError if potato
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPotatoTilesNeeded(-10.0, False)
        self.assertEqual("Potato amount cannot be negative.",
                         str(context.exception))

    def test_getPotatoTilesNeededWithoutBeehive(self) -> None:
        """
        The getPotatoTilesNeeded method must correctly calculate tiles
        needed without beehive modifier.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 6
            mockFactionDataInstance.getCropHarvestYield.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPotatoTilesNeeded(30.0, False)

            # Production per tile = 1 / 6 = 0.16666...
            # Tiles needed = 30.0 / 0.16666... = 180.0
            self.assertEqual(180.0, result)

    def test_getPotatoTilesNeededWithBeehive(self) -> None:
        """
        The getPotatoTilesNeeded method must correctly calculate tiles
        needed with beehive modifier applied.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 6
            mockFactionDataInstance.getCropHarvestYield.return_value = 1
            mockFactionDataInstance.getBeehiveModifier.return_value = 1.43
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPotatoTilesNeeded(30.0, True)

            # Production per tile = 1 / 6 = 0.16666...
            # With beehive = 0.16666... * 1.43 = 0.238333...
            # Tiles needed = 30.0 / 0.238333... = 125.87412587412588
            self.assertAlmostEqual(125.87412587412588, result)
            mockFactionDataInstance.getBeehiveModifier.assert_called_once()

    def test_getWheatTilesNeededNegativeAmount(self) -> None:
        """
        The getWheatTilesNeeded method must raise ValueError if wheat
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatTilesNeeded(-10.0, False)
        self.assertEqual("Wheat amount cannot be negative.",
                         str(context.exception))

    def test_getWheatTilesNeededWithoutBeehive(self) -> None:
        """
        The getWheatTilesNeeded method must correctly calculate tiles
        needed without beehive.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 10
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWheatTilesNeeded(30.0, False)

            # Production per tile = 3 / 10 = 0.3
            # Tiles needed = 30.0 / 0.3 = 100.0
            self.assertEqual(100.0, result)

    def test_getWheatTilesNeededWithBeehive(self) -> None:
        """
        The getWheatTilesNeeded method must correctly calculate tiles
        needed with beehive.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 10
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            mockFactionDataInstance.getBeehiveModifier.return_value = 1.43
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWheatTilesNeeded(30.0, True)

            # Production per tile = 3 / 10 = 0.3
            # With beehive = 0.3 * 1.43 = 0.429
            # Tiles needed = 30.0 / 0.429 = 69.93006993006993
            self.assertAlmostEqual(69.93006993006993, result)
            mockFactionDataInstance.getBeehiveModifier.assert_called_once()

    def test_getCattailTilesNeededNegativeAmount(self) -> None:
        """
        The getCattailTilesNeeded method must raise ValueError if cattail
        root amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCattailTilesNeeded(-10.0, False)
        self.assertEqual("Cattail root amount cannot be negative.",
                         str(context.exception))

    def test_getCattailTilesNeededWithoutBeehive(self) -> None:
        """
        The getCattailTilesNeeded method must correctly calculate tiles
        needed without beehive.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 8
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getCattailTilesNeeded(30.0, False)

            # Production per tile = 3 / 8 = 0.375
            # Tiles needed = 30.0 / 0.375 = 80.0
            self.assertEqual(80.0, result)

    def test_getCattailTilesNeededWithBeehive(self) -> None:
        """
        The getCattailTilesNeeded method must correctly calculate tiles
        needed with beehive.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 8
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            mockFactionDataInstance.getBeehiveModifier.return_value = 1.43
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getCattailTilesNeeded(30.0, True)

            # Production per tile = 3 / 8 = 0.375
            # With beehive = 0.375 * 1.43 = 0.53625
            # Tiles needed = 30.0 / 0.53625 = 55.94405594405594
            self.assertAlmostEqual(55.94405594405594, result)
            mockFactionDataInstance.getBeehiveModifier.assert_called_once()

    def test_getSpadderdockTilesNeededNegativeAmount(self) -> None:
        """
        The getSpadderdockTilesNeeded method must raise ValueError if
        spadderdock amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getSpadderdockTilesNeeded(-10.0, False)
        self.assertEqual("Spadderdock amount cannot be negative.",
                         str(context.exception))

    def test_getSpadderdockTilesNeededWithoutBeehive(self) -> None:
        """
        The getSpadderdockTilesNeeded method must correctly calculate tiles
        needed without beehive.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 12
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getSpadderdockTilesNeeded(30.0, False)

            # Production per tile = 3 / 12 = 0.25
            # Tiles needed = 30.0 / 0.25 = 120.0
            self.assertEqual(120.0, result)

    def test_getSpadderdockTilesNeededWithBeehive(self) -> None:
        """
        The getSpadderdockTilesNeeded method must correctly calculate tiles
        needed with beehive.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 12
            mockFactionDataInstance.getCropHarvestYield.return_value = 3
            mockFactionDataInstance.getBeehiveModifier.return_value = 1.43
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getSpadderdockTilesNeeded(30.0, True)

            # Production per tile = 3 / 12 = 0.25
            # With beehive = 0.25 * 1.43 = 0.3575
            # Tiles needed = 30.0 / 0.3575 = 83.91608391608392
            self.assertAlmostEqual(83.91608391608392, result)
            mockFactionDataInstance.getBeehiveModifier.assert_called_once()

    def test_getChestnutTilesNeededNegativeAmount(self) -> None:
        """
        The getChestnutTilesNeeded method must raise ValueError if chestnut
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getChestnutTilesNeeded(-10.0)
        self.assertEqual("Chestnut amount cannot be negative.",
                         str(context.exception))

    def test_getChestnutTilesNeededSuccess(self) -> None:
        """
        The getChestnutTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeHarvestTime.return_value = 8
            mockFactionDataInstance.getTreeHarvestYield.return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getChestnutTilesNeeded(30.0)

            # Production per tile = 3 / 8 = 0.375
            # Tiles needed = 30.0 / 0.375 = 80.0
            self.assertEqual(80.0, result)
