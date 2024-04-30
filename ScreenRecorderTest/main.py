import pyautogui
import cv2
import numpy as np
import time
from PIL import Image, ImageDraw

# Tamaño de la pantalla
screen_width, screen_height = pyautogui.size()

# Duración de la grabación en segundos
duration = 10

frames = []
mouse_info = []

# Bucle de grabación
start_time = time.time()
while (time.time() - start_time) < duration:
    frames.append(pyautogui.screenshot())
    mouse_info.append(pyautogui.position())

fps = len(frames) / duration
print(f'fps: {fps}')
print(f'Total Frames: {len(frames)}')

# Configurar el codec de video y el objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para H.264 en MP4
out = cv2.VideoWriter('video.mp4', fourcc, fps, (screen_width, screen_height))

radius = 30

for frame, pos in zip (frames, mouse_info):
    x, y = pos
    draw = ImageDraw.Draw(frame)    
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="blue", width=5)   
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    out.write(frame)

# Liberar el objeto VideoWriter y cerrar la ventana
out.release()
cv2.destroyAllWindows()
