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

        # Consumption = 10 * 2.75 * 1.0 = 27.5
        self.assertEqual(27.5, result)
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

        # Consumption = 10 * 2.25 * 1.0 = 22.5
        self.assertEqual(22.5, result)
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
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.PINE)
        self.uut.factionData.getTreeLogOutput \
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
        self.uut.factionData.getTreeGrowthTime \
            .assert_called_once_with(TreeName.OAK)
        self.uut.factionData.getTreeLogOutput \
            .assert_called_once_with(TreeName.OAK)

    # Test Cases for Harvest Tiles
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
        self.uut.factionData.getTreeHarvestTime \
            .assert_called_once_with(TreeName.PINE)
        self.uut.factionData.getTreeHarvestYield \
            .assert_called_once_with(TreeName.PINE)

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

    def test_getCoffeeBeansNeededForCoffeeBreweriesNegativeCount(self) -> None:
        """
        The getCoffeeBeansNeededForCoffeeBreweries method must raise
        ValueError if breweries count is negative.
        """
        errMsg = "Coffee breweries count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getCoffeeBeansNeededForCoffeeBreweries(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getCoffeeBeansNeededForCoffeeBreweriesSuccess(self) -> None:
        """
        The getCoffeeBeansNeededForCoffeeBreweries method must correctly
        calculate coffee beans needed.
        """
        self.uut.factionData.getFoodProcessingRecipeIndex \
            .return_value = 0
        self.uut.factionData.getFoodProcessingProductionTime \
            .return_value = 1.0
        self.uut.factionData.getFoodProcessingInputQuantity \
            .return_value = 1

        result = self.uut.getCoffeeBeansNeededForCoffeeBreweries(3)

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

    def test_getLogsNeededForIndustrialLumberMillsNegativeCount(self) -> None:
        """
        The getLogsNeededForIndustrialLumberMills method must raise
        ValueError if mills count is negative.
        """
        errMsg = "Industrial lumber mills count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getLogsNeededForIndustrialLumberMills(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getLogsNeededForIndustrialLumberMillsSuccess(self) -> None:
        """
        The getLogsNeededForIndustrialLumberMills method must correctly
        calculate logs needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 0.63
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getLogsNeededForIndustrialLumberMills(3)

        # Cycles per day = 24 / 0.63 = 38.095...
        # Logs per mill per day = 1 * 38.095... = 38.095...
        # Total logs = 3 * 38.095... = 114.285...
        self.assertAlmostEqual(114.285714285714, result, places=10)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()

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

    def test_getTreatedPlanksNeededForEfficientMinesNegativeCount(
            self) -> None:
        """
        The getTreatedPlanksNeededForEfficientMines method must raise
        ValueError if efficient mines count is negative.
        """
        errMsg = "Efficient mines count cannot be negative."
        with self.assertRaises(ValueError) as context:
            self.uut.getTreatedPlanksNeededForEfficientMines(-1)
        self.assertEqual(errMsg, str(context.exception))

    def test_getTreatedPlanksNeededForEfficientMinesSuccess(self) -> None:
        """
        The getTreatedPlanksNeededForEfficientMines method must correctly
        calculate treated planks needed.
        """
        self.uut.factionData.getGoodsRecipeIndex.return_value = 0
        self.uut.factionData.getGoodsProductionTime.return_value = 1.8
        self.uut.factionData.getGoodsInputQuantity.return_value = 1

        result = self.uut.getTreatedPlanksNeededForEfficientMines(3)

        # Cycles per day = 24 / 1.8 = 13.333...
        # Treated planks per mine per day = 1 * 13.333... = 13.333...
        # Total treated planks = 3 * 13.333... = 40
        self.assertEqual(40, result)
        self.uut.factionData.getGoodsRecipeIndex.assert_called_once()
        self.uut.factionData.getGoodsProductionTime.assert_called_once()
        self.uut.factionData.getGoodsInputQuantity.assert_called_once()
