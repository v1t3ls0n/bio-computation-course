import numpy as np
import logging


class Cell:
    def __init__(self, cell_type, temperature=0.0, water_mass=0.0, pollution_level=0.0, direction=(0, 0)):
        # 0: Sea, 1: Land, 2: Cloud, 3: Ice, 4: Forest, 5: City, 6: Air
        self.cell_type = cell_type
        # Automatically assign phase based on cell type
        self.temperature = temperature
        self.water_mass = water_mass
        self.pollution_level = pollution_level
        self.direction = direction  # Represents (dx, dy)

    def update(self, neighbors, current_position=None, grid_size=None):

        # General updates for all cell types
        self._adjust_temperature_with_pollution()

        # Delegate specific updates based on cell type
        if self.cell_type == 0:  # Sea
            self._update_sea(neighbors)
        elif self.cell_type == 1:  # Land
            # self._update_land(neighbors)
            return
        elif self.cell_type == 2:  # Cloud
            self._update_cloud(neighbors, current_position, grid_size)
        elif self.cell_type == 3:  # Ice
            self._update_ice(neighbors)
        elif self.cell_type == 4:  # Forest
            self._update_forest(neighbors)
        elif self.cell_type == 5:  # City
            self._update_city(neighbors)
        elif self.cell_type == 6:  # Air
            self._update_air(neighbors)

    def _adjust_temperature_with_pollution(self):
        """
        Adjust the cell's temperature based on its pollution level.
        A higher pollution level increases the temperature, with diminishing returns at high levels.
        """
        pollution_effect = self.pollution_level * \
            0.05  # Adjust the scaling factor as needed
        max_effect = 10  # Cap the effect at a certain maximum

        # Increase temperature proportionally to pollution
        self.temperature += min(pollution_effect, max_effect)

        # Simulate cooling if pollution level is low
        if self.pollution_level < 10:
            self.temperature = max(0, self.temperature - 0.1)  # Cooling effect

    def convert_to_city(self):
        """
        Change the cell type from forest to city.
        """
        if self.cell_type == 4:  # Ensure the current cell is a forest
            self.cell_type = 5  # Change to city
            self.pollution_level = 10  # Initial pollution level for a city
            self.water_mass = 0  # Cities don't retain water mass
            self.temperature += 2  # Cities may raise the local temperature slightly

    def convert_to_land(self):
        """
        Change the cell type to land.
        """
        if self.cell_type in [4, 5]:  # Ensure the cell is a forest or city
            self.cell_type = 1  # Change to land
            self.pollution_level = 0  # Reset pollution level for land
            self.water_mass = 0  # Land does not retain water mass
            # Slightly decrease temperature as vegetation or urban heat effect disappears
            self.temperature -= 1

    def _update_forest(self, neighbors):
        """
        Update logic for forests. Forests absorb pollution and may undergo deforestation.
        """
        # Absorb pollution from the forest itself
        self.pollution_level = max(
            0, self.pollution_level - 0.02 * self.pollution_level)
        cooling_effect = min(0.1, self.pollution_level * 0.02)
        self.temperature -= cooling_effect
        

        for neighbor in neighbors:
            # Absorb pollution from neighboring cells
            if neighbor.pollution_level > 0:
                # Forest can absorb up to 0.1 pollution
                absorbed_pollution = min(0.1, neighbor.pollution_level * 0.1)
                neighbor.pollution_level -= absorbed_pollution
                self.pollution_level = max(
                    0, self.pollution_level - absorbed_pollution)

            # Increase water mass from rainfall (clouds)
            if neighbor.cell_type == 2 and neighbor.water_mass > 0:  # Cloud neighbor
                rain = min(0.1, neighbor.water_mass)
                self.water_mass += rain
                neighbor.water_mass -= rain

        # Deforestation due to nearby city or high pollution
        if (self.pollution_level > 80 and self.temperature > 50) and np.random.uniform(0,1) < 0.2:
                    self.convert_to_land()
                    return
        # Orbanization
        if self.pollution_level == 0 and self.temperature <= 25 and np.random.uniform(0,1) < 0.2:
                    self.convert_to_city()
                    return



    def _update_land(self, neighbors):
        
        """
        Update logic for land cells:
        - Forests turn to land if temperature or pollution is high.
        - Land can turn into a forest if pollution is low and temperature is suitable.
        - Land surrounded by sea and with significant rainfall may turn into sea.
        """
        # Check if the land should turn into sea
        surrounding_sea_count = sum(
            1 for neighbor in neighbors if neighbor.cell_type == 0)
        # High water mass and surrounded by sea
        if surrounding_sea_count > len(neighbors) * 0.6 and self.water_mass > 1.0:
            self.cell_type = 0  # Land turns into sea
            self.water_mass = 1.0  # Normalize water mass for sea
            self.pollution_level = 0  # Sea has no pollution
            return

        # Check if the land should turn into a forest
        if self.pollution_level == 0 and self.temperature < 25:  # Low pollution and suitable temperature
            recovery_chance = 0.4
            if np.random.uniform(0,1)  < recovery_chance:
                self.cell_type = 4  # Land turns into forest
                self.pollution_level = 0  # Reset pollution
                return


    def _update_city(self, neighbors):
        """
        Update logic for cities. Cities generate pollution and can collapse.
        """
        # Generate pollution
        self.pollution_level += 0.2 * self.pollution_level
        self.temperature += 0.2 * self.temperature  # Cities are heat sources

        for neighbor in neighbors:
            # Spread pollution to neighboring cells
            pollution_spread = 0.1 * self.pollution_level
            neighbor.pollution_level = neighbor.pollution_level + pollution_spread

            # Cause deforestation in neighboring forests
            # Forest
            if neighbor.cell_type == 4 and (neighbor.pollution_level > 50 and neighbor.temperature > 50) and np.random.random() < 0.02:
                neighbor.cell_type = 1  # Forest turns into land

    def _update_ice(self, neighbors):
        """
        Update the behavior of ice cells.
        Ice cells melt or freeze depending on temperature.
        """
        if self.temperature > 0:
            self.cell_type = 0  # Melt to sea
            self.water_mass += 1

        for neighbor in neighbors:
            if neighbor.cell_type == 0 and neighbor.temperature < 0.0:  # Freeze sea to ice
                neighbor.cell_type = 3
                neighbor.water_mass = 0

            # Spread coldness to neighbors
            neighbor.temperature -= 0.1

    def _update_sea(self, neighbors):
        """
        Update the behavior of sea cells.
        Sea cells interact with clouds, temperature, and neighboring ice.
        """
        evaporation_rate = max(0.01, 0.02 * (self.temperature - 15))
        self.water_mass = max(0, self.water_mass - evaporation_rate)
        # Spread water currents

        for neighbor in neighbors:
            # Update temperature through diffusion
            temp_diffusion = (self.temperature - neighbor.temperature) * 0.2
            neighbor.temperature += temp_diffusion
            self.temperature -= temp_diffusion / len(neighbors)

            if neighbor.cell_type == 2:  # Cloud
                neighbor.water_mass += evaporation_rate / 2

            if neighbor.cell_type == 0:  # Another sea cell
                water_diffusion = (self.water_mass - neighbor.water_mass) * 0.1
                neighbor.water_mass += water_diffusion
                self.water_mass -= water_diffusion

            # Freezing and temperature diffusion
            if self.temperature < -2.0 and self.water_mass > 0:
                self.cell_type = 3  # Freeze to ice
                self.water_mass = 0

    def _update_air(self, neighbors):
        for neighbor in neighbors:
            if neighbor.cell_type == 2 or neighbor.cell_type == 6:  # Cloud
                neighbor.direction = self.direction  # Air influences Cloud direction
        for neighbor in neighbors:
            neighbor.temperature += 0.4 * \
                (self.temperature - neighbor.temperature)
            neighbor.pollution_level += 0.5 * \
                (self.pollution_level - neighbor.pollution_level)

    def _update_cloud(self, neighbors, current_position, grid_size):
        """
        Update logic for clouds, including movement, rain, and pollution spread.
        """
        # Move the cloud
        self.move(current_position, grid_size)

        # Rain logic
        if self.water_mass > 0:
            for neighbor in neighbors:
                if neighbor.cell_type in [0, 1, 4]:  # Sea, Land, or Forest
                    rain = min(0.1, self.water_mass)
                    neighbor.water_mass += rain
                    self.water_mass -= rain

        # Spread pollution to neighbors
        for neighbor in neighbors:
            if neighbor.cell_type in [1, 4, 5]:  # Land, Forest, or City
                pollution_spread = 0.05 * self.pollution_level
                neighbor.pollution_level = min(
                    100, neighbor.pollution_level + pollution_spread)

    def move(self, current_position, grid_size):
        """
        Calculate the next position of the cell based on its direction.
        :param current_position: Tuple of (x, y, z) indicating the current position of the cell.
        :param grid_size: Tuple of (x, y, z) indicating the grid size.
        :return: Tuple of (new_x, new_y, new_z) for the next position.
        """
        if self.cell_type in [2, 6, 0, 3]:  # Cloud, Air, Water, Ice
            x, y, z = current_position
            dx, dy = self.direction
            new_x = (x + dx) % grid_size[0]
            new_y = (y + dy) % grid_size[1]
            return new_x, new_y, z  # Movement in the X-Y plane
        return current_position  # Other cells do not move

    def get_color(self):
        """Get the color of the cell."""

        # if self.cell_type == 6: # Air (Transparent)
        #     return None

        base_colors = {
            0: (0.0, 0.0, 1.0, 1.0),  # Sea (blue)
            1: (1.0, 0.84, 0.0, 1.0),  # Land (gold)
            2: (0.5, 0.5, 0.5, 1.0),  # Cloud (gray)
            3: (0.0, 1.0, 1.0, 1.0),  # Ice (cyan)
            4: (0.0, 0.5, 0.0, 1.0),  # Forest (green)
            5: (1.0, 0.0, 0.0, 1.0),  # City (Red)
            6: (1.0, 1.0, 1.0, 0.01),  # Air (White)

        }

        base_color = base_colors[self.cell_type]
        # Tint towards black based on pollution level
        pollution_intensity = min(1.0, self.pollution_level / 100.0)
        black_tinted_color = tuple(
            base_color[i] * (1.0 - pollution_intensity) for i in range(4)
        )

        return black_tinted_color
