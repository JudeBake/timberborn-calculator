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

            # 100 * 2.75 * 1.0 = 275.0 / 5 = ceil(55.0) = 55
            self.assertEqual(55, result)

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
            # Tiles needed = ceil(30.0 / 0.25) = 120
            self.assertEqual(120, result)

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
            # Tiles needed = ceil(30.0 / 0.75) = 40
            self.assertEqual(40, result)

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
            # Tiles needed = ceil(30.0 / 1.0725) = ceil(27.972...) = 28
            self.assertEqual(28, result)
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
            # Tiles needed = ceil(20.0 / 0.4) = 50
            self.assertEqual(50, result)

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
            # Tiles needed = ceil(20.0 / 0.572) = ceil(34.965...) = 35
            self.assertEqual(35, result)
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
            # Tiles needed = ceil(30.0 / 0.16666...) = 180
            self.assertEqual(180, result)

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
            # Tiles needed = ceil(30.0 / 0.238333...) = ceil(125.874...) = 126
            self.assertEqual(126, result)
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
            # Tiles needed = ceil(30.0 / 0.3) = 100
            self.assertEqual(100, result)

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
            # Tiles needed = ceil(30.0 / 0.429) = ceil(69.930...) = 70
            self.assertEqual(70, result)
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
            # Tiles needed = ceil(30.0 / 0.375) = 80
            self.assertEqual(80, result)

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
            # Tiles needed = ceil(30.0 / 0.53625) = ceil(55.944...) = 56
            self.assertEqual(56, result)
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
            # Tiles needed = ceil(30.0 / 0.25) = 120
            self.assertEqual(120, result)

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
            # Tiles needed = ceil(30.0 / 0.3575) = ceil(83.916...) = 84
            self.assertEqual(84, result)
            mockFactionDataInstance.getBeehiveModifier.assert_called_once()

    def test_getLogPerTypeNegativeTotalLogAmount(self) -> None:
        """
        The getLogPerType method must raise ValueError if total log amount
        is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogPerType(-100.0, 3)
        self.assertEqual("Total log amount cannot be negative.",
                         str(context.exception))

    def test_getLogPerTypeZeroTreeTypeCount(self) -> None:
        """
        The getLogPerType method must raise ValueError if tree type count
        is zero.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogPerType(100.0, 0)
        self.assertEqual("Tree type count must be positive.",
                         str(context.exception))

    def test_getLogPerTypeNegativeTreeTypeCount(self) -> None:
        """
        The getLogPerType method must raise ValueError if tree type count
        is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogPerType(100.0, -3)
        self.assertEqual("Tree type count must be positive.",
                         str(context.exception))

    def test_getLogPerTypeSuccess(self) -> None:
        """
        The getLogPerType method must correctly calculate logs per tree type
        by dividing total log amount by the number of tree types.
        """
        with patch('pkgs.factions.folktail.FactionData'):
            folktail = Folktail()
            result = folktail.getLogPerType(100.0, 3)

            # Logs per type = ceil(100.0 / 3) = ceil(33.333...) = 34
            self.assertEqual(34, result)

    def test_getBirchLogTilesNeededNegativeAmount(self) -> None:
        """
        The getBirchLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBirchLogTilesNeeded(-10.0)
        self.assertEqual("Log amount cannot be negative.",
                         str(context.exception))

    def test_getBirchLogTilesNeededSuccess(self) -> None:
        """
        The getBirchLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeGrowthTime.return_value = 15
            mockFactionDataInstance.getTreeLogOutput.return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBirchLogTilesNeeded(30.0)

            # Production per tile = 5 / 15 = 0.333...
            # Tiles needed = ceil(30.0 / 0.333...) = ceil(90.0) = 90
            self.assertEqual(90, result)

    def test_getPineLogTilesNeededNegativeAmount(self) -> None:
        """
        The getPineLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPineLogTilesNeeded(-10.0)
        self.assertEqual("Log amount cannot be negative.",
                         str(context.exception))

    def test_getPineLogTilesNeededSuccess(self) -> None:
        """
        The getPineLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeGrowthTime.return_value = 12
            mockFactionDataInstance.getTreeLogOutput.return_value = 4
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPineLogTilesNeeded(30.0)

            # Production per tile = 4 / 12 = 0.333...
            # Tiles needed = ceil(30.0 / 0.333...) = ceil(90.0) = 90
            self.assertEqual(90, result)

    def test_getPineResinTilesNeededNegativeAmount(self) -> None:
        """
        The getPineResinTilesNeeded method must raise ValueError if pine
        resin amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPineResinTilesNeeded(-10.0)
        self.assertEqual("Pine resin amount cannot be negative.",
                         str(context.exception))

    def test_getPineResinTilesNeededSuccess(self) -> None:
        """
        The getPineResinTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeHarvestTime.return_value = 8
            mockFactionDataInstance.getTreeHarvestYield.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPineResinTilesNeeded(30.0)

            # Production per tile = 2 / 8 = 0.25
            # Tiles needed = ceil(30.0 / 0.25) = 120
            self.assertEqual(120, result)

    def test_getMapleLogTilesNeededNegativeAmount(self) -> None:
        """
        The getMapleLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMapleLogTilesNeeded(-10.0)
        self.assertEqual("Log amount cannot be negative.",
                         str(context.exception))

    def test_getMapleLogTilesNeededSuccess(self) -> None:
        """
        The getMapleLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeGrowthTime.return_value = 18
            mockFactionDataInstance.getTreeLogOutput.return_value = 6
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getMapleLogTilesNeeded(30.0)

            # Production per tile = 6 / 18 = 0.333...
            # Tiles needed = ceil(30.0 / 0.333...) = ceil(90.0) = 90
            self.assertEqual(90, result)

    def test_getMapleSyrupTilesNeededNegativeAmount(self) -> None:
        """
        The getMapleSyrupTilesNeeded method must raise ValueError if maple
        syrup amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMapleSyrupTilesNeeded(-10.0)
        self.assertEqual("Maple syrup amount cannot be negative.",
                         str(context.exception))

    def test_getMapleSyrupTilesNeededSuccess(self) -> None:
        """
        The getMapleSyrupTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeHarvestTime.return_value = 10
            mockFactionDataInstance.getTreeHarvestYield.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getMapleSyrupTilesNeeded(30.0)

            # Production per tile = 2 / 10 = 0.2
            # Tiles needed = ceil(30.0 / 0.2) = 150
            self.assertEqual(150, result)

    def test_getChestnutLogTilesNeededNegativeAmount(self) -> None:
        """
        The getChestnutLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getChestnutLogTilesNeeded(-10.0)
        self.assertEqual("Log amount cannot be negative.",
                         str(context.exception))

    def test_getChestnutLogTilesNeededSuccess(self) -> None:
        """
        The getChestnutLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeGrowthTime.return_value = 20
            mockFactionDataInstance.getTreeLogOutput.return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getChestnutLogTilesNeeded(30.0)

            # Production per tile = 5 / 20 = 0.25
            # Tiles needed = ceil(30.0 / 0.25) = 120
            self.assertEqual(120, result)

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
            # Tiles needed = ceil(30.0 / 0.375) = 80
            self.assertEqual(80, result)

    def test_getOakLogTilesNeededNegativeAmount(self) -> None:
        """
        The getOakLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getOakLogTilesNeeded(-10.0)
        self.assertEqual("Log amount cannot be negative.",
                         str(context.exception))

    def test_getOakLogTilesNeededSuccess(self) -> None:
        """
        The getOakLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getTreeGrowthTime.return_value = 25
            mockFactionDataInstance.getTreeLogOutput.return_value = 8
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getOakLogTilesNeeded(30.0)

            # Production per tile = 8 / 25 = 0.32
            # Tiles needed = ceil(30.0 / 0.32) = ceil(93.75) = 94
            self.assertEqual(94, result)

    def test_getWaterPumpsNeededNegativeAmount(self) -> None:
        """
        The getWaterPumpsNeeded method must raise ValueError if water
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWaterPumpsNeeded(-10.0)
        self.assertEqual("Water amount cannot be negative.",
                         str(context.exception))

    def test_getWaterPumpsNeededSuccess(self) -> None:
        """
        The getWaterPumpsNeeded method must correctly calculate water pumps
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getWaterProductionTime.return_value = 2.0
            mockFactionDataInstance.getWaterOutputQuantity.return_value = 24
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWaterPumpsNeeded(50.0)

            # Production per pump per day = (24 / 2.0) * 24 = 288.0
            # Pumps needed = ceil(50.0 / 288.0) = ceil(0.173...) = 1
            self.assertEqual(1, result)

    def test_getLargeWaterPumpsNeededNegativeWaterAmount(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must raise ValueError if water
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLargeWaterPumpsNeeded(-10.0, 2)
        self.assertEqual("Water amount cannot be negative.",
                         str(context.exception))

    def test_getLargeWaterPumpsNeededNegativeWorkersCount(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must raise ValueError if workers
        count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLargeWaterPumpsNeeded(50.0, -1)
        self.assertEqual("Workers count cannot be negative.",
                         str(context.exception))

    def test_getLargeWaterPumpsNeededExceedsMaxWorkers(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must raise ValueError if workers
        count exceeds maximum.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getWaterWorkers.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            with self.assertRaises(ValueError) as context:
                folktail.getLargeWaterPumpsNeeded(50.0, 5)
            self.assertEqual("Workers count cannot exceed 2.",
                             str(context.exception))

    def test_getLargeWaterPumpsNeededSuccessFullWorkers(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must correctly calculate pumps
        needed with full workers.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getWaterWorkers.return_value = 2
            mockFactionDataInstance.getWaterProductionTime.return_value = 2.0
            mockFactionDataInstance.getWaterOutputQuantity.return_value = 48
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLargeWaterPumpsNeeded(50.0, 2)

            # Effective output = 48 * (2 / 2) = 48
            # Production per pump per day = (48 / 2.0) * 24 = 576.0
            # Pumps needed = ceil(50.0 / 576.0) = ceil(0.086...) = 1
            self.assertEqual(1, result)

    def test_getLargeWaterPumpsNeededSuccessReducedWorkers(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must correctly calculate pumps
        needed with reduced workers.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getWaterWorkers.return_value = 2
            mockFactionDataInstance.getWaterProductionTime.return_value = 2.0
            mockFactionDataInstance.getWaterOutputQuantity.return_value = 48
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLargeWaterPumpsNeeded(50.0, 1)

            # Effective output = 48 * (1 / 2) = 24
            # Production per pump per day = (24 / 2.0) * 24 = 288.0
            # Pumps needed = ceil(50.0 / 288.0) = ceil(0.173...) = 1
            self.assertEqual(1, result)

    def test_getBadwaterPumpsNeededNegativeAmount(self) -> None:
        """
        The getBadwaterPumpsNeeded method must raise ValueError if water
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBadwaterPumpsNeeded(-10.0)
        self.assertEqual("Water amount cannot be negative.",
                         str(context.exception))

    def test_getBadwaterPumpsNeededSuccess(self) -> None:
        """
        The getBadwaterPumpsNeeded method must correctly calculate badwater
        pumps needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getWaterProductionTime.return_value = 3.0
            mockFactionDataInstance.getWaterOutputQuantity.return_value = 18
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBadwaterPumpsNeeded(40.0)

            # Production per pump per day = (18 / 3.0) * 24 = 144.0
            # Pumps needed = ceil(40.0 / 144.0) = ceil(0.277...) = 1
            self.assertEqual(1, result)

    def test_getGrillsNeededForPotatoesNegativeAmount(self) -> None:
        """
        The getGrillsNeededForPotatoes method must raise ValueError if
        grilled potato amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGrillsNeededForPotatoes(-10.0)
        self.assertEqual("Grilled potato amount cannot be negative.",
                         str(context.exception))

    def test_getGrillsNeededForPotatoesSuccess(self) -> None:
        """
        The getGrillsNeededForPotatoes method must correctly calculate grills
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.52
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 4
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGrillsNeededForPotatoes(200.0)

            # Production per grill per day = (4 / 0.52) * 24 = 184.615...
            # Grills needed = ceil(200.0 / 184.615...) = ceil(1.083...) = 2
            self.assertEqual(2, result)

    def test_getPotatoesNeededForGrillsNegativeCount(self) -> None:
        """
        The getPotatoesNeededForGrills method must raise ValueError if
        grills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPotatoesNeededForGrills(-1)
        self.assertEqual("Grills count cannot be negative.",
                         str(context.exception))

    def test_getPotatoesNeededForGrillsSuccess(self) -> None:
        """
        The getPotatoesNeededForGrills method must correctly calculate
        potatoes needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.52
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPotatoesNeededForGrills(3)

            # Cycles per day = 24 / 0.52 = 46.153...
            # Potatoes per grill per day = 1 * 46.153... = 46.153...
            # Total potatoes = 3 * 46.153... = 138.461...
            # Ceiling = 139
            self.assertEqual(139, result)

    def test_getLogsNeededForGrillsWithPotatoesNegativeCount(self) -> None:
        """
        The getLogsNeededForGrillsWithPotatoes method must raise ValueError
        if grills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForGrillsWithPotatoes(-1)
        self.assertEqual("Grills count cannot be negative.",
                         str(context.exception))

    def test_getLogsNeededForGrillsWithPotatoesSuccess(self) -> None:
        """
        The getLogsNeededForGrillsWithPotatoes method must correctly
        calculate logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.52
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 0.1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForGrillsWithPotatoes(3)

            # Cycles per day = 24 / 0.52 = 46.153...
            # Logs per grill per day = 0.1 * 46.153... = 4.615...
            # Total logs = 3 * 4.615... = 13.846...
            self.assertAlmostEqual(13.846153846153847, result, places=10)

    def test_getChestnutsNeededForGrillsNegativeCount(self) -> None:
        """
        The getChestnutsNeededForGrills method must raise ValueError if
        grills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getChestnutsNeededForGrills(-1)
        self.assertEqual("Grills count cannot be negative.",
                         str(context.exception))

    def test_getChestnutsNeededForGrillsSuccess(self) -> None:
        """
        The getChestnutsNeededForGrills method must correctly calculate
        chestnuts needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.33
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getChestnutsNeededForGrills(3)

            # Cycles per day = 24 / 0.33 = 72.727...
            # Chestnuts per grill per day = 1 * 72.727... = 72.727...
            # Total chestnuts = 3 * 72.727... = 218.181...
            # Ceiling = 219
            self.assertEqual(219, result)

    def test_getLogsNeededForGrillsWithChestnutsNegativeCount(self) -> None:
        """
        The getLogsNeededForGrillsWithChestnuts method must raise ValueError
        if grills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForGrillsWithChestnuts(-1)
        self.assertEqual("Grills count cannot be negative.",
                         str(context.exception))

    def test_getLogsNeededForGrillsWithChestnutsSuccess(self) -> None:
        """
        The getLogsNeededForGrillsWithChestnuts method must correctly
        calculate logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.33
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 0.1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForGrillsWithChestnuts(3)

            # Cycles per day = 24 / 0.33 = 72.727...
            # Logs per grill per day = 0.1 * 72.727... = 7.272...
            # Total logs = 3 * 7.272... = 21.818...
            self.assertAlmostEqual(21.818181818181817, result, places=10)

    def test_getGrillsNeededForSpadderdocksNegativeAmount(self) -> None:
        """
        The getGrillsNeededForSpadderdocks method must raise ValueError if
        grilled spadderdock amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGrillsNeededForSpadderdocks(-10.0)
        self.assertEqual("Grilled spadderdock amount cannot be negative.",
                         str(context.exception))

    def test_getGrillsNeededForSpadderdocksSuccess(self) -> None:
        """
        The getGrillsNeededForSpadderdocks method must correctly calculate
        grills needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 2
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.25
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGrillsNeededForSpadderdocks(300.0)

            # Production per grill per day = (3 / 0.25) * 24 = 288.0
            # Grills needed = ceil(300.0 / 288.0) = ceil(1.041...) = 2
            self.assertEqual(2, result)

    def test_getSpadderdocksNeededForGrillsNegativeCount(self) -> None:
        """
        The getSpadderdocksNeededForGrills method must raise ValueError if
        grills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getSpadderdocksNeededForGrills(-1)
        self.assertEqual("Grills count cannot be negative.",
                         str(context.exception))

    def test_getSpadderdocksNeededForGrillsSuccess(self) -> None:
        """
        The getSpadderdocksNeededForGrills method must correctly calculate
        spadderdocks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 2
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.25
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getSpadderdocksNeededForGrills(3)

            # Cycles per day = 24 / 0.25 = 96.0
            # Spadderdocks per grill per day = 2 * 96.0 = 192.0
            # Total spadderdocks = 3 * 192.0 = 576.0
            # Ceiling = 576
            self.assertEqual(576, result)

    def test_getLogsNeededForGrillsWithSpadderdocksNegativeCount(self) -> None:
        """
        The getLogsNeededForGrillsWithSpadderdocks method must raise
        ValueError if grills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForGrillsWithSpadderdocks(-1)
        self.assertEqual("Grills count cannot be negative.",
                         str(context.exception))

    def test_getLogsNeededForGrillsWithSpadderdocksSuccess(self) -> None:
        """
        The getLogsNeededForGrillsWithSpadderdocks method must correctly
        calculate logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 2
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.25
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 0.15
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForGrillsWithSpadderdocks(3)

            # Cycles per day = 24 / 0.25 = 96.0
            # Logs per grill per day = 0.15 * 96.0 = 14.4
            # Total logs = 3 * 14.4 = 43.2
            self.assertAlmostEqual(43.2, result, places=10)

    def test_getGristmillsNeededForWheatFlourNegativeAmount(self) -> None:
        """
        The getGristmillsNeededForWheatFlour method must raise ValueError if
        wheat flour amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGristmillsNeededForWheatFlour(-10.0)
        self.assertEqual("Wheat flour amount cannot be negative.",
                         str(context.exception))

    def test_getGristmillsNeededForWheatFlourSuccess(self) -> None:
        """
        The getGristmillsNeededForWheatFlour method must correctly calculate
        gristmills needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.5
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGristmillsNeededForWheatFlour(50.0)

            # Production per gristmill per day = (1 / 0.5) * 24 = 48.0
            # Gristmills needed = ceil(50.0 / 48.0) = ceil(1.041...) = 2
            self.assertEqual(2, result)

    def test_getWheatNeededForGristmillsNegativeCount(self) -> None:
        """
        The getWheatNeededForGristmills method must raise ValueError if
        gristmills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatNeededForGristmills(-1)
        self.assertEqual("Gristmills count cannot be negative.",
                         str(context.exception))

    def test_getWheatNeededForGristmillsSuccess(self) -> None:
        """
        The getWheatNeededForGristmills method must correctly calculate wheat
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.5
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWheatNeededForGristmills(3)

            # Cycles per day = 24 / 0.5 = 48.0
            # Wheat per gristmill per day = 1 * 48.0 = 48.0
            # Total wheat = 3 * 48.0 = 144.0
            # Ceiling = 144
            self.assertEqual(144, result)

    def test_getGristmillsNeededForCattailFlourNegativeAmount(self) -> None:
        """
        The getGristmillsNeededForCattailFlour method must raise ValueError if
        cattail flour amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGristmillsNeededForCattailFlour(-10.0)
        self.assertEqual("Cattail flour amount cannot be negative.",
                         str(context.exception))

    def test_getGristmillsNeededForCattailFlourSuccess(self) -> None:
        """
        The getGristmillsNeededForCattailFlour method must correctly calculate
        gristmills needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.25
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGristmillsNeededForCattailFlour(100.0)

            # Production per gristmill per day = (1 / 0.25) * 24 = 96.0
            # Gristmills needed = ceil(100.0 / 96.0) = ceil(1.041...) = 2
            self.assertEqual(2, result)

    def test_getCattailRootsNeededForGristmillsNegativeCount(self) -> None:
        """
        The getCattailRootsNeededForGristmills method must raise ValueError if
        gristmills count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCattailRootsNeededForGristmills(-1)
        self.assertEqual("Gristmills count cannot be negative.",
                         str(context.exception))

    def test_getCattailRootsNeededForGristmillsSuccess(self) -> None:
        """
        The getCattailRootsNeededForGristmills method must correctly calculate
        cattail roots needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.25
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getCattailRootsNeededForGristmills(3)

            # Cycles per day = 24 / 0.25 = 96.0
            # Cattail roots per gristmill per day = 1 * 96.0 = 96.0
            # Total cattail roots = 3 * 96.0 = 288.0
            # Ceiling = 288
            self.assertEqual(288, result)

    def test_getBakeriesNeededForBreadsNegativeAmount(self) -> None:
        """
        The getBakeriesNeededForBreads method must raise ValueError if breads
        amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBakeriesNeededForBreads(-10.0)
        self.assertEqual("Breads amount cannot be negative.",
                         str(context.exception))

    def test_getBakeriesNeededForBreadsSuccess(self) -> None:
        """
        The getBakeriesNeededForBreads method must correctly calculate
        bakeries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.42
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBakeriesNeededForBreads(300.0)

            # Production per bakery per day = (5 / 0.42) * 24 = 285.714...
            # Bakeries needed = ceil(300.0 / 285.714...) = ceil(1.05) = 2
            self.assertEqual(2, result)

    def test_getWheatFlourNeededForBakeriesWithBreadsNegativeCount(
            self) -> None:
        """
        The getWheatFlourNeededForBakeriesWithBreads method must raise
        ValueError if bakeries count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatFlourNeededForBakeriesWithBreads(-1)
        self.assertEqual("Bakeries count cannot be negative.",
                         str(context.exception))

    def test_getWheatFlourNeededForBakeriesWithBreadsSuccess(self) -> None:
        """
        The getWheatFlourNeededForBakeriesWithBreads method must correctly
        calculate wheat flour needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.42
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWheatFlourNeededForBakeriesWithBreads(3)

            # Cycles per day = 24 / 0.42 = 57.142...
            # Wheat flour per bakery per day = 1 * 57.142... = 57.142...
            # Total wheat flour = 3 * 57.142... = 171.428...
            # Ceiling = 172
            self.assertEqual(172, result)

    def test_getLogsNeededForBakeriesWithBreadsNegativeCount(self) -> None:
        """
        The getLogsNeededForBakeriesWithBreads method must raise ValueError
        if bakeries count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForBakeriesWithBreads(-1)
        self.assertEqual("Bakeries count cannot be negative.",
                         str(context.exception))

    def test_getLogsNeededForBakeriesWithBreadsSuccess(self) -> None:
        """
        The getLogsNeededForBakeriesWithBreads method must correctly calculate
        logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 0
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.42
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 0.1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForBakeriesWithBreads(3)

            # Cycles per day = 24 / 0.42 = 57.142...
            # Logs per bakery per day = 0.1 * 57.142... = 5.714...
            # Total logs = 3 * 5.714... = 17.142...
            self.assertAlmostEqual(17.142857142857142, result, places=10)

    def test_getBakeriesNeededForCattailCrackersNegativeAmount(self) -> None:
        """
        The getBakeriesNeededForCattailCrackers method must raise ValueError
        if cattail crackers amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBakeriesNeededForCattailCrackers(-10.0)
        self.assertEqual("Cattail crackers amount cannot be negative.",
                         str(context.exception))

    def test_getBakeriesNeededForCattailCrackersSuccess(self) -> None:
        """
        The getBakeriesNeededForCattailCrackers method must correctly
        calculate bakeries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.5
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 4
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBakeriesNeededForCattailCrackers(200.0)

            # Production per bakery per day = (4 / 0.5) * 24 = 192.0
            # Bakeries needed = ceil(200.0 / 192.0) = ceil(1.041...) = 2
            self.assertEqual(2, result)

    def test_getCattailFlourNeededForBakeriesWithCattailCrackersNegativeCount(
            self) -> None:
        """
        The getCattailFlourNeededForBakeriesWithCattailCrackers method must
        raise ValueError if bakeries count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCattailFlourNeededForBakeriesWithCattailCrackers(-1)
        self.assertEqual("Bakeries count cannot be negative.",
                         str(context.exception))

    def test_getCattailFlourNeededForBakeriesWithCattailCrackersSuccess(
            self) -> None:
        """
        The getCattailFlourNeededForBakeriesWithCattailCrackers method must
        correctly calculate cattail flour needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.5
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getCattailFlourNeededForBakeriesWithCattailCrackers(3)

            # Cycles per day = 24 / 0.5 = 48.0
            # Cattail flour per bakery per day = 1 * 48.0 = 48.0
            # Total cattail flour = 3 * 48.0 = 144.0
            # Ceiling = 144
            self.assertEqual(144, result)

    def test_getLogsNeededForBakeriesWithCattailCrackersNegativeCount(
            self) -> None:
        """
        The getLogsNeededForBakeriesWithCattailCrackers method must raise
        ValueError if bakeries count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForBakeriesWithCattailCrackers(-1)
        self.assertEqual("Bakeries count cannot be negative.",
                         str(context.exception))

    def test_getLogsNeededForBakeriesWithCattailCrackersSuccess(self) -> None:
        """
        The getLogsNeededForBakeriesWithCattailCrackers method must correctly
        calculate logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.5
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 0.1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForBakeriesWithCattailCrackers(3)

            # Cycles per day = 24 / 0.5 = 48.0
            # Logs per bakery per day = 0.1 * 48.0 = 4.8
            # Total logs = 3 * 4.8 = 14.4
            self.assertAlmostEqual(14.4, result, places=10)

    def test_getBakeriesNeededForMaplePastriesNegativeAmount(self) -> None:
        """
        The getBakeriesNeededForMaplePastries method must raise ValueError
        if maple pastries amount is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBakeriesNeededForMaplePastries(-10.0)
        self.assertEqual("Maple pastries amount cannot be negative.",
                         str(context.exception))

    def test_getBakeriesNeededForMaplePastriesSuccess(self) -> None:
        """
        The getBakeriesNeededForMaplePastries method must correctly calculate
        bakeries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 2
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.55
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBakeriesNeededForMaplePastries(140.0)

            # Production per bakery per day = (3 / 0.55) * 24 = 130.909...
            # Bakeries needed = ceil(140.0 / 130.909...) = ceil(1.069...) = 2
            self.assertEqual(2, result)

    def test_getWheatFlourNeededForBakeriesWithMaplePastriesNegativeCount(
            self) -> None:
        """
        The getWheatFlourNeededForBakeriesWithMaplePastries method must raise
        ValueError if bakeries count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatFlourNeededForBakeriesWithMaplePastries(-1)
        self.assertEqual("Bakeries count cannot be negative.",
                         str(context.exception))

    def test_getWheatFlourNeededForBakeriesWithMaplePastriesSuccess(
            self) -> None:
        """
        The getWheatFlourNeededForBakeriesWithMaplePastries method must
        correctly calculate wheat flour needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 2
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.55
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getWheatFlourNeededForBakeriesWithMaplePastries(3)

            # Cycles per day = 24 / 0.55 = 43.636...
            # Wheat flour per bakery per day = 1 * 43.636... = 43.636...
            # Total wheat flour = 3 * 43.636... = 130.909...
            # Ceiling = 131
            self.assertEqual(131, result)

    def test_getMapleSyrupNeededForBakeriesWithMaplePastriesNegativeCount(
            self) -> None:
        """
        The getMapleSyrupNeededForBakeriesWithMaplePastries method must raise
        ValueError if bakeries count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMapleSyrupNeededForBakeriesWithMaplePastries(-1)
        self.assertEqual("Bakeries count cannot be negative.",
                         str(context.exception))

    def test_getMapleSyrupNeededForBakeriesWithMaplePastriesSuccess(
            self) -> None:
        """
        The getMapleSyrupNeededForBakeriesWithMaplePastries method must
        correctly calculate maple syrup needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 2
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.55
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getMapleSyrupNeededForBakeriesWithMaplePastries(3)

            # Cycles per day = 24 / 0.55 = 43.636...
            # Maple syrup per bakery per day = 1 * 43.636... = 43.636...
            # Total maple syrup = 3 * 43.636... = 130.909...
            # Ceiling = 131
            self.assertEqual(131, result)

    def test_getLogsNeededForBakeriesWithMaplePastriesNegativeCount(
            self) -> None:
        """
        The getLogsNeededForBakeriesWithMaplePastries method must raise
        ValueError if bakeries count is negative.
        """
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForBakeriesWithMaplePastries(-1)
        self.assertEqual("Bakeries count cannot be negative.",
                         str(context.exception))

    def test_getLogsNeededForBakeriesWithMaplePastriesSuccess(self) -> None:
        """
        The getLogsNeededForBakeriesWithMaplePastries method must correctly
        calculate logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 2
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.55
            mockFactionDataInstance.getFoodProcessingInputQuantity \
                .return_value = 0.1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForBakeriesWithMaplePastries(3)

            # Cycles per day = 24 / 0.55 = 43.636...
            # Logs per bakery per day = 0.1 * 43.636... = 4.363...
            # Total logs = 3 * 4.363... = 13.090...
            self.assertAlmostEqual(13.090909090909092, result, places=10)
