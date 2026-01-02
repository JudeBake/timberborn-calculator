#!/usr/bin/env python3
"""
Main entry point for the Timberborn Calculator desktop application.
"""

import tkinter as tk
from tkinter import ttk


class TimberbornCalculatorApp:
    """Main application window for the Timberborn Calculator."""

    def __init__(self, root):
        """
        Initialize the main application window.

        :param root: The root tkinter window.
        :type root: tk.Tk
        """
        self.root = root
        self.root.title("Timberborn Calculator")
        self.root.geometry("1200x800")

        # Create the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Import tab implementations
        from folktail_tab import FolktailTab
        from ironteeth_tab import IronTeethTab

        # Create tabs
        self.folktail_tab = FolktailTab(self.notebook)
        self.ironteeth_tab = IronTeethTab(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.folktail_tab.frame, text="Folktail")
        self.notebook.add(self.ironteeth_tab.frame, text="Iron Teeth")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = TimberbornCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
