import json
import time
from jsonSerializer import JsonSerializer
from  eventSender import EventSender
from  eyeTrackingEvent import EyeTrackingEvent
from typing import List

#Ejemplo de uso:
serializer = JsonSerializer()
eventSender = EventSender(serializer, 5,(10078940,20053400),(1018900,10132500),(10056680,1074500),(14440,5540))  # Enviar eventos cada 5 segundos

#Generar algunos eventos de seguimiento ocular
eventSender.add_event(EyeTrackingEvent(timestamp=time.time(), leftPupilX=100, leftPupilY=200,rightPupilX=600,rightPupilY=700))
eventSender.add_event(EyeTrackingEvent(timestamp=time.time(), leftPupilX=100, leftPupilY=0,rightPupilX=900,rightPupilY=200))



#Iniciar el envío de eventos en segundo plano
eventSender.sendEvents()