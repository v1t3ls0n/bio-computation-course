import numpy as np
import logging

baseline_temperature = 15  # Assume a global baseline temperature
freezing_point = 0  # Temperature that cause water freeze and convert into ice
melting_point = 50  # Temperature threshold for melting ice
evaporation_point = 100  # Temperature threshold for melting ice
rain_threshold = 1.0
cloud_threshold = 1.0

class Cell:
    def __init__(self, cell_type=6, temperature=0, water_mass=0, pollution_level=0, direction=(0, 0, 0), elevation=None):

        self.cell_type = cell_type
        self.temperature = temperature
        self.water_mass = water_mass
        self.pollution_level = pollution_level
        self.direction = direction

    def clone(self):
        return Cell(
            cell_type=self.cell_type,
            temperature=self.temperature,
            water_mass=self.water_mass,
            pollution_level=self.pollution_level,
            direction=self.direction,
        )

    def update_state(self, neighbors , current_position, grid_size):
        """
        Compute the next state of the cell based on its neighbors and position.
        """
        
        self._apply_natural_decay()
        self.increase_cell_temperature_by_neighbors_avg(neighbors)
        self.increase_cell_pollution_by_neighbors_avg(neighbors)
        # self.adjust_temperature_with_pollution()

        # Call the appropriate update method based on cell type
        if self.cell_type == 0:  # Water
            self._update_water(neighbors)

        elif self.cell_type == 1:  # desert
            self._update_desert(neighbors)

        elif self.cell_type == 2:  # Cloud
            self._update_cloud(neighbors)

        elif self.cell_type == 3:  # Ice
            self._update_ice(neighbors)

        elif self.cell_type == 4:  # Forest
            self._update_forest(neighbors)

        elif self.cell_type == 5:  # City
            self._update_city(neighbors)

        elif self.cell_type == 6:  # Air
            self._update_air(neighbors)

        elif self.cell_type == 7: # Rain
            self._update_rain(neighbors)


        return self



####################################################################################################################
######################################  CELL'S SELF EFFECTS : ######################################################
####################################################################################################################

    def _apply_natural_decay(self):

        pollution_decay_rate = 0.1  # Rate at which pollution naturally decreases
        temperature_decay_rate = 0.1  # Rate at which temperature naturally decreases

        # Apply decay to pollution level
        self.pollution_level = max( 0, self.pollution_level - (self.pollution_level * pollution_decay_rate))

        # Apply decay to temperature, reducing towards a baseline temperature
        if self.temperature > baseline_temperature:
            self.temperature -= (self.temperature -
                                 baseline_temperature) * temperature_decay_rate
        elif self.temperature < baseline_temperature:
            self.temperature += (baseline_temperature -
                                 self.temperature) * temperature_decay_rate


    def adjust_temperature_with_pollution(self):

        pollution_effect = self.pollution_level * 0.1  # Increased scaling factor
        max_effect = 5  # Higher maximum effect to reflect significant pollution impact
        self.temperature += min(pollution_effect, max_effect)

        # Stronger effect for very high pollution levels
        if self.pollution_level > 50:
            extra_effect = (self.pollution_level - 50) * \
                0.2  # Additional temperature increase
            # Limit extra effect to 10 degrees
            self.temperature += min(extra_effect, 3)

        # Apply natural cooling if pollution is very low
        if self.pollution_level < 10:
            self.temperature = max(0, self.temperature - 0.2)

    def pollution_absorb(self):
        if self.cell_type == 4:
            pollution_absorption_rate = 0.2
            cooling_effect = 0.2
            self.pollution_level = max(
                0, self.pollution_level - pollution_absorption_rate * self.pollution_level)
            self.temperature = max(
                self.temperature - self.temperature * cooling_effect, baseline_temperature)
    
    def create_city_pollution(self):
        if self.cell_type == 5:
            pollution_increase_rate = 0.2
            warming_effect = 0.2
            self.pollution_level =  self.pollution_level + pollution_increase_rate * self.pollution_level
            self.temperature = self.temperature + self.temperature * warming_effect

####################################################################################################################
######################################  CELL's NEIGHBORS EFFECTS: ##################################################
####################################################################################################################

    def calc_neighbors_avg_temperature(self, neighbors):
        return (sum(neighbor.temperature for neighbor in neighbors)) / len(neighbors)

    def calc_neighbors_avg_pollution(self, neighbors):
        return (sum(neighbor.pollution_level for neighbor in neighbors)) / len(neighbors)
    
    def calc_neighbors_avg_water_mass(self, neighbors):
        return (sum(neighbor.water_mass for neighbor in neighbors)) / len(neighbors)
    
    def increase_cell_temperature_by_neighbors_avg(self, neighbors):
        nei_avg_temp = self.calc_neighbors_avg_temperature(neighbors)
        diff = self.temperature - (nei_avg_temp if nei_avg_temp > 0 else -nei_avg_temp) 
        self.temperature += diff

    def increase_cell_pollution_by_neighbors_avg(self, neighbors):
        nei_avg_pollution = self.calc_neighbors_avg_pollution(neighbors)
        if  nei_avg_pollution > self.pollution_level:
           self.pollution_level+= (nei_avg_pollution - self.pollution_level)
        else:
            self.pollution_level -= (nei_avg_pollution + self.pollution_level)

    
    def increase_water_mass_by_neighbors_avg(self, neighbors):
        nei_avg_water_mass= self.calc_neighbors_avg_water_mass(neighbors)
        if nei_avg_water_mass > self.water_mass:
            self.water_mass += (nei_avg_water_mass - self.water_mass)
        else:
            self.water_mass -= (nei_avg_water_mass - self.water_mass)


    def adjust_air_elevation_by_neighbors(self, neighbors):
        neighbors_avg_temp = self.calc_neighbors_avg_temperature(neighbors)
        if self.temperature > min(neighbors_avg_temp, melting_point, baseline_temperature):
            self.direction = (self.direction[0], self.direction[1], 1)
        elif self.temperature < max(freezing_point, neighbors_avg_temp):
            self.direction = (self.direction[0], self.direction[1], -1)
        else:
            self.direction = (self.direction[0], self.direction[1], 0)


    def is_surrounded_by_clouds(self, neighbors):
        return sum(1 for neighbor in neighbors if neighbor.cell_type == 2) >= 0.8 * len(neighbors)

    def is_surrounded_by_water_or_ice(self, neighbors):
        return sum(1 for neighbor in neighbors if neighbor.cell_type in {0, 3}) >= 0.8 * len(neighbors)




        

####################################################################################################################
###################################### CELL_TYPE UPDATES: ##########################################################
####################################################################################################################


    def _update_forest(self, neighbors):
        if self.is_surrounded_by_water_or_ice(neighbors):
            self.sink_to_ocean()
            return
        self.pollution_absorb()
        if self.temperature >= abs(evaporation_point) or self.pollution_level >= 100:
            self.convert_to_desert()

        elif self.pollution_level == 0 and 0 < self.temperature <= baseline_temperature:
            self.convert_to_city()

    def _update_desert(self, neighbors):
        if self.is_surrounded_by_water_or_ice(neighbors):
            self.sink_to_ocean()
        elif self.pollution_level == 0 and self.temperature <= baseline_temperature:
            self.convert_to_forest()

    def _update_city(self, neighbors):
        self.create_city_pollution()
        if self.is_surrounded_by_water_or_ice(neighbors):
            self.sink_to_ocean()
        elif self.pollution_level > 100 or abs(self.temperature) >= evaporation_point:
            self.convert_to_desert()

    def _update_ice(self, neighbors):
        if self.temperature > melting_point:
            self.convert_to_water()

    def _update_water(self, neighbors):
        if self.temperature <= freezing_point:
            self.convert_to_ice()
        elif self.temperature >= evaporation_point:
            self.convert_to_air()

    def _update_air(self, neighbors):    
        self.adjust_air_elevation_by_neighbors(neighbors)
        if self.water_mass >= 1.0 and self.is_surrounded_by_clouds(neighbors):
            self.convert_to_cloud()
                  
    def _update_rain(self, neighbors):
        for neighbor in neighbors:
            if neighbor.cell_type in {0, 1, 3, 4, 5, 6}:
                self.water_mass -= neighbor.water_mass
        self.water_mass = max(0,self.water_mass)
        if self.is_surrounded_by_water_or_ice():
            self.sink_to_ocean()
        elif self.water_mass == 0:
            self.convert_to_air()

    def _update_cloud(self, neighbors):
        # self.adjust_air_elevation_by_neighbors(neighbors)
        if self.is_surrounded_by_clouds(neighbors):
            self.convert_to_rain()
        




####################################################################################################################
###################################### CELL_TYPE CONVERSIONS ##########################################################
####################################################################################################################
    def sink_to_ocean(self):
        if self.temperature <= freezing_point:
            self.convert_to_ice()
        else:
            self.convert_to_water()

    def convert_to_city(self):
        self.cell_type = 5
        self.water_mass = 0
        self.direction = (0, 0, 0)

    def convert_to_desert(self):
        self.cell_type = 1
        self.water_mass = 0
        self.temperature -= self.temperature * 0.2
        self.direction = (0, 0, 0)

    def convert_to_water(self):
        self.cell_type = 0
        self.water_mass = 1.0
        self.direction = (self.direction[0], self.direction[1], 0)

    def convert_to_ice(self):
        self.cell_type = 3
        self.water_mass = 1.0
        self.direction = (self.direction[0], self.direction[1], 0)

    def convert_to_air(self):
        self.cell_type = 6
        self.direction = (self.direction[0], self.direction[1], 1)
        # self.water_mass = 0
        # self.adjust_air_elevation_by_neighbors(neighbors)
    
    def convert_to_rain(self):
        self.cell_type = 7
        self.direction = (0,0, -1)

    def convert_to_forest(self):
        self.cell_type = 4
        self.direction = (0, 0, 0)
        self.temperature = baseline_temperature
        self.pollution_level = 0
        self.water_mass = 0
    
    def convert_to_cloud(self):
        self.cell_type = 2
        self.direction = (self.direction[0], self.direction[1], 0)



####################################################################################################################
###################################### CELL UTILS FUNCTIONS: ##########################################################
####################################################################################################################
    
    def move(self, current_position, grid_size):

        if self.direction == (0, 0, 0):  # No movement for static cells
            return current_position

        x, y, z = current_position
        dx, dy, dz = self.direction
        new_z = z + dz

        if new_z <= 0:
            new_z = 0
        elif new_z >= grid_size[2]:
            new_z = grid_size[2] - 1

        new_x = (x + dx) % grid_size[0]
        new_y = (y + dy) % grid_size[1]

        return new_x, new_y, new_z

    def get_color(self):
        """Get the color of the cell."""
        base_colors = {
            6: (1.0, 1.0, 1.0, 0.01), # Air (transparent white)
            2: (0.5, 0.5, 0.5, 1.0),  # Cloud (gray)
            0: (0.0, 0.0, 1.0, 1.0),  # Water (blue)
            3: (0.4, 0.8, 1.0, 1.0),  # Ice (cyan)
            7: (0.2, 0.3, 0.5, 1.0),  # Rain (Dark Blue-Grey)
            1: (1.0, 1.0, 0.0, 1.0),  # Land (gold)
            4: (0.0, 0.5, 0.0, 1.0),  # Forest (green)
            5: (0.5, 0.0, 0.5, 1.0),  # City (purple)
        }

        # Get the base color for the cell type or default to transparent white
        base_color = base_colors.get(self.cell_type, (1.0, 1.0, 1.0, 0.01))

        # Ensure the base_color has exactly 4 components (RGBA)
        if len(base_color) != 4:
            logging.error(f"Invalid color definition for cell_type {
                          self.cell_type}: {base_color}")
            return None

        # Tint based on pollution level
        # Ensure within 0-1 range
        pollution_intensity = max(0.0, min(self.pollution_level / 100.0, 1.0))
        black_tinted_color = [
            max(0.0, min(base_color[i] * (1.0 - pollution_intensity), 1.0)) for i in range(3)]
        # Ensure alpha is also within 0-1 range
        alpha = max(0.0, min(base_color[3], 1.0))

        return (*black_tinted_color, alpha)
