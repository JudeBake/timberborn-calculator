from logger import initLogger

from pkgs.ui import AppComposer


def main():
    """
    Application main.
    """
    initLogger()
    app = AppComposer()
    app.run()


if __name__ == '__main__':
    main()
