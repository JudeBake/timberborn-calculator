"""
Folktail faction tab for the Timberborn Calculator.
"""

import tkinter as tk
from tkinter import ttk


class FolktailTab:
    """Folktail faction calculator tab."""

    def __init__(self, parent):
        """
        Initialize the Folktail tab.

        :param parent: The parent notebook widget.
        :type parent: ttk.Notebook
        """
        self.frame = ttk.Frame(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Set up the UI components for the Folktail tab."""
        # Main container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Difficulty selection section (top)
        self._create_difficulty_section(main_container)

        # Two-column layout for Food/Water and Goods
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Configure grid columns to be equal width
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)

        # Left column: Food and Water
        self._create_food_water_section(content_frame)

        # Right column: Goods
        self._create_goods_section(content_frame)

    def _create_difficulty_section(self, parent):
        """
        Create the difficulty selection section.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        """
        difficulty_frame = ttk.LabelFrame(
            parent, text="Difficulty", padding=(10, 5))
        difficulty_frame.pack(fill=tk.X)

        # Difficulty radio buttons
        self.difficulty_var = tk.StringVar(value="Normal")

        difficulties = ["Easy", "Normal", "Hard"]
        radio_container = ttk.Frame(difficulty_frame)
        radio_container.pack()

        for difficulty in difficulties:
            rb = ttk.Radiobutton(
                radio_container,
                text=difficulty,
                value=difficulty,
                variable=self.difficulty_var,
                command=self._on_difficulty_changed
            )
            rb.pack(side=tk.LEFT, padx=20)

    def _create_food_water_section(self, parent):
        """
        Create the Food and Water section.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        """
        food_water_frame = ttk.LabelFrame(
            parent, text="Food and Water", padding=(10, 10))
        food_water_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Target population section
        pop_frame = ttk.Frame(food_water_frame)
        pop_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(pop_frame, text="Target Population:").pack(
            side=tk.LEFT, padx=(0, 5))
        self.population_var = tk.StringVar(value="100")
        pop_entry = ttk.Entry(pop_frame, textvariable=self.population_var,
                              width=10)
        pop_entry.pack(side=tk.LEFT, padx=(0, 20))

        # Use Beehive checkbox
        self.beehive_var = tk.BooleanVar(value=False)
        beehive_cb = ttk.Checkbutton(
            pop_frame, text="Use Beehive", variable=self.beehive_var,
            command=self._on_beehive_changed
        )
        beehive_cb.pack(side=tk.LEFT)

        # Water section
        self._create_water_section(food_water_frame)

        # Food section
        self._create_food_section(food_water_frame)

    def _create_water_section(self, parent):
        """
        Create the water buildings section.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        """
        water_frame = ttk.LabelFrame(parent, text="Water", padding=(5, 5))
        water_frame.pack(fill=tk.X, pady=(0, 10))

        # Header row
        header_frame = ttk.Frame(water_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(header_frame, text="", width=3).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Building", width=15).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Workers", width=10).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Needs", width=10).pack(side=tk.LEFT)

        # Pumps row
        self._create_water_building_row(
            water_frame, "Pumps", has_workers=False)

        # Large Pumps row
        self._create_water_building_row(
            water_frame, "Large Pumps", has_workers=True)

    def _create_water_building_row(self, parent, building_name,
                                    has_workers=False):
        """
        Create a row for a water building.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        :param building_name: Name of the building.
        :type building_name: str
        :param has_workers: Whether this building has a workers input.
        :type has_workers: bool
        """
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)

        # Enable checkbox
        enabled_var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(row_frame, variable=enabled_var)
        cb.pack(side=tk.LEFT, padx=(0, 5))

        # Building label
        ttk.Label(row_frame, text=building_name, width=15).pack(side=tk.LEFT)

        # Workers input (if applicable)
        if has_workers:
            workers_var = tk.StringVar(value="6")
            workers_entry = ttk.Entry(row_frame, textvariable=workers_var,
                                      width=10)
            workers_entry.pack(side=tk.LEFT, padx=(0, 5))
        else:
            # Spacer to align with other rows
            ttk.Label(row_frame, text="", width=10).pack(side=tk.LEFT)

        # Needs display
        needs_var = tk.StringVar(value="0")
        needs_label = ttk.Label(row_frame, textvariable=needs_var,
                                width=10, relief=tk.SUNKEN)
        needs_label.pack(side=tk.LEFT)

        # Store references for later use
        if not hasattr(self, 'water_buildings'):
            self.water_buildings = {}
        self.water_buildings[building_name] = {
            'enabled': enabled_var,
            'needs': needs_var
        }
        if has_workers:
            self.water_buildings[building_name]['workers'] = workers_var

    def _create_food_section(self, parent):
        """
        Create the food production section.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        """
        food_frame = ttk.LabelFrame(parent, text="Food", padding=(5, 5))
        food_frame.pack(fill=tk.BOTH, expand=True)

        # Header row
        header_frame = ttk.Frame(food_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(header_frame, text="", width=3).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Food Type", width=20).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Buildings", width=10).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Tiles/Trees", width=10).pack(
            side=tk.LEFT)

        # Scrollable frame for food items
        canvas = tk.Canvas(food_frame, height=200)
        scrollbar = ttk.Scrollbar(
            food_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Food items (examples - will need to be populated from data)
        food_items = [
            ("Grilled Potatoes", "Grill", "Potatoes"),
            ("Grilled Chestnuts", "Grill", "Chestnuts"),
            ("Grilled Spadderdocks", "Grill", "Spadderdocks"),
            ("Breads", "Bakery", "Wheat"),
            ("Cattail Crackers", "Bakery", "Cattail"),
            ("Maple Pastries", "Bakery", "Maple Syrup"),
        ]

        self.food_items = {}
        for food_name, building, crop in food_items:
            self._create_food_item_row(
                scrollable_frame, food_name, building, crop)

    def _create_food_item_row(self, parent, food_name, building, crop):
        """
        Create a row for a food item.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        :param food_name: Name of the food item.
        :type food_name: str
        :param building: Building type needed.
        :type building: str
        :param crop: Crop/resource needed.
        :type crop: str
        """
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)

        # Enable checkbox
        enabled_var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(row_frame, variable=enabled_var)
        cb.pack(side=tk.LEFT, padx=(0, 5))

        # Food name label
        ttk.Label(row_frame, text=food_name, width=20).pack(side=tk.LEFT)

        # Buildings needed display
        buildings_var = tk.StringVar(value="0")
        buildings_label = ttk.Label(
            row_frame, textvariable=buildings_var, width=10, relief=tk.SUNKEN)
        buildings_label.pack(side=tk.LEFT, padx=(0, 5))

        # Tiles/Trees needed display
        tiles_var = tk.StringVar(value="0")
        tiles_label = ttk.Label(
            row_frame, textvariable=tiles_var, width=10, relief=tk.SUNKEN)
        tiles_label.pack(side=tk.LEFT)

        # Store references
        self.food_items[food_name] = {
            'enabled': enabled_var,
            'building': building,
            'crop': crop,
            'buildings_needed': buildings_var,
            'tiles_needed': tiles_var
        }

    def _create_goods_section(self, parent):
        """
        Create the goods production section.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        """
        goods_frame = ttk.LabelFrame(
            parent, text="Goods", padding=(10, 10))
        goods_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Header row
        header_frame = ttk.Frame(goods_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(header_frame, text="", width=3).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Good Type", width=20).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Target", width=10).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Buildings", width=10).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Input Needed", width=12).pack(
            side=tk.LEFT)

        # Scrollable frame for goods items
        canvas = tk.Canvas(goods_frame)
        scrollbar = ttk.Scrollbar(
            goods_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Goods items (examples - will need to be populated from data)
        goods_items = [
            ("Planks", "Lumber Mill", "Logs"),
            ("Gears", "Gear Workshop", "Planks"),
            ("Paper", "Paper Mill", "Logs"),
            ("Treated Planks", "Wood Workshop", "Planks + Pine Resin"),
            ("Metal Blocks", "Smelter", "Scrap Metal + Logs"),
            ("Books", "Printing Press", "Paper"),
        ]

        self.goods_items = {}
        for good_name, building, inputs in goods_items:
            self._create_goods_item_row(
                scrollable_frame, good_name, building, inputs)

    def _create_goods_item_row(self, parent, good_name, building, inputs):
        """
        Create a row for a goods item.

        :param parent: Parent widget.
        :type parent: ttk.Frame
        :param good_name: Name of the good.
        :type good_name: str
        :param building: Building type needed.
        :type building: str
        :param inputs: Input resources needed.
        :type inputs: str
        """
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)

        # Enable checkbox
        enabled_var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(row_frame, variable=enabled_var)
        cb.pack(side=tk.LEFT, padx=(0, 5))

        # Good name label
        ttk.Label(row_frame, text=good_name, width=20).pack(side=tk.LEFT)

        # Target production input
        target_var = tk.StringVar(value="0")
        target_entry = ttk.Entry(row_frame, textvariable=target_var, width=10)
        target_entry.pack(side=tk.LEFT, padx=(0, 5))

        # Buildings needed display
        buildings_var = tk.StringVar(value="0")
        buildings_label = ttk.Label(
            row_frame, textvariable=buildings_var, width=10, relief=tk.SUNKEN)
        buildings_label.pack(side=tk.LEFT, padx=(0, 5))

        # Input needed display
        input_needed_var = tk.StringVar(value="0")
        input_label = ttk.Label(
            row_frame, textvariable=input_needed_var, width=12,
            relief=tk.SUNKEN)
        input_label.pack(side=tk.LEFT)

        # Store references
        self.goods_items[good_name] = {
            'enabled': enabled_var,
            'building': building,
            'inputs': inputs,
            'target': target_var,
            'buildings_needed': buildings_var,
            'input_needed': input_needed_var
        }

    def _on_difficulty_changed(self):
        """Handle difficulty selection change."""
        # TODO: Recalculate all values based on new difficulty
        pass

    def _on_beehive_changed(self):
        """Handle beehive checkbox change."""
        # TODO: Recalculate food/crop values
        pass
