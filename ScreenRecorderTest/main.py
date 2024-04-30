import pyautogui
import cv2
import numpy as np
import time

# Tamaño de la pantalla
screen_width, screen_height = pyautogui.size()

# Duración de la grabación en segundos
duration = 10

frames = []
nFrames = 0

# Bucle de grabación
start_time = time.time()
while (time.time() - start_time) < duration:
    # Captura de pantalla
    screenshot = pyautogui.screenshot()

    # Convertir la captura de pantalla a un formato compatible con OpenCV
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frames.append(frame)

    nFrames += 1

print(nFrames)

# Configurar el codec de video y el objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para H.264 en MP4
fps = nFrames / duration
print(fps)
out = cv2.VideoWriter('video.mp4', fourcc, fps, (screen_width, screen_height))

for frame in frames:
    out.write(frame)

# Liberar el objeto VideoWriter y cerrar la ventana
out.release()
cv2.destroyAllWindows()
