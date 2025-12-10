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
        with patch('pkgs.factions.folktail.FactionData'):
            folktail = Folktail()
            with self.assertRaises(ValueError) as context:
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
        with patch('pkgs.factions.folktail.FactionData'):
            folktail = Folktail()
            with self.assertRaises(ValueError) as context:
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
