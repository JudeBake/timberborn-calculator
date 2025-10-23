from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import yaml as yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.data.folktails import Folktails                       # noqa: E402


class TestFolktails(TestCase):
    """
    Folktails class test cases.
    """
    def setUp(self) -> None:
        """
        Test setup.
        """
        pass

    def test_constructorErrorOpenFile(self) -> None:
        """
        The constructor must raise any error raised by opening the data file.
        """
        errMsg = "File not found."
        with patch("builtins.open", mock_open()) as mockedOpen, \
                self.assertRaises(IOError) as context:
            mockedOpen.side_effect = IOError(errMsg)
            Folktails()
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorErrorLoadYaml(self) -> None:
        """
        The constructor must raise any error raised by loading the YAML data.
        """
        data = "data"
        errMsg = "YAML error."
        with patch("builtins.open", mock_open(read_data=data)) as mockedOpen, \
                patch("yaml.safe_load") as mockedYamlLoad, \
                self.assertRaises(yaml.YAMLError) as context:
            mockedYamlLoad.side_effect = yaml.YAMLError(errMsg)
            Folktails()
            mockedYamlLoad.assert_called_once_with(mockedOpen())
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorSuccess(self) -> None:
        """
        The constructor must save internally the data when the load operation
        succeeds.
        """
        data = "data"
        loadedData = {"key": "value"}
        with patch("builtins.open", mock_open(read_data=data)) as mockedOpen, \
                patch("yaml.safe_load") as mockedYamlLoad:
            mockedYamlLoad.return_value = loadedData
            folktails = Folktails()
            mockedYamlLoad.assert_called_once_with(mockedOpen())
        self.assertEqual(loadedData, folktails.data)
