import yaml as yaml


class Folktails:
    """
    Folktails data and calculation class.
    """
    def __init__(self) -> None:
        """
        Constructor.
        """
        with open("data/folktails.yaml", "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)
