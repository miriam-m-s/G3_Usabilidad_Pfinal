import cv2

class VideoPlayer:

    def __init__(self, path):
        self.video = cv2.VideoCapture(path)

        if not self.video.isOpened():
            print("Error al abrir el archivo de vídeo")
            return
        
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.nFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.dt = 1 / self.video.get(cv2.CAP_PROP_FPS)
        self.duration = self.dt * self.nFrames

        self.frames = []
        for _ in range(self.nFrames):         
            self.frames.append(self.video.read()[1])
        self.frames.append(None)

        print(f'Duración del video: {self.duration}')
        print(f'FPS: {int(self.video.get(cv2.CAP_PROP_FPS))}')
        print(f'Frames totales {self.nFrames}')

    def getFrame(self, time):
        return self.frames[min(int(time / self.dt),  self.nFrames)]
