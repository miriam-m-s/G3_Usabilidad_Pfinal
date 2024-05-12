import json
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class dataAnalyzer:
    def createHeatMap(coords):
        # Extraer las coordenadas x e y de la lista
        x = [coord[0] for coord in coords]
        y = [coord[1] for coord in coords]

        # Crear un histograma 2D normalizado
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=50, density=True)

        # Plotear el mapa de calor
        plt.imshow(heatmap.T, origin='lower', extent=[min(x), max(x), min(y), max(y)], cmap='hot')
        plt.colorbar(label='Densidad')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Mapa de Calor')
        plt.show()
    
    # Cargar el JSON desde un archivo
    with open('prueba.json', 'r') as json_data:
        data = json.load(json_data)
    eyePosData = data["eye_positions"]
    
    initTime = eyePosData[0]['timestamp']

    startDataTime = 0
    endDataTime= len(eyePosData)

    #Avanzar hasta la primera marca de tiempo que se necesita
    for j in range(0, len(eyePosData)):
        if(eyePosData[j]['timestamp'] >= (initTime + startDataTime)):
            break

    print(j)
    print(eyePosData[j]['timestamp'])
    totalPositions= []
    for k in range(j,len(eyePosData)):
        if(eyePosData[k]['timestamp'] > (initTime + endDataTime)):
            break
        print
        totalPositions.append((eyePosData[k]['posX'], eyePosData[k]['posY']))
    createHeatMap(totalPositions)
    print(len(totalPositions))




