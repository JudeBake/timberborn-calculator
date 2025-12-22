from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.factions.folktail import Folktail                     # noqa: E402
from pkgs.data.enumerators import DifficultyLevel               # noqa: E402


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
        errMsg = "Population cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getDailyFoodConsumption(-1, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

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
            mockFactionDataInstance.getDifficultyModifier \
                .assert_called_once_with(DifficultyLevel.NORMAL)

    def test_getDailyWaterConsumptionNegativePopulation(self) -> None:
        """
        The getDailyWaterConsumption method must raise ValueError if
        population is negative.
        """
        errMsg = "Population cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getDailyWaterConsumption(-1, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

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
            mockFactionDataInstance.getDifficultyModifier \
                .assert_called_once_with(DifficultyLevel.NORMAL)

    def test_getFoodPerTypeNegativePopulation(self) -> None:
        """
        The getFoodPerType method must raise ValueError if population is
        negative.
        """
        errMsg = "Population cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getFoodPerType(-1, 5, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodPerTypeZeroFoodTypeCount(self) -> None:
        """
        The getFoodPerType method must raise ValueError if foodTypeCount is
        zero.
        """
        errMsg = "Food type count must be positive."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getFoodPerType(100, 0, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getFoodPerTypeNegativeFoodTypeCount(self) -> None:
        """
        The getFoodPerType method must raise ValueError if foodTypeCount is
        negative.
        """
        errMsg = "Food type count must be positive."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getFoodPerType(100, -5, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg,
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
        errMsg = "Berry amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBerryTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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

    def test_getDandelionTilesNeededNegativeAmount(self) -> None:
        """
        The getDandelionTilesNeeded method must raise ValueError if dandelion
        amount is negative.
        """
        errMsg = "Dandelion amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getDandelionTilesNeeded(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getDandelionTilesNeededSuccess(self) -> None:
        """
        The getDandelionTilesNeeded method must correctly calculate tiles
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getCropHarvestTime.return_value = 3
            mockFactionDataInstance.getCropHarvestYield.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getDandelionTilesNeeded(10.0)

            # Production per tile = 1 / 3 = 0.333...
            # Tiles needed = ceil(10.0 / 0.333...) = ceil(30) = 30
            self.assertEqual(30, result)

    def test_getCarrotTilesNeededNegativeAmount(self) -> None:
        """
        The getCarrotTilesNeeded method must raise ValueError if carrot
        amount is negative.
        """
        errMsg = "Carrot amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCarrotTilesNeeded(-10.0, False)
        self.assertEqual(errMsg,
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
        errMsg = "Sunflower seed amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getSunflowerTilesNeeded(-10.0, False)
        self.assertEqual(errMsg,
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
        errMsg = "Potato amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPotatoTilesNeeded(-10.0, False)
        self.assertEqual(errMsg,
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
        errMsg = "Wheat amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatTilesNeeded(-10.0, False)
        self.assertEqual(errMsg,
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
        errMsg = "Cattail root amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCattailTilesNeeded(-10.0, False)
        self.assertEqual(errMsg,
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
        errMsg = "Spadderdock amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getSpadderdockTilesNeeded(-10.0, False)
        self.assertEqual(errMsg,
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
        errMsg = "Total log amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogPerType(-100.0, 3)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLogPerTypeZeroTreeTypeCount(self) -> None:
        """
        The getLogPerType method must raise ValueError if tree type count
        is zero.
        """
        errMsg = "Tree type count must be positive."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogPerType(100.0, 0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLogPerTypeNegativeTreeTypeCount(self) -> None:
        """
        The getLogPerType method must raise ValueError if tree type count
        is negative.
        """
        errMsg = "Tree type count must be positive."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogPerType(100.0, -3)
        self.assertEqual(errMsg,
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
        errMsg = "Log amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBirchLogTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Log amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPineLogTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Pine resin amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPineResinTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Log amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMapleLogTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Maple syrup amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMapleSyrupTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Log amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getChestnutLogTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Chestnut amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getChestnutTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Log amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getOakLogTilesNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Water amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWaterPumpsNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Water amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLargeWaterPumpsNeeded(-10.0, 2)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLargeWaterPumpsNeededNegativeWorkersCount(self) -> None:
        """
        The getLargeWaterPumpsNeeded method must raise ValueError if workers
        count is negative.
        """
        errMsg = "Workers count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLargeWaterPumpsNeeded(50.0, -1)
        self.assertEqual(errMsg,
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
            errMsg = "Workers count cannot exceed 2."
            with self.assertRaises(ValueError) as context:
                folktail.getLargeWaterPumpsNeeded(50.0, 5)
            self.assertEqual(errMsg,
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
        errMsg = "Water amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBadwaterPumpsNeeded(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Grilled potato amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGrillsNeededForPotatoes(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Grills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPotatoesNeededForGrills(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Grills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForGrillsWithPotatoes(-1)
        self.assertEqual(errMsg,
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

    def test_getGrillsNeededForChestnutsNegativeAmount(self) -> None:
        """
        The getGrillsNeededForChestnuts method must raise ValueError if
        grilled chestnut amount is negative.
        """
        errMsg = "Grilled chestnut amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGrillsNeededForChestnuts(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getGrillsNeededForChestnutsSuccess(self) -> None:
        """
        The getGrillsNeededForChestnuts method must correctly calculate
        grills needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getFoodProcessingRecipeIndex \
                .return_value = 1
            mockFactionDataInstance.getFoodProcessingProductionTime \
                .return_value = 0.33
            mockFactionDataInstance.getFoodProcessingOutputQuantity \
                .return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGrillsNeededForChestnuts(400.0)

            # Production per grill per day = (5 / 0.33) * 24 = 363.636...
            # Grills needed = ceil(400.0 / 363.636...) = ceil(1.1) = 2
            self.assertEqual(2, result)

    def test_getChestnutsNeededForGrillsNegativeCount(self) -> None:
        """
        The getChestnutsNeededForGrills method must raise ValueError if
        grills count is negative.
        """
        errMsg = "Grills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getChestnutsNeededForGrills(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Grills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForGrillsWithChestnuts(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Grilled spadderdock amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGrillsNeededForSpadderdocks(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Grills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getSpadderdocksNeededForGrills(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Grills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForGrillsWithSpadderdocks(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Wheat flour amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGristmillsNeededForWheatFlour(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Gristmills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatNeededForGristmills(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Cattail flour amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGristmillsNeededForCattailFlour(-10.0)
        self.assertEqual(errMsg,
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
        errMsg = "Gristmills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCattailRootsNeededForGristmills(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Breads amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBakeriesNeededForBreads(-10.0)
        self.assertEqual(errMsg,
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

    def test_getWheatFlourNeededForBakeriesWithBreadsNegativeCount(self) -> None:   # noqa: E501
        """
        The getWheatFlourNeededForBakeriesWithBreads method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatFlourNeededForBakeriesWithBreads(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Bakeries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForBakeriesWithBreads(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Cattail crackers amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBakeriesNeededForCattailCrackers(-10.0)
        self.assertEqual(errMsg,
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

    def test_getCattailFlourNeededForBakeriesWithCattailCrackersNegativeCount(self) -> None:    # noqa: E501
        """
        The getCattailFlourNeededForBakeriesWithCattailCrackers method must
        raise ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCattailFlourNeededForBakeriesWithCattailCrackers(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getCattailFlourNeededForBakeriesWithCattailCrackersSuccess(self) -> None:  # noqa: E501
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

    def test_getLogsNeededForBakeriesWithCattailCrackersNegativeCount(self) -> None:    # noqa: E501
        """
        The getLogsNeededForBakeriesWithCattailCrackers method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForBakeriesWithCattailCrackers(-1)
        self.assertEqual(errMsg,
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
        errMsg = "Maple pastries amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBakeriesNeededForMaplePastries(-10.0)
        self.assertEqual(errMsg,
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

    def test_getWheatFlourNeededForBakeriesWithMaplePastriesNegativeCount(self) -> None:    # noqa: E501
        """
        The getWheatFlourNeededForBakeriesWithMaplePastries method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWheatFlourNeededForBakeriesWithMaplePastries(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getWheatFlourNeededForBakeriesWithMaplePastriesSuccess(self) -> None:  # noqa: E501
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

    def test_getMapleSyrupNeededForBakeriesWithMaplePastriesNegativeCount(self) -> None:    # noqa: E501
        """
        The getMapleSyrupNeededForBakeriesWithMaplePastries method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMapleSyrupNeededForBakeriesWithMaplePastries(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getMapleSyrupNeededForBakeriesWithMaplePastriesSuccess(self) -> None:  # noqa: E501
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

    def test_getLogsNeededForBakeriesWithMaplePastriesNegativeCount(self) -> None:  # noqa: E501
        """
        The getLogsNeededForBakeriesWithMaplePastries method must raise
        ValueError if bakeries count is negative.
        """
        errMsg = "Bakeries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForBakeriesWithMaplePastries(-1)
        self.assertEqual(errMsg,
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

    def test_getLumberMillsNeededForPlanksNegativeAmount(self) -> None:
        """
        The getLumberMillsNeededForPlanks method must raise ValueError if
        planks amount is negative.
        """
        errMsg = "Planks amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLumberMillsNeededForPlanks(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLumberMillsNeededForPlanksSuccess(self) -> None:
        """
        The getLumberMillsNeededForPlanks method must correctly calculate
        lumber mills needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.3
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLumberMillsNeededForPlanks(20.0)

            # Production per lumber mill per day = (1 / 1.3) * 24 = 18.461...
            # Lumber mills needed = ceil(20.0 / 18.461...) = ceil(1.083...) = 2
            self.assertEqual(2, result)

    def test_getLogsNeededForLumberMillsNegativeCount(self) -> None:
        """
        The getLogsNeededForLumberMills method must raise ValueError if
        lumber mills count is negative.
        """
        errMsg = "Lumber mills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForLumberMills(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLogsNeededForLumberMillsSuccess(self) -> None:
        """
        The getLogsNeededForLumberMills method must correctly calculate logs
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.3
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForLumberMills(3)

            # Cycles per day = 24 / 1.3 = 18.461...
            # Logs per lumber mill per day = 1 * 18.461... = 18.461...
            # Total logs = 3 * 18.461... = 55.384...
            # Ceiling = 56
            self.assertEqual(56, result)

    # Test Cases for Gear Workshop
    def test_getGearWorkshopsNeededForGearsNegativeAmount(self) -> None:
        """
        The getGearWorkshopsNeededForGears method must raise ValueError if
        gears amount is negative.
        """
        errMsg = "Gears amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGearWorkshopsNeededForGears(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getGearWorkshopsNeededForGearsSuccess(self) -> None:
        """
        The getGearWorkshopsNeededForGears method must correctly calculate
        gear workshops needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGearWorkshopsNeededForGears(50.0)

            # Production per gear workshop per day = (1 / 3.0) * 24 = 8
            # Gear workshops needed = ceil(50.0 / 8) = ceil(6.25) = 7
            self.assertEqual(7, result)

    def test_getPlanksNeededForGearWorkshopsNegativeCount(self) -> None:
        """
        The getPlanksNeededForGearWorkshops method must raise ValueError if
        gear workshops count is negative.
        """
        errMsg = "Gear workshops count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPlanksNeededForGearWorkshops(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPlanksNeededForGearWorkshopsSuccess(self) -> None:
        """
        The getPlanksNeededForGearWorkshops method must correctly calculate
        planks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPlanksNeededForGearWorkshops(3)

            # Cycles per day = 24 / 3.0 = 8
            # Planks per gear workshop per day = 1 * 8 = 8
            # Total planks = 3 * 8 = 24
            self.assertEqual(24, result)

    # Test Cases for Paper Mill
    def test_getPaperMillsNeededForPaperNegativeAmount(self) -> None:
        """
        The getPaperMillsNeededForPaper method must raise ValueError if
        paper amount is negative.
        """
        errMsg = "Paper amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPaperMillsNeededForPaper(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPaperMillsNeededForPaperSuccess(self) -> None:
        """
        The getPaperMillsNeededForPaper method must correctly calculate
        paper mills needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.6
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPaperMillsNeededForPaper(100.0)

            # Production per paper mill per day = (2 / 1.6) * 24 = 30
            # Paper mills needed = ceil(100.0 / 30) = ceil(3.333...) = 4
            self.assertEqual(4, result)

    def test_getLogsNeededForPaperMillsNegativeCount(self) -> None:
        """
        The getLogsNeededForPaperMills method must raise ValueError if
        paper mills count is negative.
        """
        errMsg = "Paper mills count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForPaperMills(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLogsNeededForPaperMillsSuccess(self) -> None:
        """
        The getLogsNeededForPaperMills method must correctly calculate
        logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.6
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForPaperMills(2)

            # Cycles per day = 24 / 1.6 = 15
            # Logs per paper mill per day = 1 * 15 = 15
            # Total logs = 2 * 15 = 30
            self.assertEqual(30, result)

    # Test Cases for Printing Press - Books
    def test_getPrintingPressesNeededForBooksNegativeAmount(self) -> None:
        """
        The getPrintingPressesNeededForBooks method must raise ValueError if
        books amount is negative.
        """
        errMsg = "Books amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPrintingPressesNeededForBooks(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPrintingPressesNeededForBooksSuccess(self) -> None:
        """
        The getPrintingPressesNeededForBooks method must correctly calculate
        printing presses needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.5
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPrintingPressesNeededForBooks(20.0)

            # Production per printing press per day = (1 / 1.5) * 24 = 16
            # Printing presses needed = ceil(20.0 / 16) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getPaperNeededForPrintingPressesWithBooksNegativeCount(self) -> None:  # noqa: E501
        """
        The getPaperNeededForPrintingPressesWithBooks method must raise
        ValueError if printing presses count is negative.
        """
        errMsg = "Printing presses count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPaperNeededForPrintingPressesWithBooks(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPaperNeededForPrintingPressesWithBooksSuccess(self) -> None:
        """
        The getPaperNeededForPrintingPressesWithBooks method must correctly
        calculate paper needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.5
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPaperNeededForPrintingPressesWithBooks(2)

            # Cycles per day = 24 / 1.5 = 16
            # Paper per printing press per day = 2 * 16 = 32
            # Total paper = 2 * 32 = 64
            self.assertEqual(64, result)

    # Test Cases for Printing Press - Punchcards
    def test_getPrintingPressesNeededForPunchcardsNegativeAmount(self) -> None:     # noqa: E501
        """
        The getPrintingPressesNeededForPunchcards method must raise ValueError
        if punchcards amount is negative.
        """
        errMsg = "Punchcards amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPrintingPressesNeededForPunchcards(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPrintingPressesNeededForPunchcardsSuccess(self) -> None:
        """
        The getPrintingPressesNeededForPunchcards method must correctly
        calculate printing presses needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 0.75
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPrintingPressesNeededForPunchcards(50.0)

            # Production per printing press per day = (2 / 0.75) * 24 = 64
            # Printing presses needed = ceil(50.0 / 64) = ceil(0.78125) = 1
            self.assertEqual(1, result)

    def test_getPaperNeededForPrintingPressesWithPunchcardsNegativeCount(self) -> None:     # noqa: E501
        """
        The getPaperNeededForPrintingPressesWithPunchcards method must raise
        ValueError if printing presses count is negative.
        """
        errMsg = "Printing presses count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPaperNeededForPrintingPressesWithPunchcards(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPaperNeededForPrintingPressesWithPunchcardsSuccess(self) -> None:   # noqa: E501
        """
        The getPaperNeededForPrintingPressesWithPunchcards method must
        correctly calculate paper needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 0.75
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPaperNeededForPrintingPressesWithPunchcards(2)

            # Cycles per day = 24 / 0.75 = 32
            # Paper per printing press per day = 2 * 32 = 64
            # Total paper = 2 * 64 = 128
            self.assertEqual(128, result)

    def test_getPlanksNeededForPrintingPressesWithPunchcardsNegativeCount(self) -> None:    # noqa: E501
        """
        The getPlanksNeededForPrintingPressesWithPunchcards method must raise
        ValueError if printing presses count is negative.
        """
        errMsg = "Printing presses count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPlanksNeededForPrintingPressesWithPunchcards(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPlanksNeededForPrintingPressesWithPunchcardsSuccess(self) -> None:  # noqa: E501
        """
        The getPlanksNeededForPrintingPressesWithPunchcards method must
        correctly calculate planks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 0.75
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getPlanksNeededForPrintingPressesWithPunchcards(2)

            # Cycles per day = 24 / 0.75 = 32
            # Planks per printing press per day = 1 * 32 = 32
            # Total planks = 2 * 32 = 64
            self.assertEqual(64, result)

    # Test Cases for Wood Workshop
    def test_getWoodWorkshopsNeededForTreatedPlanksNegativeAmount(self) -> None:    # noqa: E501
        """
        The getWoodWorkshopsNeededForTreatedPlanks method must raise ValueError
        if treated planks amount is negative.
        """
        errMsg = "Treated planks amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWoodWorkshopsNeededForTreatedPlanks(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getWoodWorkshopsNeededForTreatedPlanksSuccess(self) -> None:
        """
        The getWoodWorkshopsNeededForTreatedPlanks method must correctly
        calculate wood workshops needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWoodWorkshopsNeededForTreatedPlanks(30.0)

            # Production per wood workshop per day = (1 / 3.0) * 24 = 8
            # Wood workshops needed = ceil(30.0 / 8) = ceil(3.75) = 4
            self.assertEqual(4, result)

    def test_getPineResinNeededForWoodWorkshopsNegativeCount(self) -> None:
        """
        The getPineResinNeededForWoodWorkshops method must raise ValueError if
        wood workshops count is negative.
        """
        errMsg = "Wood workshops count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPineResinNeededForWoodWorkshops(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPineResinNeededForWoodWorkshopsSuccess(self) -> None:
        """
        The getPineResinNeededForWoodWorkshops method must correctly calculate
        pine resin needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPineResinNeededForWoodWorkshops(3)

            # Cycles per day = 24 / 3.0 = 8
            # Pine resin per wood workshop per day = 1 * 8 = 8
            # Total pine resin = 3 * 8 = 24
            self.assertEqual(24, result)

    def test_getPlanksNeededForWoodWorkshopsNegativeCount(self) -> None:
        """
        The getPlanksNeededForWoodWorkshops method must raise ValueError if
        wood workshops count is negative.
        """
        errMsg = "Wood workshops count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPlanksNeededForWoodWorkshops(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPlanksNeededForWoodWorkshopsSuccess(self) -> None:
        """
        The getPlanksNeededForWoodWorkshops method must correctly calculate
        planks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPlanksNeededForWoodWorkshops(3)

            # Cycles per day = 24 / 3.0 = 8
            # Planks per wood workshop per day = 1 * 8 = 8
            # Total planks = 3 * 8 = 24
            self.assertEqual(24, result)

    # Test Cases for Smelter
    def test_getSmeltersNeededForMetalBlocksNegativeAmount(self) -> None:
        """
        The getSmeltersNeededForMetalBlocks method must raise ValueError if
        metal blocks amount is negative.
        """
        errMsg = "Metal blocks amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getSmeltersNeededForMetalBlocks(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getSmeltersNeededForMetalBlocksSuccess(self) -> None:
        """
        The getSmeltersNeededForMetalBlocks method must correctly calculate
        smelters needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getSmeltersNeededForMetalBlocks(15.0)

            # Production per smelter per day = (1 / 2.0) * 24 = 12
            # Smelters needed = ceil(15.0 / 12) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getScrapMetalNeededForSmeltersNegativeCount(self) -> None:
        """
        The getScrapMetalNeededForSmelters method must raise ValueError if
        smelters count is negative.
        """
        errMsg = "Smelters count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getScrapMetalNeededForSmelters(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getScrapMetalNeededForSmeltersSuccess(self) -> None:
        """
        The getScrapMetalNeededForSmelters method must correctly calculate
        scrap metal needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getScrapMetalNeededForSmelters(2)

            # Cycles per day = 24 / 2.0 = 12
            # Scrap metal per smelter per day = 1 * 12 = 12
            # Total scrap metal = 2 * 12 = 24
            self.assertEqual(24, result)

    def test_getLogsNeededForSmeltersNegativeCount(self) -> None:
        """
        The getLogsNeededForSmelters method must raise ValueError if
        smelters count is negative.
        """
        errMsg = "Smelters count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForSmelters(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLogsNeededForSmeltersSuccess(self) -> None:
        """
        The getLogsNeededForSmelters method must correctly calculate
        logs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 0.2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForSmelters(2)

            # Cycles per day = 24 / 2.0 = 12
            # Logs per smelter per day = 0.2 * 12 = 2.4
            # Total logs = 2 * 2.4 = 4.8
            self.assertAlmostEqual(4.8, result, places=5)

    # Test Cases for Mine
    def test_getMinesNeededForScrapMetalNegativeAmount(self) -> None:
        """
        The getMinesNeededForScrapMetal method must raise ValueError if
        scrap metal amount is negative.
        """
        errMsg = "Scrap metal amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMinesNeededForScrapMetal(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getMinesNeededForScrapMetalSuccess(self) -> None:
        """
        The getMinesNeededForScrapMetal method must correctly calculate
        mines needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.8
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getMinesNeededForScrapMetal(100.0)

            # Production per mine per day = (5 / 1.8) * 24 = 66.666...
            # Mines needed = ceil(100.0 / 66.666...) = ceil(1.5) = 2
            self.assertEqual(2, result)

    def test_getTreatedPlanksNeededForMinesNegativeCount(self) -> None:
        """
        The getTreatedPlanksNeededForMines method must raise ValueError if
        mines count is negative.
        """
        errMsg = "Mines count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getTreatedPlanksNeededForMines(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getTreatedPlanksNeededForMinesSuccess(self) -> None:
        """
        The getTreatedPlanksNeededForMines method must correctly calculate
        treated planks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 1.8
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getTreatedPlanksNeededForMines(3)

            # Cycles per day = 24 / 1.8 = 13.333...
            # Treated planks per mine per day = 1 * 13.333... = 13.333...
            # Total treated planks = 3 * 13.333... = 40
            self.assertEqual(40, result)

    def test_getRefineriesNeededForBiofuelCarrotsNegativeAmount(self) -> None:
        """
        The getRefineriesNeededForBiofuelCarrots method must raise ValueError
        if biofuel carrots amount is negative.
        """
        errMsg = "Biofuel Carrots amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getRefineriesNeededForBiofuelCarrots(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getRefineriesNeededForBiofuelCarrotsSuccess(self) -> None:
        """
        The getRefineriesNeededForBiofuelCarrots method must correctly
        calculate refineries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getRefineriesNeededForBiofuelCarrots(100.0)

            # Production per refinery per day = (5 / 3.0) * 24 = 40
            # Refineries needed = ceil(100.0 / 40) = ceil(2.5) = 3
            self.assertEqual(3, result)

    def test_getCarrotsNeededForRefineriesWithBiofuelCarrotsNegativeCount(self) -> None:    # noqa: E501
        """
        The getCarrotsNeededForRefineriesWithBiofuelCarrots method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCarrotsNeededForRefineriesWithBiofuelCarrots(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getCarrotsNeededForRefineriesWithBiofuelCarrotsSuccess(self) -> None:  # noqa: E501
        """
        The getCarrotsNeededForRefineriesWithBiofuelCarrots method must
        correctly calculate carrots needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getCarrotsNeededForRefineriesWithBiofuelCarrots(3)

            # Cycles per day = 24 / 3.0 = 8
            # Carrots per refinery per day = 2 * 8 = 16
            # Total carrots = 3 * 16 = 48
            self.assertEqual(48, result)

    def test_getWaterNeededForRefineriesWithBiofuelCarrotsNegativeCount(self) -> None:  # noqa: E501
        """
        The getWaterNeededForRefineriesWithBiofuelCarrots method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWaterNeededForRefineriesWithBiofuelCarrots(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getWaterNeededForRefineriesWithBiofuelCarrotsSuccess(self) -> None:    # noqa: E501
        """
        The getWaterNeededForRefineriesWithBiofuelCarrots method must
        correctly calculate water needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWaterNeededForRefineriesWithBiofuelCarrots(3)

            # Cycles per day = 24 / 3.0 = 8
            # Water per refinery per day = 2 * 8 = 16
            # Total water = 3 * 16 = 48
            self.assertEqual(48, result)

    def test_getRefineriesNeededForBiofuelPotatoesNegativeAmount(self) -> None:     # noqa: E501
        """
        The getRefineriesNeededForBiofuelPotatoes method must raise ValueError
        if biofuel potatoes amount is negative.
        """
        errMsg = "Biofuel Potatoes amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getRefineriesNeededForBiofuelPotatoes(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getRefineriesNeededForBiofuelPotatoesSuccess(self) -> None:
        """
        The getRefineriesNeededForBiofuelPotatoes method must correctly
        calculate refineries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 30
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getRefineriesNeededForBiofuelPotatoes(250.0)

            # Production per refinery per day = (30 / 3.0) * 24 = 240
            # Refineries needed = ceil(250.0 / 240) = ceil(1.0416...) = 2
            self.assertEqual(2, result)

    def test_getPotatoesNeededForRefineriesWithBiofuelPotatoesNegativeCount(self) -> None:  # noqa: E501
        """
        The getPotatoesNeededForRefineriesWithBiofuelPotatoes method must
        raise ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPotatoesNeededForRefineriesWithBiofuelPotatoes(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPotatoesNeededForRefineriesWithBiofuelPotatoesSuccess(self) -> None:    # noqa: E501
        """
        The getPotatoesNeededForRefineriesWithBiofuelPotatoes method must
        correctly calculate potatoes needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getPotatoesNeededForRefineriesWithBiofuelPotatoes(3)

            # Cycles per day = 24 / 3.0 = 8
            # Potatoes per refinery per day = 2 * 8 = 16
            # Total potatoes = 3 * 16 = 48
            self.assertEqual(48, result)

    def test_getWaterNeededForRefineriesWithBiofuelPotatoesNegativeCount(self) -> None:     # noqa: E501
        """
        The getWaterNeededForRefineriesWithBiofuelPotatoes method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWaterNeededForRefineriesWithBiofuelPotatoes(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getWaterNeededForRefineriesWithBiofuelPotatoesSuccess(self) -> None:   # noqa: E501
        """
        The getWaterNeededForRefineriesWithBiofuelPotatoes method must
        correctly calculate water needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getWaterNeededForRefineriesWithBiofuelPotatoes(3)

            # Cycles per day = 24 / 3.0 = 8
            # Water per refinery per day = 2 * 8 = 16
            # Total water = 3 * 16 = 48
            self.assertEqual(48, result)

    def test_getRefineriesNeededForBiofuelSpadderdocksNegativeAmount(self) -> None:     # noqa: E501
        """
        The getRefineriesNeededForBiofuelSpadderdocks method must raise
        ValueError if biofuel spadderdocks amount is negative.
        """
        errMsg = "Biofuel Spadderdocks amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getRefineriesNeededForBiofuelSpadderdocks(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getRefineriesNeededForBiofuelSpadderdocksSuccess(self) -> None:
        """
        The getRefineriesNeededForBiofuelSpadderdocks method must correctly
        calculate refineries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 2
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 25
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getRefineriesNeededForBiofuelSpadderdocks(220.0)

            # Production per refinery per day = (25 / 3.0) * 24 = 200
            # Refineries needed = ceil(220.0 / 200) = ceil(1.1) = 2
            self.assertEqual(2, result)

    def test_getSpadderdocksNeededForRefineriesWithBiofuelSpadderdocksNegativeCount(self) -> None:      # noqa: E501
        """
        The getSpadderdocksNeededForRefineriesWithBiofuelSpadderdocks method
        must raise ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail \
                .getSpadderdocksNeededForRefineriesWithBiofuelSpadderdocks(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getSpadderdocksNeededForRefineriesWithBiofuelSpadderdocksSuccess(self) -> None:    # noqa: E501
        """
        The getSpadderdocksNeededForRefineriesWithBiofuelSpadderdocks method
        must correctly calculate spadderdocks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 2
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getSpadderdocksNeededForRefineriesWithBiofuelSpadderdocks(3)

            # Cycles per day = 24 / 3.0 = 8
            # Spadderdocks per refinery per day = 2 * 8 = 16
            # Total spadderdocks = 3 * 16 = 48
            self.assertEqual(48, result)

    def test_getWaterNeededForRefineriesWithBiofuelSpadderdocksNegativeCount(self) -> None:     # noqa: E501
        """
        The getWaterNeededForRefineriesWithBiofuelSpadderdocks method must
        raise ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getWaterNeededForRefineriesWithBiofuelSpadderdocks(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getWaterNeededForRefineriesWithBiofuelSpadderdocksSuccess(self) -> None:   # noqa: E501
        """
        The getWaterNeededForRefineriesWithBiofuelSpadderdocks method must
        correctly calculate water needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 2
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getWaterNeededForRefineriesWithBiofuelSpadderdocks(3)

            # Cycles per day = 24 / 3.0 = 8
            # Water per refinery per day = 2 * 8 = 16
            # Total water = 3 * 16 = 48
            self.assertEqual(48, result)

    def test_getRefineriesNeededForCatalystNegativeAmount(self) -> None:
        """
        The getRefineriesNeededForCatalyst method must raise ValueError if
        catalyst amount is negative.
        """
        errMsg = "Catalyst amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getRefineriesNeededForCatalyst(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getRefineriesNeededForCatalystSuccess(self) -> None:
        """
        The getRefineriesNeededForCatalyst method must correctly calculate
        refineries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 3
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getRefineriesNeededForCatalyst(15.0)

            # Production per refinery per day = (1 / 2.0) * 24 = 12
            # Refineries needed = ceil(15.0 / 12) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getMapleSyrupNeededForRefineriesWithCatalystNegativeCount(self) -> None:   # noqa: E501
        """
        The getMapleSyrupNeededForRefineriesWithCatalyst method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMapleSyrupNeededForRefineriesWithCatalyst(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getMapleSyrupNeededForRefineriesWithCatalystSuccess(self) -> None:
        """
        The getMapleSyrupNeededForRefineriesWithCatalyst method must correctly
        calculate maple syrup needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 3
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getMapleSyrupNeededForRefineriesWithCatalyst(3)

            # Cycles per day = 24 / 2.0 = 12
            # Maple syrup per refinery per day = 1 * 12 = 12
            # Total maple syrup = 3 * 12 = 36
            self.assertEqual(36, result)

    def test_getExtractNeededForRefineriesWithCatalystNegativeCount(self) -> None:  # noqa: E501
        """
        The getExtractNeededForRefineriesWithCatalyst method must raise
        ValueError if refineries count is negative.
        """
        errMsg = "Refineries count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getExtractNeededForRefineriesWithCatalyst(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getExtractNeededForRefineriesWithCatalystSuccess(self) -> None:
        """
        The getExtractNeededForRefineriesWithCatalyst method must correctly
        calculate extract needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 3
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getExtractNeededForRefineriesWithCatalyst(3)

            # Cycles per day = 24 / 2.0 = 12
            # Extract per refinery per day = 1 * 12 = 12
            # Total extract = 3 * 12 = 36
            self.assertEqual(36, result)

    # Test Cases for Bot Part Factory
    def test_getBotPartFactoriesNeededForBotChassisNegativeAmount(self) -> None:    # noqa: E501
        """
        The getBotPartFactoriesNeededForBotChassis method must raise
        ValueError if bot chassis amount is negative.
        """
        errMsg = "Bot Chassis amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBotPartFactoriesNeededForBotChassis(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBotPartFactoriesNeededForBotChassisSuccess(self) -> None:
        """
        The getBotPartFactoriesNeededForBotChassis method must correctly
        calculate bot part factories needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 4.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBotPartFactoriesNeededForBotChassis(8.0)

            # Production per bot part factory per day = (1 / 4.0) * 24 = 6
            # Bot part factories needed = ceil(8.0 / 6) = ceil(1.333...) = 2
            self.assertEqual(2, result)

    def test_getPlanksNeededForBotPartFactoriesWithBotChassisNegativeCount(self) -> None:   # noqa: E501
        """
        The getPlanksNeededForBotPartFactoriesWithBotChassis method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPlanksNeededForBotPartFactoriesWithBotChassis(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPlanksNeededForBotPartFactoriesWithBotChassisSuccess(self) -> None:     # noqa: E501
        """
        The getPlanksNeededForBotPartFactoriesWithBotChassis method must
        correctly calculate planks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 4.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getPlanksNeededForBotPartFactoriesWithBotChassis(3)

            # Cycles per day = 24 / 4.0 = 6
            # Planks per bot part factory per day = 2 * 6 = 12
            # Total planks = 3 * 12 = 36
            self.assertEqual(36, result)

    def test_getMetalBlocksNeededForBotPartFactoriesWithBotChassisNegativeCount(self) -> None:  # noqa: E501
        """
        The getMetalBlocksNeededForBotPartFactoriesWithBotChassis method must
        raise ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMetalBlocksNeededForBotPartFactoriesWithBotChassis(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getMetalBlocksNeededForBotPartFactoriesWithBotChassisSuccess(self) -> None:    # noqa: E501
        """
        The getMetalBlocksNeededForBotPartFactoriesWithBotChassis method must
        correctly calculate metal blocks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 4.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getMetalBlocksNeededForBotPartFactoriesWithBotChassis(3)

            # Cycles per day = 24 / 4.0 = 6
            # Metal blocks per bot part factory per day = 1 * 6 = 6
            # Total metal blocks = 3 * 6 = 18
            self.assertEqual(18, result)

    def test_getBiofuelNeededForBotPartFactoriesWithBotChassisNegativeCount(self) -> None:  # noqa: E501
        """
        The getBiofuelNeededForBotPartFactoriesWithBotChassis method must
        raise ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBiofuelNeededForBotPartFactoriesWithBotChassis(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBiofuelNeededForBotPartFactoriesWithBotChassisSuccess(self) -> None:    # noqa: E501
        """
        The getBiofuelNeededForBotPartFactoriesWithBotChassis method must
        correctly calculate biofuel needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 4.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getBiofuelNeededForBotPartFactoriesWithBotChassis(3)

            # Cycles per day = 24 / 4.0 = 6
            # Biofuel per bot part factory per day = 1 * 6 = 6
            # Total biofuel = 3 * 6 = 18
            self.assertEqual(18, result)

    def test_getBotPartFactoriesNeededForBotHeadsNegativeAmount(self) -> None:
        """
        The getBotPartFactoriesNeededForBotHeads method must raise ValueError
        if bot heads amount is negative.
        """
        errMsg = "Bot Heads amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBotPartFactoriesNeededForBotHeads(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBotPartFactoriesNeededForBotHeadsSuccess(self) -> None:
        """
        The getBotPartFactoriesNeededForBotHeads method must correctly
        calculate bot part factories needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBotPartFactoriesNeededForBotHeads(10.0)

            # Production per bot part factory per day = (1 / 3.0) * 24 = 8
            # Bot part factories needed = ceil(10.0 / 8) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getGearsNeededForBotPartFactoriesWithBotHeadsNegativeCount(self) -> None:  # noqa: E501
        """
        The getGearsNeededForBotPartFactoriesWithBotHeads method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGearsNeededForBotPartFactoriesWithBotHeads(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getGearsNeededForBotPartFactoriesWithBotHeadsSuccess(self) -> None:    # noqa: E501
        """
        The getGearsNeededForBotPartFactoriesWithBotHeads method must
        correctly calculate gears needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGearsNeededForBotPartFactoriesWithBotHeads(3)

            # Cycles per day = 24 / 3.0 = 8
            # Gears per bot part factory per day = 1 * 8 = 8
            # Total gears = 3 * 8 = 24
            self.assertEqual(24, result)

    def test_getMetalBlocksNeededForBotPartFactoriesWithBotHeadsNegativeCount(self) -> None:    # noqa: E501
        """
        The getMetalBlocksNeededForBotPartFactoriesWithBotHeads method must
        raise ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getMetalBlocksNeededForBotPartFactoriesWithBotHeads(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getMetalBlocksNeededForBotPartFactoriesWithBotHeadsSuccess(self) -> None:  # noqa: E501
        """
        The getMetalBlocksNeededForBotPartFactoriesWithBotHeads method must
        correctly calculate metal blocks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail \
                .getMetalBlocksNeededForBotPartFactoriesWithBotHeads(3)

            # Cycles per day = 24 / 3.0 = 8
            # Metal blocks per bot part factory per day = 1 * 8 = 8
            # Total metal blocks = 3 * 8 = 24
            self.assertEqual(24, result)

    def test_getPlanksNeededForBotPartFactoriesWithBotHeadsNegativeCount(self) -> None:     # noqa: E501
        """
        The getPlanksNeededForBotPartFactoriesWithBotHeads method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPlanksNeededForBotPartFactoriesWithBotHeads(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPlanksNeededForBotPartFactoriesWithBotHeadsSuccess(self) -> None:   # noqa: E501
        """
        The getPlanksNeededForBotPartFactoriesWithBotHeads method must
        correctly calculate planks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 1
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPlanksNeededForBotPartFactoriesWithBotHeads(3)

            # Cycles per day = 24 / 3.0 = 8
            # Planks per bot part factory per day = 1 * 8 = 8
            # Total planks = 3 * 8 = 24
            self.assertEqual(24, result)

    def test_getBotPartFactoriesNeededForBotLimbsNegativeAmount(self) -> None:
        """
        The getBotPartFactoriesNeededForBotLimbs method must raise ValueError
        if bot limbs amount is negative.
        """
        errMsg = "Bot Limbs amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBotPartFactoriesNeededForBotLimbs(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBotPartFactoriesNeededForBotLimbsSuccess(self) -> None:
        """
        The getBotPartFactoriesNeededForBotLimbs method must correctly
        calculate bot part factories needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 2
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBotPartFactoriesNeededForBotLimbs(20.0)

            # Production per bot part factory per day = (2 / 3.0) * 24 = 16
            # Bot part factories needed = ceil(20.0 / 16) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getGearsNeededForBotPartFactoriesWithBotLimbsNegativeCount(self) -> None:  # noqa: E501
        """
        The getGearsNeededForBotPartFactoriesWithBotLimbs method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getGearsNeededForBotPartFactoriesWithBotLimbs(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getGearsNeededForBotPartFactoriesWithBotLimbsSuccess(self) -> None:    # noqa: E501
        """
        The getGearsNeededForBotPartFactoriesWithBotLimbs method must
        correctly calculate gears needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 2
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getGearsNeededForBotPartFactoriesWithBotLimbs(3)

            # Cycles per day = 24 / 3.0 = 8
            # Gears per bot part factory per day = 2 * 8 = 16
            # Total gears = 3 * 16 = 48
            self.assertEqual(48, result)

    def test_getPlanksNeededForBotPartFactoriesWithBotLimbsNegativeCount(self) -> None:     # noqa: E501
        """
        The getPlanksNeededForBotPartFactoriesWithBotLimbs method must raise
        ValueError if bot part factories count is negative.
        """
        errMsg = "Bot part factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPlanksNeededForBotPartFactoriesWithBotLimbs(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPlanksNeededForBotPartFactoriesWithBotLimbsSuccess(self) -> None:   # noqa: E501
        """
        The getPlanksNeededForBotPartFactoriesWithBotLimbs method must
        correctly calculate planks needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 2
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPlanksNeededForBotPartFactoriesWithBotLimbs(3)

            # Cycles per day = 24 / 3.0 = 8
            # Planks per bot part factory per day = 1 * 8 = 8
            # Total planks = 3 * 8 = 24
            self.assertEqual(24, result)

    # Test Cases for Bot Assembler
    def test_getBotAssemblersNeededForBotsNegativeAmount(self) -> None:
        """
        The getBotAssemblersNeededForBots method must raise ValueError if
        bots amount is negative.
        """
        errMsg = "Bots amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBotAssemblersNeededForBots(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBotAssemblersNeededForBotsSuccess(self) -> None:
        """
        The getBotAssemblersNeededForBots method must correctly calculate
        bot assemblers needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 6.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBotAssemblersNeededForBots(5.0)

            # Production per bot assembler per day = (1 / 6.0) * 24 = 4
            # Bot assemblers needed = ceil(5.0 / 4) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getBotChassisNeededForBotAssemblersNegativeCount(self) -> None:
        """
        The getBotChassisNeededForBotAssemblers method must raise ValueError
        if bot assemblers count is negative.
        """
        errMsg = "Bot assemblers count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBotChassisNeededForBotAssemblers(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBotChassisNeededForBotAssemblersSuccess(self) -> None:
        """
        The getBotChassisNeededForBotAssemblers method must correctly
        calculate bot chassis needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 6.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBotChassisNeededForBotAssemblers(3)

            # Cycles per day = 24 / 6.0 = 4
            # Bot chassis per bot assembler per day = 1 * 4 = 4
            # Total bot chassis = 3 * 4 = 12
            self.assertEqual(12, result)

    def test_getBotHeadsNeededForBotAssemblersNegativeCount(self) -> None:
        """
        The getBotHeadsNeededForBotAssemblers method must raise ValueError
        if bot assemblers count is negative.
        """
        errMsg = "Bot assemblers count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBotHeadsNeededForBotAssemblers(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBotHeadsNeededForBotAssemblersSuccess(self) -> None:
        """
        The getBotHeadsNeededForBotAssemblers method must correctly calculate
        bot heads needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 6.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBotHeadsNeededForBotAssemblers(3)

            # Cycles per day = 24 / 6.0 = 4
            # Bot heads per bot assembler per day = 1 * 4 = 4
            # Total bot heads = 3 * 4 = 12
            self.assertEqual(12, result)

    def test_getBotLimbsNeededForBotAssemblersNegativeCount(self) -> None:
        """
        The getBotLimbsNeededForBotAssemblers method must raise ValueError
        if bot assemblers count is negative.
        """
        errMsg = "Bot assemblers count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBotLimbsNeededForBotAssemblers(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBotLimbsNeededForBotAssemblersSuccess(self) -> None:
        """
        The getBotLimbsNeededForBotAssemblers method must correctly calculate
        bot limbs needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 6.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBotLimbsNeededForBotAssemblers(3)

            # Cycles per day = 24 / 6.0 = 4
            # Bot limbs per bot assembler per day = 1 * 4 = 4
            # Total bot limbs = 3 * 4 = 12
            self.assertEqual(12, result)

    # Test Cases for Explosives Factory
    def test_getExplosivesFactoriesNeededForExplosivesNegativeAmount(self) -> None:     # noqa: E501
        """
        The getExplosivesFactoriesNeededForExplosives method must raise
        ValueError if explosives amount is negative.
        """
        errMsg = "Explosives amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getExplosivesFactoriesNeededForExplosives(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getExplosivesFactoriesNeededForExplosivesSuccess(self) -> None:
        """
        The getExplosivesFactoriesNeededForExplosives method must correctly
        calculate explosives factories needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getExplosivesFactoriesNeededForExplosives(15.0)

            # Production per explosives factory per day = (1 / 2.0) * 24 = 12
            # Explosives factories needed = ceil(15.0 / 12) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getBadwaterNeededForExplosivesFactoriesNegativeCount(self) -> None:    # noqa: E501
        """
        The getBadwaterNeededForExplosivesFactories method must raise
        ValueError if explosives factories count is negative.
        """
        errMsg = "Explosives factories count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBadwaterNeededForExplosivesFactories(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBadwaterNeededForExplosivesFactoriesSuccess(self) -> None:
        """
        The getBadwaterNeededForExplosivesFactories method must correctly
        calculate badwater needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBadwaterNeededForExplosivesFactories(3)

            # Cycles per day = 24 / 2.0 = 12
            # Badwater per explosives factory per day = 5 * 12 = 60
            # Total badwater = 3 * 60 = 180
            self.assertEqual(180, result)

    # Test Cases for Centrifuge
    def test_getCentrifugesNeededForExtractNegativeAmount(self) -> None:
        """
        The getCentrifugesNeededForExtract method must raise ValueError if
        extract amount is negative.
        """
        errMsg = "Extract amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getCentrifugesNeededForExtract(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getCentrifugesNeededForExtractSuccess(self) -> None:
        """
        The getCentrifugesNeededForExtract method must correctly calculate
        centrifuges needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getCentrifugesNeededForExtract(10.0)

            # Production per centrifuge per day = (1 / 3.0) * 24 = 8
            # Centrifuges needed = ceil(10.0 / 8) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getBadwaterNeededForCentrifugesNegativeCount(self) -> None:
        """
        The getBadwaterNeededForCentrifuges method must raise ValueError if
        centrifuges count is negative.
        """
        errMsg = "Centrifuges count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBadwaterNeededForCentrifuges(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBadwaterNeededForCentrifugesSuccess(self) -> None:
        """
        The getBadwaterNeededForCentrifuges method must correctly calculate
        badwater needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 5
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBadwaterNeededForCentrifuges(3)

            # Cycles per day = 24 / 3.0 = 8
            # Badwater per centrifuge per day = 5 * 8 = 40
            # Total badwater = 3 * 40 = 120
            self.assertEqual(120, result)

    def test_getLogsNeededForCentrifugesNegativeCount(self) -> None:
        """
        The getLogsNeededForCentrifuges method must raise ValueError if
        centrifuges count is negative.
        """
        errMsg = "Centrifuges count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getLogsNeededForCentrifuges(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getLogsNeededForCentrifugesSuccess(self) -> None:
        """
        The getLogsNeededForCentrifuges method must correctly calculate logs
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 3.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getLogsNeededForCentrifuges(3)

            # Cycles per day = 24 / 3.0 = 8
            # Logs per centrifuge per day = 2 * 8 = 16
            # Total logs = 3 * 16 = 48
            self.assertAlmostEqual(48.0, result, places=5)

    # Test Cases for Herbalist
    def test_getHerbalistsNeededForAntidoteNegativeAmount(self) -> None:
        """
        The getHerbalistsNeededForAntidote method must raise ValueError if
        antidote amount is negative.
        """
        errMsg = "Antidote amount cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getHerbalistsNeededForAntidote(-10.0)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getHerbalistsNeededForAntidoteSuccess(self) -> None:
        """
        The getHerbalistsNeededForAntidote method must correctly calculate
        herbalists needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsOutputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getHerbalistsNeededForAntidote(15.0)

            # Production per herbalist per day = (1 / 2.0) * 24 = 12
            # Herbalists needed = ceil(15.0 / 12) = ceil(1.25) = 2
            self.assertEqual(2, result)

    def test_getDandelionsNeededForHerbalistsNegativeCount(self) -> None:
        """
        The getDandelionsNeededForHerbalists method must raise ValueError if
        herbalists count is negative.
        """
        errMsg = "Herbalists count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getDandelionsNeededForHerbalists(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getDandelionsNeededForHerbalistsSuccess(self) -> None:
        """
        The getDandelionsNeededForHerbalists method must correctly calculate
        dandelions needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 2
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getDandelionsNeededForHerbalists(3)

            # Cycles per day = 24 / 2.0 = 12
            # Dandelions per herbalist per day = 2 * 12 = 24
            # Total dandelions = 3 * 24 = 72
            self.assertEqual(72, result)

    def test_getBerriesNeededForHerbalistsNegativeCount(self) -> None:
        """
        The getBerriesNeededForHerbalists method must raise ValueError if
        herbalists count is negative.
        """
        errMsg = "Herbalists count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getBerriesNeededForHerbalists(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getBerriesNeededForHerbalistsSuccess(self) -> None:
        """
        The getBerriesNeededForHerbalists method must correctly calculate
        berries needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 3
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getBerriesNeededForHerbalists(3)

            # Cycles per day = 24 / 2.0 = 12
            # Berries per herbalist per day = 3 * 12 = 36
            # Total berries = 3 * 36 = 108
            self.assertEqual(108, result)

    def test_getPapersNeededForHerbalistsNegativeCount(self) -> None:
        """
        The getPapersNeededForHerbalists method must raise ValueError if
        herbalists count is negative.
        """
        errMsg = "Herbalists count cannot be negative."
        with patch('pkgs.factions.folktail.FactionData'), \
                self.assertRaises(ValueError) as context:
            folktail = Folktail()
            folktail.getPapersNeededForHerbalists(-1)
        self.assertEqual(errMsg,
                         str(context.exception))

    def test_getPapersNeededForHerbalistsSuccess(self) -> None:
        """
        The getPapersNeededForHerbalists method must correctly calculate logs
        needed.
        """
        with patch('pkgs.factions.folktail.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            mockFactionDataInstance.getGoodsRecipeIndex.return_value = 0
            mockFactionDataInstance.getGoodsProductionTime.return_value = 2.0
            mockFactionDataInstance.getGoodsInputQuantity.return_value = 1
            MockFactionData.return_value = mockFactionDataInstance

            folktail = Folktail()
            result = folktail.getPapersNeededForHerbalists(3)

            # Cycles per day = 24 / 2.0 = 12
            # Logs per herbalist per day = 1 * 12 = 12
            # Total logs = 3 * 12 = 36
            self.assertAlmostEqual(36.0, result, places=5)
