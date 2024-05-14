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
        self.currentFrame = 0

        self.frames = []
        for _ in range(self.nFrames):         
            self.frames.append(self.video.read()[1])
        self.frames.append(None)

        print(f'Duración del video: {self.duration}')
        print(f'FPS: {int(self.video.get(cv2.CAP_PROP_FPS))}')
        print(f'Frames totales {self.nFrames}')

    def getFrame(self, time):
        self.currentFrame = int(time / self.dt)      
        if self.currentFrame < self.nFrames:
            return True, self.frames[self.currentFrame]
        else:
            self.currentFrame = self.nFrames - 1
            return False, self.frames[self.currentFrame]
