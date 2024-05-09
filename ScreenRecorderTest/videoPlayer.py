import cv2

class VideoPlayer:

    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)

        if not self.cap.isOpened():
            print("Error al abrir el archivo de vídeo")
        else:
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def getFrame(self):

        # Lee un fotograma del archivo de vídeo
        ret, frame = self.cap.read()

        # Verifica si se pudo leer el fotograma
        if not ret:
            print("Error al leer fotograma")

        return frame
