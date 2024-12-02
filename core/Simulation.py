from core.World import World  # Import the World class
import logging
import numpy as np


class Simulation:
    """
    The Simulation class is responsible for managing the lifecycle of a simulation,
    including initialization, precomputing states over a specified number of days,
    and analyzing results.
    """

    def __init__(self, grid_size, initial_ratios, days):
        """
        Initialize the Simulation class with initial conditions.

        Args:
            grid_size (tuple): Dimensions of the grid (x, y, z).
            initial_ratios (dict): Initial ratios for different cell types (e.g., forest, city, desert).
            days (int): Number of days to run the simulation.
        """
        self.grid_size = grid_size
        self.initial_ratios = initial_ratios
        self.days = days
        self.states = []  # Store the history of World objects (one per day)
        # Aggregates to track various metrics over time
        self.pollution_over_time = []  # Average pollution over time
        self.temperature_over_time = []  # Average temperature over time
        self.city_population_over_time = []  # Total number of city cells over time
        self.forest_count_over_time = []  # Total number of forest cells over time
        self.water_mass_over_time = []  # Average water mass over time
        self.std_dev_pollution_over_time = []  # Standard deviation of pollution
        self.std_dev_temperature_over_time = []  # Standard deviation of temperature
        self.std_dev_water_mass_over_time = []  # Standard deviation of water mass
        # Track counts of each cell type
        self.cell_type_counts_over_time = {
            cell_type: [] for cell_type in range(10)}
        self.cell_type_std_dev_over_time = {
            # Track std dev per cell type
            cell_type: [] for cell_type in range(10)}
        # Standard deviation of cell type distribution over time
        self.std_dev_cell_distribution_over_time = []
        self.std_dev_forest_count_over_time = []  # Standard deviation of forest count
        # Standard deviation of city population
        self.std_dev_city_population_over_time = []

    def _update_aggregates(self, state):
        """
        Update aggregate metrics based on the current state of the simulation.

        Args:
            state (World): Current World object representing the state of the grid.
        """
        self.pollution_over_time.append(state.avg_pollution)
        self.temperature_over_time.append(state.avg_temperature)
        self.city_population_over_time.append(state.total_cities)
        self.forest_count_over_time.append(state.total_forests)
        self.water_mass_over_time.append(state.avg_water_mass)
        self.std_dev_pollution_over_time.append(state.std_dev_pollution)
        self.std_dev_temperature_over_time.append(state.std_dev_temperature)
        self.std_dev_water_mass_over_time.append(state.std_dev_water_mass)

        for cell_type, stats in state.cell_type_stats.items():
            self.cell_type_std_dev_over_time[cell_type].append(
                stats["std_dev_temperature"])
            self.cell_type_counts_over_time[cell_type].append(stats["count"])

        # Calculate standard deviation of cell counts
        cell_counts = [stats["count"]
                       for stats in state.cell_type_stats.values()]
        self.std_dev_cell_distribution_over_time.append(
            self._calculate_standard_deviation(cell_counts))

        # Compute standard deviation for forests and cities
        self.std_dev_forest_count_over_time.append(
            self._calculate_standard_deviation(self.forest_count_over_time)
        )
        self.std_dev_city_population_over_time.append(
            self._calculate_standard_deviation(self.city_population_over_time)
        )

        # Log aggregate metrics
        logging.info(f"Day {state.day_number}: Total forests = {
                     state.total_forests}")
        logging.info(f"Aggregated forest count: {self.forest_count_over_time}")

        # Calculate and log standardized values for pollution, temperature, and water mass
        for param, values in {
            "pollution": self.pollution_over_time,
            "temperature": self.temperature_over_time,
            "water_mass": self.water_mass_over_time,
        }.items():
            if len(values) > 1:  # Ensure enough data points for calculations
                mean_value = np.mean(values)
                std_dev_value = np.std(values)
                standardized_values = [
                    (value - mean_value) /
                    std_dev_value if std_dev_value > 0 else 0
                    for value in values
                ]
                logging.info(
                    f"Day {state.day_number}: Standardized {param.capitalize()} Values = {
                        standardized_values}"
                )

    def precompute(self):
        """
        Run the simulation for the specified number of days and precompute all states.
        This function initializes the grid and iteratively updates it for each day.

        Steps:
        1. Initialize the first state (Day 0).
        2. For each day, clone the last state, update it, and store it.
        3. Update aggregates for analysis.
        """
        # Initialize the first state (Day 0)
        initial_state = World(
            grid_size=self.grid_size,
            initial_ratios=self.initial_ratios,
            day_number=0
        )
        initial_state.initialize_grid()
        self.states.append(initial_state)
        self._update_aggregates(initial_state)  # Update aggregates for Day 0

        # # Simulate for the specified number of days
        for day in range(self.days):
            print(f"Pre-computing Day {day}...")

            # Compute the next state by cloning the current state
            next_state = self.states[-1].clone()
            next_state.day_number += 1  # Increment the day number
            next_state.update_cells_on_grid()  # Update the grid cells
            next_state._recalculate_global_attributes()  # Recalculate global attributes
            self.states.append(next_state)  # Store the new state
            self._update_aggregates(next_state)  # Update aggregates

    def get_averages_and_std_dev_over_time(self):
        """
        Retrieve averages and standard deviations of metrics over the simulation period.

        Returns:
            dict: Averages and standard deviations of temperature, pollution, water mass, 
                  city counts, forest counts, and cell type counts.
        """
        return {
            "averages": {
                "temperature": self.temperature_over_time,
                "pollution": self.pollution_over_time,
                "water_mass": self.water_mass_over_time,
                "cities": self.city_population_over_time,
                "forests": self.forest_count_over_time,
                "cell_type_counts": self.cell_type_counts_over_time,
            },
            "std_devs": {
                "temperature": self.std_dev_temperature_over_time,
                "pollution": self.std_dev_pollution_over_time,
                "water_mass": self.std_dev_water_mass_over_time,
            }
        }

    def _calculate_standard_deviation(self, data_list):
        """
        Calculate standard deviation for a list of data points.

        Args:
            data_list (list): A list of numerical data points.

        Returns:
            float: Standard deviation of the data.
        """
        return np.std(data_list) if data_list else 0.0
