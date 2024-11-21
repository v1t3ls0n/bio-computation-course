import numpy as np
from .Cell import Cell
import logging

class State:
    def __init__(self, grid_size, initial_temperature, initial_pollution, initial_water_mass, initial_cities, initial_forests):
        """
        Initialize the State class with a 3D grid of Cell objects.
        :param grid_size: Tuple of (x, y, z) dimensions for the grid.
        :param initial_temperature: Initial temperature for all cells.
        :param initial_pollution: Initial pollution level for all cells.
        :param initial_water_mass: Initial water mass for all cells.
        :param initial_cities: (Optional) Target number of initial city cells.
        :param initial_forests: (Optional) Target number of initial forest cells.
        """
        self.grid_size = grid_size
        self.grid = self.initialize_grid(
            initial_temperature,
            initial_pollution,
            initial_water_mass,
            initial_cities,
            initial_forests,
        )
        self.state_index = 0  # Represents the number of days passed

    def initialize_grid(self, initial_temperature, initial_pollution, initial_water_mass, initial_cities, initial_forests):
        """
        Initialize the 3D grid with cells.
        """
        logging.debug("Initializing grid with size: %s", self.grid_size)

        x, y, z = self.grid_size
        grid = np.empty((x, y, z), dtype=object)

        city_count = forest_count = sea_count = iceberg_count = air_count = cloud_count = air_count = land_count = 0
        elevation_map = self._generate_elevation_map(self.grid_size)

        for i in range(x):
            for j in range(y):
                for k in range(z):
                    cell_type = 6  # Default to air
                    elev = elevation_map[i, j]

                    if k <= elev * 0.6:  # Below elevation: sea and ice
                        if np.random.random() < 0.8:
                            cell_type = 0  # Sea
                            sea_count += 1
                        else:
                            cell_type = 3  # Ice
                            iceberg_count += 1
                    elif k  == int(elev) :  # Land level
                        if forest_count < initial_forests and np.random.random() < 0.5:
                            cell_type = 4  # Forest
                            forest_count += 1
                        elif city_count < initial_cities:
                            cell_type = 5  # City
                            city_count += 1
                        else:
                            cell_type = 1  # Land
                            land_count+=1
                    elif k > int(elev) + 2 and np.random.random() < 0.1:  # Clouds
                        cell_type = 2
                        cloud_count += 1
                    else:
                        air_count+=1
                        cell_type = 6

                    # Initialize cell
                    grid[i, j, k] = Cell(
                        cell_type=cell_type,
                        temperature=initial_temperature + np.random.uniform(-2, 2),
                        water_mass=initial_water_mass if cell_type in [0, 3] else 0,
                        pollution_level=initial_pollution,
                        direction=(np.random.choice([-1, 1]), np.random.choice([-1, 1])) if cell_type in [0,2,3,6] else (0, 0),
                    )

        logging.info(
            "Grid initialized: %d cities, %d forests, %d land cells, %d sea cells, %d icebergs, %d air cells, %d clouds.",
            city_count, forest_count, land_count, sea_count, iceberg_count, air_count, cloud_count
        )

        return grid

    def _generate_elevation_map(self, grid_size):
        """
        Generate an elevation map using Perlin noise to simulate terrain elevation.
        :param grid_size: Tuple of (x, y, z) dimensions for the grid.
        :return: A 2D numpy array representing terrain elevation.
        """
        from noise import pnoise2
        x, y, z = grid_size
        elevation_map = np.zeros((x, y))

        # Scale factor for Perlin noise coordinates to create variability
        scale = 10.0
        octaves = 4
        persistence = 0.5
        lacunarity = 2.0

        for i in range(x):
            for j in range(y):
                # Generate Perlin noise and normalize it to fit the z-dimension
                noise_value = pnoise2(i / scale, j / scale, octaves=octaves,
                                      persistence=persistence, lacunarity=lacunarity, repeatx=x, repeaty=y)
                # Normalize to [0, z * 0.4]
                elevation_map[i, j] = (noise_value + 1) * (z * 0.4)

        return elevation_map

    def move_cells(self):
        """
        Move cells based on their direction property, handling Clouds, Air, Ice, and Water.
        """
        logging.debug("Moving cells for state index %d", self.state_index)

        x, y, z = self.grid_size
        new_grid = np.empty((x, y, z), dtype=object)

        # Initialize the new grid with empty cells (Air by default)
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    new_grid[i, j, k] = Cell(6)  # Default to Air

        # Move cells
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    current_cell = self.grid[i, j, k]

                    if current_cell.cell_type in [2, 6]:  # Clouds or Air
                        # Clouds and Air move freely in X-Y plane
                        new_i, new_j, new_k = current_cell.move((i, j, k), self.grid_size)
                    elif current_cell.cell_type == 3:  # Ice
                        # Ice moves if adjacent to water or under specific conditions
                        neighbors = self.get_neighbors(i, j, k)
                        if any(neighbor.cell_type == 0 for neighbor in neighbors):  # Adjacent to water
                            new_i, new_j, new_k = current_cell.move((i, j, k), self.grid_size)
                        else:
                            new_i, new_j, new_k = i, j, k  # No movement
                    elif current_cell.cell_type == 0:  # Water
                        # Water flows downhill if elevation map exists
                        neighbors = self.get_neighbors(i, j, k)
                        lowest_neighbor = min(neighbors, key=lambda n: n.elevation if hasattr(n, 'elevation') else float('inf'))
                        if hasattr(lowest_neighbor, 'elevation') and lowest_neighbor.elevation < current_cell.elevation:
                            new_i, new_j, new_k = lowest_neighbor.position
                        else:
                            new_i, new_j, new_k = current_cell.move((i, j, k), self.grid_size)
                    else:
                        # Other cells (Land, Forest, City) do not move
                        new_i, new_j, new_k = i, j, k

                    # Handle collisions and place the cell in the new position
                    if new_grid[new_i, new_j, new_k].cell_type == 6:  # Empty Air cell
                        new_grid[new_i, new_j, new_k] = current_cell
                    elif new_grid[new_i, new_j, new_k].cell_type in [2, 0]:  # Cloud or Water
                        # Merge properties for Cloud and Water
                        target_cell = new_grid[new_i, new_j, new_k]
                        target_cell.water_mass += current_cell.water_mass
                        target_cell.pollution_level = max(target_cell.pollution_level, current_cell.pollution_level)
                    else:
                        # If the target cell is not Air, Cloud, or Water, retain the original position
                        new_grid[i, j, k] = current_cell


        logging.debug("Completed moving cells.")


        self.grid = new_grid


    def resolve_collision(self, cell1, cell2):
        """
        Resolve a collision between two cells.
        Prioritize based on a predefined hierarchy: City > Forest > Cloud > Land > Sea > Ice > Air.
        """
        priority = {5: 6, 4: 5, 2: 4, 1: 3, 0: 2,
                    3: 1, 6: 0}  # Higher priority wins
        return cell1 if priority[cell1.cell_type] >= priority[cell2.cell_type] else cell2

    def update_cells(self):
        """
        Update each cell in the grid based on its interactions with neighbors.
        """
        logging.debug("Updating cells for state index %d", self.state_index)

        x, y, z = self.grid_size

        for i in range(x):
            for j in range(y):
                for k in range(z):
                    current_cell = self.grid[i, j, k]

                    # Get neighbors of the current cell
                    neighbors = self.get_neighbors(i, j, k)
                    current_position = (i, j, k)
                    current_cell.update(neighbors, current_position, self.grid_size)

        logging.debug("Completed updating cells.")

    def get_neighbors(self, i, j, k):
        """
        Get the neighbors of a cell at position (i, j, k).
        :param i: X-coordinate.
        :param j: Y-coordinate.
        :param k: Z-coordinate.
        :return: A list of neighboring Cell objects.
        """
        neighbors = []
        x, y, z = self.grid_size
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                    ni, nj, nk = (i + dx) % x, (j + dy) % y, (k + dz) % z
                    neighbors.append(self.grid[ni, nj, nk])
        return neighbors
        return neighbors

    def next_state(self):
        logging.info("Calculating next state from state index %d", self.state_index)

        """
        Calculate the next state of the grid (simulate one day).
        :return: A new State object representing the next state.
        """
        # Step 1: Move cells based on their direction
        self.move_cells()

        # Step 2: Update each cell based on interactions with neighbors
        self.update_cells()

        # Step 3: Derive global state attributes (temperature, pollution, water mass) from the current grid
        total_temperature = 0
        total_pollution = 0
        total_water_mass = 0
        total_cells = 0
        total_cities = 0
        total_forests = 0

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                for k in range(self.grid_size[2]):
                    cell = self.grid[i, j, k]
                    if cell.cell_type != 6:  # Exclude air cells
                        total_cities+=1
                        total_forests+=1
                        total_temperature += cell.temperature
                        total_pollution += cell.pollution_level
                        total_water_mass += cell.water_mass
                        total_cells += 1

        avg_temperature = total_temperature / total_cells if total_cells > 0 else 0
        avg_pollution = total_pollution / total_cells if total_cells > 0 else 0
        avg_water_mass = total_water_mass / total_cells if total_cells > 0 else 0

        # Step 4: Create a new state object and return it
        new_state = State(
            grid_size=self.grid_size,
            initial_temperature=avg_temperature,
            initial_pollution=avg_pollution,
            initial_water_mass=avg_water_mass,
            initial_cities=total_cities,
            initial_forests=total_forests
        )
        # Copy the updated grid to the new state
        new_state.grid = np.copy(self.grid)
        new_state.state_index = self.state_index + 1
        logging.info("Next state calculated: state index %d", self.state_index + 1)
        
        return new_state

    def visualize(self):
        """
        Visualize the 3D grid using matplotlib.
        """
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x, y, z = self.grid_size
        colors = {
            0: 'blue',  # Sea
            1: 'yellow',  # Land
            2: 'gray',  # Cloud
            3: 'cyan',  # Ice
            4: 'green',  # Forest
            5: 'purple',  # City
            6: 'white'  # Air
        }

        for i in range(x):
            for j in range(y):
                for k in range(z):
                    cell = self.grid[i, j, k]
                    color = colors.get(cell.cell_type, 'black')
                    ax.scatter(i, j, k, color=color)

        plt.title(f"State at Day {self.state_index}")
        plt.show()

