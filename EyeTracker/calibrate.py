from enum import Enum


import numpy as np


# SUP IZQ (0, 0) = 

# INF IZQ (0, y) = 

# CENTRO (x/2, y/2) =

# SUP DCHA (x, 0) = 

# INF DCHA (x, y) =


class CalibrationOutput(Enum):

    CALIBRATION_COMPLETED = 0
    STILL_CALIBRATING = 1
    CORNER_COMPLETED = 2

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

    def reset(self):
        self.collected_data = []
        self.current_iteration = 0
        print("Reset")

    def collect_data(self, left_pupil_coords, right_pupil_coords) :

        # TRUCO PARA SABER SI LAS COORDENADAS DE MIRADA SON VÁLIDAS:
        # Como la primera calibración es respecto al centro, una vez completada esta, podemos saber si el usuario está
        # mirando a al esquina que corresponda comparándolo con las coordenadas del centro. Ej: Si es esquina sup. der.
        # las coordenadas serán menores en eje x e y, si no, podemos asumir que está mirando a otro lado y no guardarlas
        # esto se puede hacer mandando como parámetro de entrada una función de validación desde el Manager, que compruebe
        # bajo que casos podemos aceptar datos, por ejemplo.

        mean_x = (left_pupil_coords[0] + right_pupil_coords[0]) / 2
        mean_y = (left_pupil_coords[1] + right_pupil_coords[1]) / 2

        self.collected_data.append((mean_x, mean_y))


        self.current_iteration += 1

        return (self.current_iteration < self.data_to_collect)


    def process_data(self, position) :

        array_np = np.array(self.collected_data)

        mean_x = np.mean(array_np[:, 0])

        mean_y = np.mean(array_np[:, 1])

        self.reset()
        
        return (mean_x, mean_y)



class CalibratorManager :

    # Posición de cada esquina 0-1
    corner_relative_positions = {
                        ScreenPositions.CENTER        : (0.5, 0.5),
                        ScreenPositions.TOP_LEFT      : (0,0),
                        ScreenPositions.TOP_RIGHT     : (1,0),
                        ScreenPositions.BOTTOM_RIGHT  : (1,1),
                        ScreenPositions.BOTTOM_LEFT   : (0,1)
                        }

    calibration_map = {
                        ScreenPositions.CENTER : (0,0),
                        ScreenPositions.TOP_LEFT : (0,0),
                        ScreenPositions.TOP_RIGHT : (0,0),
                        ScreenPositions.BOTTOM_RIGHT : (0,0),
                        ScreenPositions.BOTTOM_LEFT : (0,0)
                    }

    calibrator = None

    current_calibration = 0

    positions = [ScreenPositions.CENTER, ScreenPositions.TOP_LEFT, ScreenPositions.TOP_RIGHT, ScreenPositions.BOTTOM_RIGHT, ScreenPositions.BOTTOM_LEFT]


    def __init__(self):
        self.calibrator = Calibrator()

    def reset(self):
        self.current_calibration = 0
        self.calibration_map = {
                        ScreenPositions.CENTER : (0,0),
                        ScreenPositions.TOP_LEFT : (0,0),
                        ScreenPositions.TOP_RIGHT : (0,0),
                        ScreenPositions.BOTTOM_RIGHT : (0,0),
                        ScreenPositions.BOTTOM_LEFT : (0,0)
                        }
        self.calibrator.reset()

    def calibrate_update(self, left_pupil_coords, right_pupil_coords) :


        # Esperar a que indique que ya está mirando hacia esta posición

        # if not usuario_mira_a_current_calibration :

            # Si no le ha dado al espacio (o cualquier otro control)

            # mostrar_mensaje_pulsa_espacio(esta_posicion)
        

        # else :

            # Mostrar mensaje de la pantalla para siga mirando a la posición

            # y el resto del código ...
        

        if (self.current_calibration >= len(self.positions)) : 
            return CalibrationOutput.CALIBRATION_COMPLETED # Calibración completada
            # Mostrar mensaje de calibración terminada

        if not self.calibrator.collect_data(left_pupil_coords, right_pupil_coords) :
            # Calibración completada para esta posición
            screen_position = self.positions[self.current_calibration]
            self.calibration_map[screen_position] = self.calibrator.process_data(screen_position)
            self.current_calibration += 1
            return CalibrationOutput.CORNER_COMPLETED
            # Cambiar mensaje de la pantalla para que mire a la siguiente posición
            # mostrar_mensaje_pulsa_espacio(siguiente_posicion)

        return CalibrationOutput.STILL_CALIBRATING # Sigue calibrando
    
    def getTopLeft(self):
        return self.calibration_map[ScreenPositions.TOP_LEFT]
    
    def getTopRight(self):
        return self.calibration_map[ScreenPositions.TOP_RIGHT]
    
    def getBottomLeft(self):
        return self.calibration_map[ScreenPositions.BOTTOM_LEFT]
    
    def getBottomRight(self):
        return self.calibration_map[ScreenPositions.BOTTOM_RIGHT]
    
    def getCenter(self):
        return self.calibration_map[ScreenPositions.CENTER] 
    
    def get_calibration_map(self):
        return self.calibration_map.copy()  
    
    def get_current_relative_corner(self):
        currentScreenCorner = ScreenPositions(self.positions[self.current_calibration])
        return self.corner_relative_positions[currentScreenCorner]
    
    def get_corner_calibration_order_position(self):
        return [self.corner_relative_positions[ScreenPositions(position)] for position in self.positions]
    
