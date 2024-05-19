import cv2

class VideoPlayer:

    def __init__(self, path):
        self.video = cv2.VideoCapture(path)

        if not self.video.isOpened():
            print("Error al abrir el archivo de vídeo")
            return
        
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        for frame in range(int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)), -1, -1):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, self.lastFrame = self.video.read()
            if ret: break

        self.nFrames = frame + 1
        self.dt = 1 / self.video.get(cv2.CAP_PROP_FPS)
        self.duration = self.dt * self.nFrames
        self.lastFrame = -1

        print(f'Duración del video: {self.duration}')
        print(f'FPS: {int(self.video.get(cv2.CAP_PROP_FPS))}')
        print(f'Frames totales {self.nFrames}')

    def getFrame(self, time):
        currentFrame = int(time / self.dt)
        if currentFrame != self.lastFrame and currentFrame < self.nFrames:         
            self.video.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)
            self.lastFrame = currentFrame
            return self.video.read()[1]      
        return None

    def get_frame_as_image(self, time):
        currentFrame = int(time / self.dt)
        if currentFrame < self.nFrames:   
            self.video.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)
            img = self.video.read()[1]      
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.lastFrame)
            return img
        return None
    
    def getFrameFromFrameIncrease(self, frameIncrease):
        currentFrame = max(0, min(self.lastFrame + frameIncrease, self.nFrames - 1))
        self.video.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)
        time = currentFrame * self.dt + self.dt / 10.0
        self.lastFrame = currentFrame
        return self.video.read()[1], time