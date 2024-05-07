from enum import Enum

import numpy as np

# SUP IZQ (0, 0) = 
# INF IZQ (0, y) = 
# CENTRO (x/2, y/2) =
# SUP DCHA (x, 0) = 
# INF DCHA (x, y) =

class ScreenPositions (Enum) :
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3
    CENTER = 4

class Calibrator :

    # Recogemos 20 datos por cada punto, y sacamos la media
    data_to_collect = 20

    collected_data = [] 
    current_iteration = 0

    def collect_data(self, left_pupil_coords, right_pupil_coords) :

        mean_x = (left_pupil_coords[0] + right_pupil_coords[0]) / 2
        mean_y = (left_pupil_coords[1] + right_pupil_coords[1]) / 2

        self.collected_data[self.current_iteration] = (mean_x, mean_y)

        self.current_iteration += 1

        return (self.current_iteration < self.data_to_collect)

    def process_data(self, position) :

        array_np = np.array(self.collected_data)

        mean_x = np.mean(array_np[:, 0])
        mean_y = np.mean(array_np[:, 1])

        

        self.collected_data = []
        self.current_iteration = 0

        return (mean_x, mean_y)


class CalibratorManager :

    calibration_map = {ScreenPositions.TOP_LEFT : (0,0),
                        ScreenPositions.TOP_RIGHT : (0,0),
                        ScreenPositions.BOTTOM_LEFT : (0,0),
                        ScreenPositions.BOTTOM_RIGHT : (0,0),
                        ScreenPositions.CENTER : (0,0)}

    calibrator = None
    current_calibration = 0
    positions = [ScreenPositions.TOP_LEFT, ScreenPositions.TOP_RIGHT, ScreenPositions.BOTTOM_LEFT, ScreenPositions.BOTTOM_RIGHT, ScreenPositions.CENTER]

    def __init__(self):
        self.calibrator = Calibrator()

    def calibrate_update(self, left_pupil_coords, right_pupil_coords) :
        
        if (self.current_calibration >= len(self.positions)) : 
            return True # Calibración completada

        if not self.calibrator.collect_data(left_pupil_coords, right_pupil_coords) :

            screen_position = self.positions[self.current_calibration]
            self.calibration_map[screen_position] = self.calibrator.process_data(screen_position)
            self.current_calibration += 1

        return False # Sigue calibrando