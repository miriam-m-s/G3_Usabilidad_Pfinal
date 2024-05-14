class EyeTrackingEvent:
    def __init__(self, timestamp,leftPupilX,leftPupilY,rightPupilX,rightPupilY):
        self.timestamp = timestamp
        
        self.leftPupilX=leftPupilX
        self.leftPupilY=leftPupilY
        
        self.rightPupilX=rightPupilX
        self.rightPupilY=rightPupilY
        
    def toJson(self):
        return f'{{\n "timestamp": {self.timestamp},\n "leftPupilX": {self.leftPupilX},\n "leftPupilY": {self.leftPupilY},\n "rightPupilX": {self.rightPupilX},\n "rightPupilY": {self.rightPupilY}\n}}'
    
    def setLeftPupilCoords(self,leftPupilX,leftPupilY):
        self.leftPupilX=leftPupilX
        self.leftPupilY=leftPupilY

    def setRightPupilCoords(self,rightPupilX,rightPupilY):
        self.rightPupilX=rightPupilX
        self.rightPupilY=rightPupilY
