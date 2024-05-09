import json
import time
from jsonSerializer import JsonSerializer
from  eventSender import EventSender
from  eyeTrackingEvent import EyeTrackingEvent
from typing import List

# Ejemplo de uso:
serializer = JsonSerializer()
event_sender = EventSender(serializer, 5)  # Enviar eventos cada 5 segundos

# Generar algunos eventos de seguimiento ocular
event_sender.add_event(EyeTrackingEvent(timestamp=time.time(), x=100, y=200))
event_sender.add_event(EyeTrackingEvent(timestamp=time.time(), x=150, y=250))

# Iniciar el envío de eventos en segundo plano
event_sender.send_events()