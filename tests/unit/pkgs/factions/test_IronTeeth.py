from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.data.enumerators import ConsumptionType               # noqa: E402
from pkgs.data.enumerators import CropName                      # noqa: E402
from pkgs.data.enumerators import DifficultyLevel               # noqa: E402
from pkgs.data.enumerators import TreeName                      # noqa: E402
from pkgs.factions.ironTeeth import IronTeeth                   # noqa: E402


class TestIronTeeth(TestCase):
    """
    Test suite for the IronTeeth class.
    """

    def setUp(self) -> None:
        """
        Test setup - creates unit under test with mocked factionData.
        """
        with patch('pkgs.factions.ironTeeth.FactionData'):
            self.uut = IronTeeth()
        self.uut.factionData = Mock()

    # Test Cases for Constructor
    def test_constructorFileNotFound(self) -> None:
        """
        The constructor must raise FileNotFoundError if YAML file is not
        found.
        """
        with patch('pkgs.data.factionData.open',
                   side_effect=FileNotFoundError()):
            with self.assertRaises(FileNotFoundError):
                IronTeeth()

    def test_constructorYAMLError(self) -> None:
        """
        The constructor must raise any YAML parsing errors from FactionData.
        """
        import yaml
        errMsg = "YAML parsing error."
        with patch('pkgs.factions.ironTeeth.FactionData') as MockFactionData, \
                self.assertRaises(yaml.YAMLError) as context:
            MockFactionData.side_effect = yaml.YAMLError(errMsg)
            IronTeeth()
            MockFactionData.assert_called_once_with('./data/ironTeeth.yml')
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorSuccess(self) -> None:
        """
        The constructor must successfully instantiate FactionData with the
        ironTeeth.yml file.
        """
        with patch('pkgs.factions.ironTeeth.FactionData') as MockFactionData:
            mockFactionDataInstance = Mock()
            MockFactionData.return_value = mockFactionDataInstance

            ironTeeth = IronTeeth()

            MockFactionData.assert_called_once_with('./data/ironTeeth.yml')
            self.assertEqual(mockFactionDataInstance, ironTeeth.factionData)

    # Test Cases for Daily Consumption
    def test_getDailyFoodConsumptionNegativePopulation(self) -> None:
        """
        The getDailyFoodConsumption method must raise ValueError if
        population is negative.
        """
        errMsg = "Population cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getDailyFoodConsumption(-10, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDailyFoodConsumptionSuccess(self) -> None:
        """
        The getDailyFoodConsumption method must correctly calculate daily
        food consumption.
        """
        self.uut.factionData.getConsumption.return_value = 2.75
        self.uut.factionData.getDifficultyModifier.return_value = 1.0

        result = self.uut.getDailyFoodConsumption(10,
                                                  DifficultyLevel.NORMAL)

        # Consumption = 10 * 2.75 * 1.0 = 27.5, ceiling = 28
        self.assertEqual(28, result)
        self.uut.factionData.getConsumption.assert_called_once()
        self.uut.factionData.getDifficultyModifier.assert_called_once()
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
            self.uut.getDailyWaterConsumption(-10, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDailyWaterConsumptionSuccess(self) -> None:
        """
        The getDailyWaterConsumption method must correctly calculate daily
        water consumption.
        """
        self.uut.factionData.getConsumption.return_value = 2.25
        self.uut.factionData.getDifficultyModifier.return_value = 1.0

        result = self.uut.getDailyWaterConsumption(10,
                                                   DifficultyLevel.NORMAL)

        # Consumption = 10 * 2.25 * 1.0 = 22.5, ceiling = 23
        self.assertEqual(23, result)
        self.uut.factionData.getConsumption.assert_called_once()
        self.uut.factionData.getDifficultyModifier.assert_called_once()
        self.uut.factionData.getConsumption \
            .assert_called_once_with(ConsumptionType.WATER)
        self.uut.factionData.getDifficultyModifier \
            .assert_called_once_with(DifficultyLevel.NORMAL)

    # Test Cases for Food Per Type
    def test_getFoodPerTypeNegativePopulation(self) -> None:
        """
        The getFoodPerType method must raise ValueError if population is
        negative.
        """
        errMsg = "Population cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodPerType(-10, 3, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodPerTypeZeroFoodTypeCount(self) -> None:
        """
        The getFoodPerType method must raise ValueError if foodTypeCount
        is not positive.
        """
        errMsg = "Food type count must be positive."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodPerType(10, 0, DifficultyLevel.NORMAL)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodPerTypeSuccess(self) -> None:
        """
        The getFoodPerType method must correctly calculate food per type.
        """
        self.uut.factionData.getConsumption.return_value = 2.75
        self.uut.factionData.getDifficultyModifier.return_value = 1.0

        result = self.uut.getFoodPerType(10, 3, DifficultyLevel.NORMAL)

        # Total food = 10 * 2.75 * 1.0 = 27.5
        # Per type = ceil(27.5 / 3) = ceil(9.166...) = 10
        self.assertEqual(10, result)
        self.uut.factionData.getConsumption \
            .assert_called_once_with(ConsumptionType.FOOD)
        self.uut.factionData.getDifficultyModifier \
            .assert_called_once_with(DifficultyLevel.NORMAL)

    # Test Cases for Log Per Type
    def test_getLogPerTypeNegativeTotalLogAmount(self) -> None:
        """
        The getLogPerType method must raise ValueError if totalLogAmount
        is negative.
        """
        errMsg = "Total log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogPerType(-10.0, 3)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogPerTypeZeroTreeTypeCount(self) -> None:
        """
        The getLogPerType method must raise ValueError if treeTypeCount
        is not positive.
        """
        errMsg = "Tree type count must be positive."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogPerType(10.0, 0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogPerTypeSuccess(self) -> None:
        """
        The getLogPerType method must correctly calculate logs per type.
        """
        result = self.uut.getLogPerType(100.0, 4)

        # Logs per type = 100.0 / 4 = 25.0
        self.assertEqual(25.0, result)

    # Test Cases for Deep Water Pump
    def test_getDeepWaterPumpsNeededNegativeAmount(self) -> None:
        """
        The getDeepWaterPumpsNeeded method must raise ValueError if water
        amount is negative.
        """
        errMsg = "Water amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getDeepWaterPumpsNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDeepWaterPumpsNeededSuccess(self) -> None:
        """
        The getDeepWaterPumpsNeeded method must correctly calculate pumps
        needed.
        """
        self.uut.factionData.getWaterProductionTime.return_value = 0.33
        self.uut.factionData.getWaterOutputQuantity.return_value = 1

        result = self.uut.getDeepWaterPumpsNeeded(100.0)

        # Production per pump per day = (1 / 0.33) * 24 = 72.727...
        # Pumps needed = ceil(100.0 / 72.727...) = ceil(1.375) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getWaterProductionTime.assert_called_once()
        self.uut.factionData.getWaterOutputQuantity.assert_called_once()

    # Test Cases for Deep Badwater Pump
    def test_getDeepBadwaterPumpsNeededNegativeAmount(self) -> None:
        """
        The getDeepBadwaterPumpsNeeded method must raise ValueError if
        badwater amount is negative.
        """
        errMsg = "Badwater amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getDeepBadwaterPumpsNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getDeepBadwaterPumpsNeededSuccess(self) -> None:
        """
        The getDeepBadwaterPumpsNeeded method must correctly calculate
        pumps needed.
        """
        self.uut.factionData.getWaterProductionTime.return_value = 0.33
        self.uut.factionData.getWaterOutputQuantity.return_value = 1

        result = self.uut.getDeepBadwaterPumpsNeeded(100.0)

        # Production per pump per day = (1 / 0.33) * 24 = 72.727...
        # Pumps needed = ceil(100.0 / 72.727...) = ceil(1.375) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getWaterProductionTime.assert_called_once()
        self.uut.factionData.getWaterOutputQuantity.assert_called_once()

    # Test Cases for Crop Tiles
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

        result = self.uut.getBerryTilesNeeded(10.0)

        # Production per tile = 3 / 12 = 0.25
        # Tiles needed = ceil(10.0 / 0.25) = ceil(40) = 40
        self.assertEqual(40, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.BERRY_BUSH)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.BERRY_BUSH)

    def test_getCoffeeBeanTilesNeededNegativeAmount(self) -> None:
        """
        The getCoffeeBeanTilesNeeded method must raise ValueError if coffee
        bean amount is negative.
        """
        errMsg = "Coffee bean amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCoffeeBeanTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCoffeeBeanTilesNeededSuccess(self) -> None:
        """
        The getCoffeeBeanTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 3
        self.uut.factionData.getCropHarvestYield.return_value = 1

        result = self.uut.getCoffeeBeanTilesNeeded(10.0)

        # Production per tile = 1 / 3 = 0.333...
        # Tiles needed = ceil(10.0 / 0.333...) = ceil(30) = 30
        self.assertEqual(30, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.COFFEE_BUSH)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.COFFEE_BUSH)

    def test_getKohlrabiTilesNeededNegativeAmount(self) -> None:
        """
        The getKohlrabiTilesNeeded method must raise ValueError if kohlrabi
        amount is negative.
        """
        errMsg = "Kohlrabi amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getKohlrabiTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getKohlrabiTilesNeededSuccess(self) -> None:
        """
        The getKohlrabiTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 3
        self.uut.factionData.getCropHarvestYield.return_value = 2

        result = self.uut.getKohlrabiTilesNeeded(10.0)

        # Production per tile = 2 / 3 = 0.666...
        # Tiles needed = ceil(10.0 / 0.666...) = ceil(15) = 15
        self.assertEqual(15, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.KOHLRABI_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.KOHLRABI_CROP)

    # Continue with more crop tests...
    def test_getCassavaTilesNeededNegativeAmount(self) -> None:
        """
        The getCassavaTilesNeeded method must raise ValueError if cassava
        amount is negative.
        """
        errMsg = "Cassava amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCassavaTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCassavaTilesNeededSuccess(self) -> None:
        """
        The getCassavaTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 5
        self.uut.factionData.getCropHarvestYield.return_value = 1

        result = self.uut.getCassavaTilesNeeded(10.0)

        # Production per tile = 1 / 5 = 0.2
        # Tiles needed = ceil(10.0 / 0.2) = ceil(50) = 50
        self.assertEqual(50, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.CASSAVA_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.CASSAVA_CROP)

    def test_getSoybeanTilesNeededNegativeAmount(self) -> None:
        """
        The getSoybeanTilesNeeded method must raise ValueError if soybean
        amount is negative.
        """
        errMsg = "Soybean amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getSoybeanTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSoybeanTilesNeededSuccess(self) -> None:
        """
        The getSoybeanTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 8
        self.uut.factionData.getCropHarvestYield.return_value = 2

        result = self.uut.getSoybeanTilesNeeded(10.0)

        # Production per tile = 2 / 8 = 0.25
        # Tiles needed = ceil(10.0 / 0.25) = ceil(40) = 40
        self.assertEqual(40, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.SOYBEAN_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.SOYBEAN_CROP)

    def test_getCanolaSeedTilesNeededNegativeAmount(self) -> None:
        """
        The getCanolaSeedTilesNeeded method must raise ValueError if canola
        seed amount is negative.
        """
        errMsg = "Canola seed amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCanolaSeedTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCanolaSeedTilesNeededSuccess(self) -> None:
        """
        The getCanolaSeedTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 9
        self.uut.factionData.getCropHarvestYield.return_value = 3

        result = self.uut.getCanolaSeedTilesNeeded(10.0)

        # Production per tile = 3 / 9 = 0.333...
        # Tiles needed = ceil(10.0 / 0.333...) = ceil(30) = 30
        self.assertEqual(30, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.CANOLA_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.CANOLA_CROP)

    def test_getCornTilesNeededNegativeAmount(self) -> None:
        """
        The getCornTilesNeeded method must raise ValueError if corn amount
        is negative.
        """
        errMsg = "Corn amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCornTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCornTilesNeededSuccess(self) -> None:
        """
        The getCornTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 10
        self.uut.factionData.getCropHarvestYield.return_value = 2

        result = self.uut.getCornTilesNeeded(10.0)

        # Production per tile = 2 / 10 = 0.2
        # Tiles needed = ceil(10.0 / 0.2) = ceil(50) = 50
        self.assertEqual(50, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.CORN_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.CORN_CROP)

    def test_getEggplantTilesNeededNegativeAmount(self) -> None:
        """
        The getEggplantTilesNeeded method must raise ValueError if eggplant
        amount is negative.
        """
        errMsg = "Eggplant amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getEggplantTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getEggplantTilesNeededSuccess(self) -> None:
        """
        The getEggplantTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getCropHarvestTime.return_value = 12
        self.uut.factionData.getCropHarvestYield.return_value = 2

        result = self.uut.getEggplantTilesNeeded(10.0)

        # Production per tile = 2 / 12 = 0.166...
        # Tiles needed = ceil(10.0 / 0.166...) = ceil(60) = 60
        self.assertEqual(60, result)
        self.uut.factionData.getCropHarvestTime.assert_called_once()
        self.uut.factionData.getCropHarvestYield.assert_called_once()
        self.uut.factionData.getCropHarvestTime \
            .assert_called_once_with(CropName.EGGPLANT_CROP)
        self.uut.factionData.getCropHarvestYield \
            .assert_called_once_with(CropName.EGGPLANT_CROP)

    # Test Cases for Tree Log Tiles
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
        self.uut.factionData.getTreeGrowthTime.return_value = 7
        self.uut.factionData.getTreeLogOutput.return_value = 1

        result = self.uut.getBirchLogTilesNeeded(10.0)

        # Production per tile = 1 / 7 = 0.142...
        # Tiles needed = ceil(10.0 / 0.142...) = ceil(70) = 70
        self.assertEqual(70, result)
        self.uut.factionData.getTreeGrowthTime.assert_called_once()
        self.uut.factionData.getTreeLogOutput.assert_called_once()
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
        self.uut.factionData.getTreeLogOutput.return_value = 2

        result = self.uut.getPineLogTilesNeeded(10.0)

        # Production per tile = 2 / 12 = 0.166...
        # Tiles needed = ceil(10.0 / 0.166...) = ceil(60) = 60
        self.assertEqual(60, result)
        self.uut.factionData.getTreeGrowthTime.assert_called_once()
        self.uut.factionData.getTreeLogOutput.assert_called_once()
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
        self.uut.factionData.getTreeHarvestTime.return_value = 7
        self.uut.factionData.getTreeHarvestYield.return_value = 2

        result = self.uut.getPineResinTilesNeeded(10.0)

        # Production per tile = 2 / 7 = 0.285...
        # Tiles needed = ceil(10.0 / 0.285...) = ceil(35) = 35
        self.assertEqual(35, result)
        self.uut.factionData.getTreeHarvestTime.assert_called_once()
        self.uut.factionData.getTreeHarvestYield.assert_called_once()
        self.uut.factionData.getTreeHarvestTime \
            .assert_called_once_with(TreeName.PINE)
        self.uut.factionData.getTreeHarvestYield \
            .assert_called_once_with(TreeName.PINE)

    def test_getMangroveLogTilesNeededNegativeAmount(self) -> None:
        """
        The getMangroveLogTilesNeeded method must raise ValueError if log
        amount is negative.
        """
        errMsg = "Log amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMangroveLogTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMangroveLogTilesNeededSuccess(self) -> None:
        """
        The getMangroveLogTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeGrowthTime.return_value = 10
        self.uut.factionData.getTreeLogOutput.return_value = 2

        result = self.uut.getMangroveLogTilesNeeded(10.0)

        # Production per tile = 2 / 10 = 0.2
        # Tiles needed = ceil(10.0 / 0.2) = ceil(50) = 50
        self.assertEqual(50, result)
        self.uut.factionData.getTreeGrowthTime.assert_called_once()
        self.uut.factionData.getTreeLogOutput.assert_called_once()
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.MANGROVE_TREE)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.MANGROVE_TREE)

    def test_getOakLogTilesNeededNegativeAmount(self) -> None:
        """
        The getOakLogTilesNeeded method must raise ValueError if log amount
        is negative.
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
        self.uut.factionData.getTreeGrowthTime.return_value = 30
        self.uut.factionData.getTreeLogOutput.return_value = 8

        result = self.uut.getOakLogTilesNeeded(10.0)

        # Production per tile = 8 / 30 = 0.266...
        # Tiles needed = ceil(10.0 / 0.266...) = ceil(37.5) = 38
        self.assertEqual(38, result)
        self.uut.factionData.getTreeGrowthTime.assert_called_once()
        self.uut.factionData.getTreeLogOutput.assert_called_once()
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.OAK)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.OAK)

    # Test Cases for Harvest Tiles
    def test_getMangroveFruitTilesNeededNegativeAmount(self) -> None:
        """
        The getMangroveFruitTilesNeeded method must raise ValueError if
        mangrove fruit amount is negative.
        """
        errMsg = "Mangrove fruit amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMangroveFruitTilesNeeded(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMangroveFruitTilesNeededSuccess(self) -> None:
        """
        The getMangroveFruitTilesNeeded method must correctly calculate tiles
        needed.
        """
        self.uut.factionData.getTreeHarvestTime.return_value = 10
        self.uut.factionData.getTreeHarvestYield.return_value = 4

        result = self.uut.getMangroveFruitTilesNeeded(10.0)

        # Production per tile = 4 / 10 = 0.4
        # Tiles needed = ceil(10.0 / 0.4) = ceil(25) = 25
        self.assertEqual(25, result)
        self.uut.factionData.getTreeHarvestTime.assert_called_once()
        self.uut.factionData.getTreeHarvestYield.assert_called_once()
        self.uut.factionData.getTreeHarvestTime \
            .assert_called_once_with(TreeName.MANGROVE_TREE)
        self.uut.factionData.getTreeHarvestYield \
            .assert_called_once_with(TreeName.MANGROVE_TREE)

    # Test Cases for Coffee Brewery
    def test_getCoffeeBreweriesNeededForCoffeeNegativeAmount(self) -> None:
        """
        The getCoffeeBreweriesNeededForCoffee method must raise ValueError
        if coffee amount is negative.
        """
        errMsg = "Coffee amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCoffeeBreweriesNeededForCoffee(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCoffeeBreweriesNeededForCoffeeSuccess(self) -> None:
        """
        The getCoffeeBreweriesNeededForCoffee method must correctly
        calculate breweries needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 1.0
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .return_value = 1

        result = self.uut.getCoffeeBreweriesNeededForCoffee(30.0)

        # Production per brewery per day = (1 / 1.0) * 24 = 24
        # Breweries needed = ceil(30.0 / 24) = ceil(1.25) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()

    def test_getCoffeeBeansNeededForCoffeeProductionNegativeCount(self) -> None:    # noqa: E501
        """
        The getCoffeeBeansNeededForCoffeeProduction method must raise
        ValueError if breweries count is negative.
        """
        errMsg = "Coffee breweries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCoffeeBeansNeededForCoffeeProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCoffeeBeansNeededForCoffeeProductionSuccess(self) -> None:
        """
        The getCoffeeBeansNeededForCoffeeProduction method must correctly
        calculate coffee beans needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 1.0
        self.uut.factionData.getFoodProcessingInputQuantity \
            .return_value = 1

        result = self.uut.getCoffeeBeansNeededForCoffeeProduction(3)

        # Cycles per day = 24 / 1.0 = 24
        # Coffee beans per brewery per day = 1 * 24 = 24
        # Total coffee beans = 3 * 24 = 72
        self.assertEqual(72, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getWaterNeededForCoffeeProductionNegativeCount(self) -> None:
        """
        The getWaterNeededForCoffeeProduction method must raise ValueError
        if breweries count is negative.
        """
        errMsg = "Coffee breweries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWaterNeededForCoffeeProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWaterNeededForCoffeeProductionSuccess(self) -> None:
        """
        The getWaterNeededForCoffeeProduction method must correctly
        calculate water needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 1.0
        self.uut.factionData.getFoodProcessingInputQuantity \
            .return_value = 1

        result = self.uut.getWaterNeededForCoffeeProduction(3)

        # Cycles per day = 24 / 1.0 = 24
        # Water per brewery per day = 1 * 24 = 24
        # Total water = 3 * 24 = 72
        self.assertEqual(72, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getLogsNeededForCoffeeProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForCoffeeProduction method must raise ValueError
        if breweries count is negative.
        """
        errMsg = "Coffee breweries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForCoffeeProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForCoffeeProductionSuccess(self) -> None:
        """
        The getLogsNeededForCoffeeProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 1.0
        self.uut.factionData.getFoodProcessingInputQuantity \
            .return_value = 0.1

        result = self.uut.getLogsNeededForCoffeeProduction(3)

        # Cycles per day = 24 / 1.0 = 24
        # Logs per brewery per day = 0.1 * 24 = 2.4
        # Total logs = 3 * 2.4 = 7.2
        # Ceiling of 7.2 = 8
        self.assertEqual(8, result)
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    # Test Cases for Fermenter
    def test_getFermentersNeededForFermentedCassavaNegativeAmount(
            self) -> None:
        """
        The getFermentersNeededForFermentedCassava method must raise
        ValueError if amount is negative.
        """
        errMsg = "Fermented cassava amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFermentersNeededForFermentedCassava(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFermentersNeededForFermentedCassavaSuccess(self) -> None:
        """
        The getFermentersNeededForFermentedCassava method must correctly
        calculate fermenters needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 2.0
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 10
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getFermentersNeededForFermentedCassava(100.0)

        # Cycles per day = 24 / 2.0 = 12
        # Output per building = 10 * 12 * 1 = 120
        # Fermenters needed = 100 / 120 = 0.833... -> ceil = 1
        self.assertEqual(1, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getCassavasNeededForFermentedCassavaProductionNegativeCount(
            self) -> None:
        """
        The getCassavasNeededForFermentedCassavaProduction method must
        raise ValueError if count is negative.
        """
        errMsg = "Fermenters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCassavasNeededForFermentedCassavaProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCassavasNeededForFermentedCassavaProductionSuccess(
            self) -> None:
        """
        The getCassavasNeededForFermentedCassavaProduction method must
        correctly calculate cassavas needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 2.0
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 4

        result = self.uut.getCassavasNeededForFermentedCassavaProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Cassavas per fermenter per day = 4 * 12 = 48
        # Total cassavas = 3 * 48 = 144
        self.assertEqual(144, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getFermentersNeededForFermentedSoybeanNegativeAmount(
            self) -> None:
        """
        The getFermentersNeededForFermentedSoybean method must raise
        ValueError if amount is negative.
        """
        errMsg = "Fermented soybean amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFermentersNeededForFermentedSoybean(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFermentersNeededForFermentedSoybeanSuccess(self) -> None:
        """
        The getFermentersNeededForFermentedSoybean method must correctly
        calculate fermenters needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 3.0
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 20
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getFermentersNeededForFermentedSoybean(150.0)

        # Cycles per day = 24 / 3.0 = 8
        # Output per building = 20 * 8 * 1 = 160
        # Fermenters needed = 150 / 160 = 0.9375 -> ceil = 1
        self.assertEqual(1, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getSoybeansNeededForFermentedSoybeanProductionNegativeCount(
            self) -> None:
        """
        The getSoybeansNeededForFermentedSoybeanProduction method must
        raise ValueError if count is negative.
        """
        errMsg = "Fermenters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getSoybeansNeededForFermentedSoybeanProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSoybeansNeededForFermentedSoybeanProductionSuccess(
            self) -> None:
        """
        The getSoybeansNeededForFermentedSoybeanProduction method must
        correctly calculate soybeans needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 3.0
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 6

        result = self.uut.getSoybeansNeededForFermentedSoybeanProduction(2)

        # Cycles per day = 24 / 3.0 = 8
        # Soybeans per fermenter per day = 6 * 8 = 48
        # Total soybeans = 2 * 48 = 96
        self.assertEqual(96, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getCanolaOilNeededForFermentedSoybeanProductionNegativeCount(
            self) -> None:
        """
        The getCanolaOilNeededForFermentedSoybeanProduction method must
        raise ValueError if count is negative.
        """
        errMsg = "Fermenters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCanolaOilNeededForFermentedSoybeanProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCanolaOilNeededForFermentedSoybeanProductionSuccess(
            self) -> None:
        """
        The getCanolaOilNeededForFermentedSoybeanProduction method must
        correctly calculate canola oil needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 3.0
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getCanolaOilNeededForFermentedSoybeanProduction(2)

        # Cycles per day = 24 / 3.0 = 8
        # Canola oil per fermenter per day = 1 * 8 = 8
        # Total canola oil = 2 * 8 = 16
        self.assertEqual(16, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getFermentersNeededForFermentedMushroomNegativeAmount(
            self) -> None:
        """
        The getFermentersNeededForFermentedMushroom method must raise
        ValueError if amount is negative.
        """
        errMsg = "Fermented mushroom amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFermentersNeededForFermentedMushroom(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFermentersNeededForFermentedMushroomSuccess(self) -> None:
        """
        The getFermentersNeededForFermentedMushroom method must correctly
        calculate fermenters needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 2.0
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 16
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getFermentersNeededForFermentedMushroom(180.0)

        # Cycles per day = 24 / 2.0 = 12
        # Output per building = 16 * 12 * 1 = 192
        # Fermenters needed = 180 / 192 = 0.9375 -> ceil = 1
        self.assertEqual(1, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getMushroomsNeededForFermentedMushroomProductionNegativeCount(
            self) -> None:
        """
        The getMushroomsNeededForFermentedMushroomProduction method must
        raise ValueError if count is negative.
        """
        errMsg = "Fermenters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMushroomsNeededForFermentedMushroomProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMushroomsNeededForFermentedMushroomProductionSuccess(
            self) -> None:
        """
        The getMushroomsNeededForFermentedMushroomProduction method must
        correctly calculate mushrooms needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 2.0
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 4

        result = self.uut.getMushroomsNeededForFermentedMushroomProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Mushrooms per fermenter per day = 4 * 12 = 48
        # Total mushrooms = 3 * 48 = 144
        self.assertEqual(144, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    # Test Cases for Food Factory
    def test_getFoodFactoriesNeededForCornRationsNegativeAmount(
            self) -> None:
        """
        The getFoodFactoriesNeededForCornRations method must raise
        ValueError if amount is negative.
        """
        errMsg = "Corn rations amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodFactoriesNeededForCornRations(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodFactoriesNeededForCornRationsSuccess(self) -> None:
        """
        The getFoodFactoriesNeededForCornRations method must correctly
        calculate food factories needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 5
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getFoodFactoriesNeededForCornRations(200.0)

        # Cycles per day = 24 / 0.5 = 48
        # Output per building = 5 * 48 * 1 = 240
        # Food factories needed = 200 / 240 = 0.833... -> ceil = 1
        self.assertEqual(1, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getCornNeededForCornRationsProductionNegativeCount(
            self) -> None:
        """
        The getCornNeededForCornRationsProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCornNeededForCornRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCornNeededForCornRationsProductionSuccess(self) -> None:
        """
        The getCornNeededForCornRationsProduction method must correctly
        calculate corn needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getCornNeededForCornRationsProduction(2)

        # Cycles per day = 24 / 0.5 = 48
        # Corn per factory per day = 1 * 48 = 48
        # Total corn = 2 * 48 = 96
        self.assertEqual(96, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getLogsNeededForCornRationsProductionNegativeCount(
            self) -> None:
        """
        The getLogsNeededForCornRationsProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForCornRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForCornRationsProductionSuccess(self) -> None:
        """
        The getLogsNeededForCornRationsProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForCornRationsProduction(2)

        # Cycles per day = 24 / 0.5 = 48
        # Logs per factory per day = 0.1 * 48 = 4.8
        # Total logs = 2 * 4.8 = 9.6 -> ceil = 10
        self.assertEqual(10, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getFoodFactoriesNeededForEggplantRationsNegativeAmount(
            self) -> None:
        """
        The getFoodFactoriesNeededForEggplantRations method must raise
        ValueError if amount is negative.
        """
        errMsg = "Eggplant rations amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodFactoriesNeededForEggplantRations(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodFactoriesNeededForEggplantRationsSuccess(self) -> None:
        """
        The getFoodFactoriesNeededForEggplantRations method must correctly
        calculate food factories needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 6
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getFoodFactoriesNeededForEggplantRations(250.0)

        # Cycles per day = 24 / 0.5 = 48
        # Output per building = 6 * 48 * 1 = 288
        # Food factories needed = 250 / 288 = 0.868... -> ceil = 1
        self.assertEqual(1, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getEggplantsNeededForEggplantRationsProductionNegativeCount(
            self) -> None:
        """
        The getEggplantsNeededForEggplantRationsProduction method must
        raise ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getEggplantsNeededForEggplantRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getEggplantsNeededForEggplantRationsProductionSuccess(
            self) -> None:
        """
        The getEggplantsNeededForEggplantRationsProduction method must
        correctly calculate eggplants needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getEggplantsNeededForEggplantRationsProduction(2)

        # Cycles per day = 24 / 0.5 = 48
        # Eggplants per factory per day = 1 * 48 = 48
        # Total eggplants = 2 * 48 = 96
        self.assertEqual(96, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getCanolaOilNeededForEggplantRationsProductionNegativeCount(
            self) -> None:
        """
        The getCanolaOilNeededForEggplantRationsProduction method must
        raise ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCanolaOilNeededForEggplantRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCanolaOilNeededForEggplantRationsProductionSuccess(
            self) -> None:
        """
        The getCanolaOilNeededForEggplantRationsProduction method must
        correctly calculate canola oil needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getCanolaOilNeededForEggplantRationsProduction(2)

        # Cycles per day = 24 / 0.5 = 48
        # Canola oil per factory per day = 1 * 48 = 48
        # Total canola oil = 2 * 48 = 96
        self.assertEqual(96, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getLogsNeededForEggplantRationsProductionNegativeCount(
            self) -> None:
        """
        The getLogsNeededForEggplantRationsProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForEggplantRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForEggplantRationsProductionSuccess(self) -> None:
        """
        The getLogsNeededForEggplantRationsProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 0.5
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForEggplantRationsProduction(2)

        # Cycles per day = 24 / 0.5 = 48
        # Logs per factory per day = 0.1 * 48 = 4.8
        # Total logs = 2 * 4.8 = 9.6 -> ceil = 10
        self.assertEqual(10, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getFoodFactoriesNeededForAlgaeRationsNegativeAmount(
            self) -> None:
        """
        The getFoodFactoriesNeededForAlgaeRations method must raise
        ValueError if amount is negative.
        """
        errMsg = "Algae rations amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getFoodFactoriesNeededForAlgaeRations(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getFoodFactoriesNeededForAlgaeRationsSuccess(self) -> None:
        """
        The getFoodFactoriesNeededForAlgaeRations method must correctly
        calculate food factories needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 6
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getFoodFactoriesNeededForAlgaeRations(500.0)

        # Cycles per day = 24 / 0.25 = 96
        # Output per building = 6 * 96 * 1 = 576
        # Food factories needed = 500 / 576 = 0.868... -> ceil = 1
        self.assertEqual(1, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getAlgaeNeededForAlgaeRationsProductionNegativeCount(
            self) -> None:
        """
        The getAlgaeNeededForAlgaeRationsProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getAlgaeNeededForAlgaeRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getAlgaeNeededForAlgaeRationsProductionSuccess(self) -> None:
        """
        The getAlgaeNeededForAlgaeRationsProduction method must correctly
        calculate algae needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getAlgaeNeededForAlgaeRationsProduction(2)

        # Cycles per day = 24 / 0.25 = 96
        # Algae per factory per day = 1 * 96 = 96
        # Total algae = 2 * 96 = 192
        self.assertEqual(192, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getCanolaOilNeededForAlgaeRationsProductionNegativeCount(
            self) -> None:
        """
        The getCanolaOilNeededForAlgaeRationsProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCanolaOilNeededForAlgaeRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCanolaOilNeededForAlgaeRationsProductionSuccess(
            self) -> None:
        """
        The getCanolaOilNeededForAlgaeRationsProduction method must
        correctly calculate canola oil needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getCanolaOilNeededForAlgaeRationsProduction(2)

        # Cycles per day = 24 / 0.25 = 96
        # Canola oil per factory per day = 1 * 96 = 96
        # Total canola oil = 2 * 96 = 192
        self.assertEqual(192, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getLogsNeededForAlgaeRationsProductionNegativeCount(
            self) -> None:
        """
        The getLogsNeededForAlgaeRationsProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Food factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForAlgaeRationsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForAlgaeRationsProductionSuccess(self) -> None:
        """
        The getLogsNeededForAlgaeRationsProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 2
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 0.25
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 0.1

        result = self.uut.getLogsNeededForAlgaeRationsProduction(2)

        # Cycles per day = 24 / 0.25 = 96
        # Logs per factory per day = 0.1 * 96 = 9.6
        # Total logs = 2 * 9.6 = 19.2 -> ceil = 20
        self.assertEqual(20, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    # Test Cases for Hydroponic Garden
    def test_getHydroponicGardensNeededForMushroomsNegativeAmount(
            self) -> None:
        """
        The getHydroponicGardensNeededForMushrooms method must raise
        ValueError if amount is negative.
        """
        errMsg = "Mushrooms amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getHydroponicGardensNeededForMushrooms(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getHydroponicGardensNeededForMushroomsSuccess(self) -> None:
        """
        The getHydroponicGardensNeededForMushrooms method must correctly
        calculate hydroponic gardens needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 192.0
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 45
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getHydroponicGardensNeededForMushrooms(6.0)

        # Cycles per day = 24 / 192.0 = 0.125
        # Output per building = 45 * 0.125 * 1 = 5.625
        # Gardens needed = 6.0 / 5.625 = 1.0666... -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getWaterNeededForMushroomsProductionNegativeCount(
            self) -> None:
        """
        The getWaterNeededForMushroomsProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Hydroponic gardens count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWaterNeededForMushroomsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWaterNeededForMushroomsProductionSuccess(self) -> None:
        """
        The getWaterNeededForMushroomsProduction method must correctly
        calculate water needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 192.0
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 40

        result = self.uut.getWaterNeededForMushroomsProduction(3)

        # Cycles per day = 24 / 192.0 = 0.125
        # Water per garden per day = 40 * 0.125 = 5
        # Total water = 3 * 5 = 15
        self.assertEqual(15, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    def test_getHydroponicGardensNeededForAlgaeNegativeAmount(
            self) -> None:
        """
        The getHydroponicGardensNeededForAlgae method must raise
        ValueError if amount is negative.
        """
        errMsg = "Algae amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getHydroponicGardensNeededForAlgae(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getHydroponicGardensNeededForAlgaeSuccess(self) -> None:
        """
        The getHydroponicGardensNeededForAlgae method must correctly
        calculate hydroponic gardens needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 288.0
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 70
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getHydroponicGardensNeededForAlgae(6.0)

        # Cycles per day = 24 / 288.0 = 0.083333...
        # Output per building = 70 * 0.083333... * 1 = 5.833333...
        # Gardens needed = 6.0 / 5.833333... = 1.0285... -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getWaterNeededForAlgaeProductionNegativeCount(self) -> None:
        """
        The getWaterNeededForAlgaeProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Hydroponic gardens count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWaterNeededForAlgaeProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWaterNeededForAlgaeProductionSuccess(self) -> None:
        """
        The getWaterNeededForAlgaeProduction method must correctly
        calculate water needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 1
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 288.0
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 60

        result = self.uut.getWaterNeededForAlgaeProduction(3)

        # Cycles per day = 24 / 288.0 = 0.083333...
        # Water per garden per day = 60 * 0.083333... = 5
        # Total water = 3 * 5 = 15
        self.assertEqual(15, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    # Test Cases for Oil Press
    def test_getOilPressesNeededForCanolaOilNegativeAmount(self) -> None:
        """
        The getOilPressesNeededForCanolaOil method must raise
        ValueError if amount is negative.
        """
        errMsg = "Canola oil amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getOilPressesNeededForCanolaOil(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getOilPressesNeededForCanolaOilSuccess(self) -> None:
        """
        The getOilPressesNeededForCanolaOil method must correctly
        calculate oil presses needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 1.3
        self.uut.factionData.getFoodProcessingOutputQuantity.return_value = 1
        self.uut.factionData.getFoodProcessingWorkers.return_value = 1

        result = self.uut.getOilPressesNeededForCanolaOil(20.0)

        # Cycles per day = 24 / 1.3 = 18.461538...
        # Output per building = 1 * 18.461538... * 1 = 18.461538...
        # Oil presses needed = 20.0 / 18.461538... = 1.083... -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingOutputQuantity \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingWorkers.assert_called_once()

    def test_getCanolaSeedsNeededForCanolaOilProductionNegativeCount(
            self) -> None:
        """
        The getCanolaSeedsNeededForCanolaOilProduction method must raise
        ValueError if count is negative.
        """
        errMsg = "Oil presses count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCanolaSeedsNeededForCanolaOilProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCanolaSeedsNeededForCanolaOilProductionSuccess(self) -> None:
        """
        The getCanolaSeedsNeededForCanolaOilProduction method must
        correctly calculate canola seeds needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex.return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime.return_value = 1.3
        self.uut.factionData.getFoodProcessingInputQuantity.return_value = 1

        result = self.uut.getCanolaSeedsNeededForCanolaOilProduction(2)

        # Cycles per day = 24 / 1.3 = 18.461538...
        # Canola seeds per press per day = 1 * 18.461538... = 18.461538...
        # Total canola seeds = 2 * 18.461538... = 36.923... -> ceil = 37
        self.assertEqual(37, result)
        self.uut.factionData.getFoodProcessingRecipeIndex.assert_called_once()
        self.uut.factionData.getFoodProcessingProductionTime \
            .assert_called_once()
        self.uut.factionData.getFoodProcessingInputQuantity \
            .assert_called_once()

    # Test Cases for Industrial Lumber Mill
    def test_getIndustrialLumberMillsNeededForPlanksNegativeAmount(
            self) -> None:
        """
        The getIndustrialLumberMillsNeededForPlanks method must raise
        ValueError if planks amount is negative.
        """
        errMsg = "Planks amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getIndustrialLumberMillsNeededForPlanks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getIndustrialLumberMillsNeededForPlanksSuccess(self) -> None:
        """
        The getIndustrialLumberMillsNeededForPlanks method must correctly
        calculate industrial lumber mills needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 0.63
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1

        result = self.uut.getIndustrialLumberMillsNeededForPlanks(50.0)

        # Production per mill per day = (1 / 0.63) * 24 = 38.095...
        # Mills needed = ceil(50.0 / 38.095...) = ceil(1.312...) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()

    def test_getLogsNeededForPlanksProductionNegativeCount(self) -> None:
        """
        The getLogsNeededForPlanksProduction method must raise
        ValueError if mills count is negative.
        """
        errMsg = "Industrial lumber mills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForPlanksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForPlanksProductionSuccess(self) -> None:
        """
        The getLogsNeededForPlanksProduction method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 0.63
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getLogsNeededForPlanksProduction(3)

        # Cycles per day = 24 / 0.63 = 38.095...
        # Logs per mill per day = 1 * 38.095... = 38.095...
        # Total logs = 3 * 38.095... = 114.285...
        self.assertEqual(115, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()

    # Test Cases for Gear Workshop
    def test_getGearWorkshopsNeededForGearsNegativeAmount(self) -> None:
        """
        The getGearWorkshopsNeededForGears method must raise ValueError
        if gears amount is negative.
        """
        errMsg = "Gears amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGearWorkshopsNeededForGears(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGearWorkshopsNeededForGearsSuccess(self) -> None:
        """
        The getGearWorkshopsNeededForGears method must correctly
        calculate gear workshops needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getGearWorkshopsNeededForGears(10.0)

        # Cycles per day = 24 / 3.0 = 8
        # Output per building = 1 * 8 * 1 = 8
        # Gear workshops needed = 10.0 / 8 = 1.25 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getPlanksNeededForGearsProductionNegativeCount(self) -> None:
        """
        The getPlanksNeededForGearsProduction method must raise ValueError
        if gear workshops count is negative.
        """
        errMsg = "Gear workshops count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForGearsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForGearsProductionSuccess(self) -> None:
        """
        The getPlanksNeededForGearsProduction method must correctly
        calculate planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getPlanksNeededForGearsProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Planks per workshop per day = 1 * 8 = 8
        # Total planks = 3 * 8 = 24
        self.assertEqual(24, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()

    # Test Cases for Wood Workshop
    def test_getWoodWorkshopsNeededForTreatedPlanksNegativeAmount(self) -> None:    # noqa: E501
        errMsg = "Treated planks amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getWoodWorkshopsNeededForTreatedPlanks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getWoodWorkshopsNeededForTreatedPlanksSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getWoodWorkshopsNeededForTreatedPlanks(20.0)

        # Cycles per day = 24 / 3.0 = 8
        # Output per building = 1 * 8 * 2 = 16
        # Wood workshops needed = 20.0 / 16 = 1.25 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getPineResinNeededForTreatedPlanksProductionNegativeCount(self) -> None:   # noqa: E501
        errMsg = "Wood workshops count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPineResinNeededForTreatedPlanksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPineResinNeededForTreatedPlanksProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getPineResinNeededForTreatedPlanksProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Pine resin per workshop per day = 1 * 8 * 2 = 16
        # Total pine resin = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getPlanksNeededForTreatedPlanksProductionNegativeCount(self) -> None:  # noqa: E501
        errMsg = "Wood workshops count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForTreatedPlanksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForTreatedPlanksProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getPlanksNeededForTreatedPlanksProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Planks per workshop per day = 1 * 8 * 2 = 16
        # Total planks = 3 * 16 = 48
        self.assertEqual(48, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Smelter
    def test_getSmeltersNeededForMetalBlocksNegativeAmount(self) -> None:
        errMsg = "Metal blocks amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getSmeltersNeededForMetalBlocks(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getSmeltersNeededForMetalBlocksSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getSmeltersNeededForMetalBlocks(15.0)

        # Cycles per day = 24 / 2.0 = 12
        # Output per building = 1 * 12 * 1 = 12
        # Smelters needed = 15.0 / 12 = 1.25 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getScrapMetalNeededForMetalBlocksProductionNegativeCount(self) -> None:    # noqa: E501
        errMsg = "Smelters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getScrapMetalNeededForMetalBlocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getScrapMetalNeededForMetalBlocksProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getScrapMetalNeededForMetalBlocksProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Scrap metal per smelter per day = 1 * 12 * 1 = 12
        # Total scrap metal = 3 * 12 = 36
        self.assertEqual(36, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getLogsNeededForMetalBlocksProductionNegativeCount(self) -> None:
        errMsg = "Smelters count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForMetalBlocksProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForMetalBlocksProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 0.2
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getLogsNeededForMetalBlocksProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Logs per smelter per day = 0.2 * 12 * 1 = 2.4
        # Total logs = 3 * 2.4 = 7.2 -> ceil = 8
        self.assertEqual(8, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Efficient Mine
    def test_getEfficientMinesNeededForScrapMetalNegativeAmount(self) -> None:
        """
        The getEfficientMinesNeededForScrapMetal method must raise
        ValueError if scrap metal amount is negative.
        """
        errMsg = "Scrap metal amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getEfficientMinesNeededForScrapMetal(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getEfficientMinesNeededForScrapMetalSuccess(self) -> None:
        """
        The getEfficientMinesNeededForScrapMetal method must correctly
        calculate efficient mines needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.8
        self.uut.factionData.getGoodsOutputQuantity.return_value = 5

        result = self.uut.getEfficientMinesNeededForScrapMetal(100.0)

        # Production per mine per day = (5 / 1.8) * 24 = 66.666...
        # Mines needed = ceil(100.0 / 66.666...) = ceil(1.5) = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()

    def test_getTreatedPlanksNeededForScrapMetalProductionNegativeCount(
            self) -> None:
        """
        The getTreatedPlanksNeededForScrapMetalProduction method must raise
        ValueError if efficient mines count is negative.
        """
        errMsg = "Efficient mines count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getTreatedPlanksNeededForScrapMetalProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getTreatedPlanksNeededForScrapMetalProductionSuccess(self) -> None:    # noqa: E501
        """
        The getTreatedPlanksNeededForScrapMetalProduction method must correctly
        calculate treated planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.8
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getTreatedPlanksNeededForScrapMetalProduction(3)

        # Cycles per day = 24 / 1.8 = 13.333...
        # Treated planks per mine per day = 1 * 13.333... = 13.333...
        # Total treated planks = 3 * 13.333... = 40
        self.assertEqual(40, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()

    # Test Cases for Grease Factory
    def test_getGreaseFactoriesNeededForGreaseNegativeAmount(self) -> None:
        errMsg = "Grease amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGreaseFactoriesNeededForGrease(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGreaseFactoriesNeededForGreaseSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 2
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getGreaseFactoriesNeededForGrease(50.0)

        # Cycles per day = 24 / 2.0 = 12
        # Output per building = 2 * 12 * 2 = 48
        # Grease factories needed = 50.0 / 48 = 1.042 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getExtractNeededForGreaseProductionNegativeCount(self) -> None:
        errMsg = "Grease factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getExtractNeededForGreaseProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getExtractNeededForGreaseProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getExtractNeededForGreaseProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Extract per factory per day = 1 * 12 * 2 = 24
        # Total extract = 3 * 24 = 72
        self.assertEqual(72, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getCanolaOilNeededForGreaseProductionNegativeCount(self) -> None:
        errMsg = "Grease factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCanolaOilNeededForGreaseProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCanolaOilNeededForGreaseProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 2.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getCanolaOilNeededForGreaseProduction(3)

        # Cycles per day = 24 / 2.0 = 12
        # Canola oil per factory per day = 1 * 12 * 2 = 24
        # Total canola oil = 3 * 24 = 72
        self.assertEqual(72, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Bot Part Factory - Bot Chassis
    def test_getBotPartFactoriesNeededForBotChassisNegativeAmount(self) -> None:    # noqa: E501
        errMsg = "Bot chassis amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotPartFactoriesNeededForBotChassis(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotPartFactoriesNeededForBotChassisSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getBotPartFactoriesNeededForBotChassis(2.0)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Output per building = 1 * 1.333... * 1 = 1.333...
        # Bot part factories needed = 2.0 / 1.333... = 1.5 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getPlanksNeededForBotChassisProductionNegativeCount(self) -> None:
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForBotChassisProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForBotChassisProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 5
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getPlanksNeededForBotChassisProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Planks per factory per day = 5 * 1.333... * 1 = 6.666... -> ceil = 7
        # Total planks = 2 * 7 = 14
        self.assertEqual(14, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getMetalBlocksNeededForBotChassisProductionNegativeCount(self) -> None:    # noqa: E501
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMetalBlocksNeededForBotChassisProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMetalBlocksNeededForBotChassisProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getMetalBlocksNeededForBotChassisProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Metal blocks per factory per day = 1 * 1.333... * 1 = 1.333...
        # Total metal blocks = 2 * 1.333... = 2.666... -> ceil = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getBiofuelNeededForBotChassisProductionNegativeCount(self) -> None:    # noqa: E501
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBiofuelNeededForBotChassisProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBiofuelNeededForBotChassisProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getBiofuelNeededForBotChassisProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Biofuel per factory per day = 1 * 1.333... * 1 = 1.333...
        # Total biofuel = 2 * 1.333... = 2.666... -> ceil = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Bot Part Factory - Bot Heads
    def test_getBotPartFactoriesNeededForBotHeadsNegativeAmount(self) -> None:
        errMsg = "Bot heads amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotPartFactoriesNeededForBotHeads(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotPartFactoriesNeededForBotHeadsSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getBotPartFactoriesNeededForBotHeads(2.0)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Output per building = 1 * 1.333... * 1 = 1.333...
        # Bot part factories needed = 2.0 / 1.333... = 1.5 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getGearsNeededForBotHeadsProductionNegativeCount(self) -> None:
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGearsNeededForBotHeadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGearsNeededForBotHeadsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 3
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getGearsNeededForBotHeadsProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Gears per factory per day = 3 * 1.333... * 1 = 4
        # Total gears = 2 * 4 = 8
        self.assertEqual(8, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getMetalBlocksNeededForBotHeadsProductionNegativeCount(self) -> None:  # noqa: E501
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getMetalBlocksNeededForBotHeadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getMetalBlocksNeededForBotHeadsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getMetalBlocksNeededForBotHeadsProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Metal blocks per factory per day = 1 * 1.333... * 1 = 1.333...
        # Total metal blocks = 2 * 1.333... = 2.666... -> ceil = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getPlanksNeededForBotHeadsProductionNegativeCount(self) -> None:
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForBotHeadsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForBotHeadsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 1
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getPlanksNeededForBotHeadsProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Planks per factory per day = 1 * 1.333... * 1 = 1.333...
        # Total planks = 2 * 1.333... = 2.666... -> ceil = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Bot Part Factory - Bot Limbs
    def test_getBotPartFactoriesNeededForBotLimbsNegativeAmount(self) -> None:
        errMsg = "Bot limbs amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotPartFactoriesNeededForBotLimbs(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotPartFactoriesNeededForBotLimbsSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getBotPartFactoriesNeededForBotLimbs(2.0)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Output per building = 1 * 1.333... * 1 = 1.333...
        # Bot part factories needed = 2.0 / 1.333... = 1.5 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getGearsNeededForBotLimbsProductionNegativeCount(self) -> None:
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getGearsNeededForBotLimbsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getGearsNeededForBotLimbsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 3
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getGearsNeededForBotLimbsProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Gears per factory per day = 3 * 1.333... * 1 = 4
        # Total gears = 2 * 4 = 8
        self.assertEqual(8, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getPlanksNeededForBotLimbsProductionNegativeCount(self) -> None:
        errMsg = "Bot part factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getPlanksNeededForBotLimbsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getPlanksNeededForBotLimbsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 2
        self.uut.factionData.getGoodsProductionTime.return_value = 18.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getPlanksNeededForBotLimbsProduction(2)

        # Cycles per day = 24 / 18.0 = 1.333...
        # Planks per factory per day = 1 * 1.333... * 1 = 1.333...
        # Total planks = 2 * 1.333... = 2.666... -> ceil = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Bot Assembler
    def test_getBotAssemblersNeededForBotsNegativeAmount(self) -> None:
        errMsg = "Bots amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotAssemblersNeededForBots(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotAssemblersNeededForBotsSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 36.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getBotAssemblersNeededForBots(2.0)

        # Cycles per day = 24 / 36.0 = 0.666...
        # Output per building = 1 * 0.666... * 2 = 1.333...
        # Bot assemblers needed = 2.0 / 1.333... = 1.5 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getBotChassisNeededForBotsProductionNegativeCount(self) -> None:
        errMsg = "Bot assemblers count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotChassisNeededForBotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotChassisNeededForBotsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 36.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getBotChassisNeededForBotsProduction(2)

        # Cycles per day = 24 / 36.0 = 0.666...
        # Bot chassis per assembler per day = 1 * 0.666... * 2 = 1.333...
        # Total bot chassis = 2 * 1.333... = 2.666... -> ceil = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getBotHeadsNeededForBotsProductionNegativeCount(self) -> None:
        errMsg = "Bot assemblers count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotHeadsNeededForBotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotHeadsNeededForBotsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 36.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getBotHeadsNeededForBotsProduction(2)

        # Cycles per day = 24 / 36.0 = 0.666...
        # Bot heads per assembler per day = 1 * 0.666... * 2 = 1.333...
        # Total bot heads = 2 * 1.333... = 2.666... -> ceil = 3
        self.assertEqual(3, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getBotLimbsNeededForBotsProductionNegativeCount(self) -> None:
        errMsg = "Bot assemblers count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBotLimbsNeededForBotsProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBotLimbsNeededForBotsProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 36.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 4
        self.uut.factionData.getGoodsWorkers.return_value = 2

        result = self.uut.getBotLimbsNeededForBotsProduction(2)

        # Cycles per day = 24 / 36.0 = 0.666...
        # Bot limbs per assembler per day = 4 * 0.666... * 2 = 5.333...
        # Total bot limbs = 2 * 5.333... = 10.666... -> ceil = 11
        self.assertEqual(11, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Explosives Factory
    def test_getExplosivesFactoriesNeededForExplosivesNegativeAmount(self) -> None:     # noqa: E501
        errMsg = "Explosives amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getExplosivesFactoriesNeededForExplosives(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getExplosivesFactoriesNeededForExplosivesSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getExplosivesFactoriesNeededForExplosives(10.0)

        # Cycles per day = 24 / 3.0 = 8
        # Output per building = 1 * 8 * 1 = 8
        # Explosives factories needed = 10.0 / 8 = 1.25 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getBadwaterNeededForExplosivesProductionNegativeCount(self) -> None:   # noqa: E501
        errMsg = "Explosives factories count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBadwaterNeededForExplosivesProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBadwaterNeededForExplosivesProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 3.0
        self.uut.factionData.getGoodsInputQuantity.return_value = 5
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getBadwaterNeededForExplosivesProduction(3)

        # Cycles per day = 24 / 3.0 = 8
        # Badwater per factory per day = 5 * 8 * 1 = 40
        # Total badwater = 3 * 40 = 120
        self.assertEqual(120, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    # Test Cases for Centrifuge
    def test_getCentrifugesNeededForExtractNegativeAmount(self) -> None:
        errMsg = "Extract amount cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCentrifugesNeededForExtract(-10.0)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCentrifugesNeededForExtractSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 0.75
        self.uut.factionData.getGoodsOutputQuantity.return_value = 1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getCentrifugesNeededForExtract(40.0)

        # Cycles per day = 24 / 0.75 = 32
        # Output per building = 1 * 32 * 1 = 32
        # Centrifuges needed = 40.0 / 32 = 1.25 -> ceil = 2
        self.assertEqual(2, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsOutputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getBadwaterNeededForExtractProductionNegativeCount(self) -> None:
        errMsg = "Centrifuges count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getBadwaterNeededForExtractProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getBadwaterNeededForExtractProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 0.75
        self.uut.factionData.getGoodsInputQuantity.return_value = 4
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getBadwaterNeededForExtractProduction(3)

        # Cycles per day = 24 / 0.75 = 32
        # Badwater per centrifuge per day = 4 * 32 * 1 = 128
        # Total badwater = 3 * 128 = 384
        self.assertEqual(384, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()

    def test_getLogsNeededForExtractProductionNegativeCount(self) -> None:
        errMsg = "Centrifuges count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForExtractProduction(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForExtractProductionSuccess(self) -> None:
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 0.75
        self.uut.factionData.getGoodsInputQuantity.return_value = 0.1
        self.uut.factionData.getGoodsWorkers.return_value = 1

        result = self.uut.getLogsNeededForExtractProduction(3)

        # Cycles per day = 24 / 0.75 = 32
        # Logs per centrifuge per day = 0.1 * 32 * 1 = 3.2
        # Total logs = 3 * 3.2 = 9.6 -> ceil = 10
        self.assertEqual(10, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
        self.uut.factionData.getGoodsWorkers.assert_called_once()
