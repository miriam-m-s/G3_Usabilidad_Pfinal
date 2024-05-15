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


        for f in range(self.nFrames, -1, -1):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, f)
            ret, self.lastFrame = self.video.read()
            if ret: break

        print(ret)

        print(f'Duración del video: {self.duration}')
        print(f'FPS: {int(self.video.get(cv2.CAP_PROP_FPS))}')
        print(f'Frames totales {self.nFrames}')

    def getFrame(self, time):
        self.currentFrame = int(time / self.dt) 
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.currentFrame)
        ret, frame = self.video.read()  
        if not ret: 
            frame = self.lastFrame
            self.currentFrame = self.nFrames - 1
        return ret, frame
