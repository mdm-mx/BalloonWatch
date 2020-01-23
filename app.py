# https://aprs-python.readthedocs.io/en/stable/examples.html
import aprslib
import time
import json
def callback(packet):
    message = aprslib.parse(packet)
    formattedMessage = "{}, {}, {}, {}, {}m heading {} at {}mph :{}"
    latitude = "?"
    longitude = "?"
    altitude = "?"
    timestamp = "?"
    speed = "?"
    course = "?"
    comment = "?"
    if 'latitude' in message and 'longitude' in message:
        latitude = round(message['latitude'], 4)
        longitude = round(message['longitude'], 4)
    if 'speed' in message:
        speed = round(message['speed'], 0)
    if 'course' in message:
        speed = message['course']
    if 'comment' in message:
        speed = message['comment']                
    if 'altitude' in message:
        speed = round(message['altitude'],0)
    if 'timestamp' in message:
        speed = round(message['timestamp'],0)        
    print (formattedMessage.format(timestamp, message['from'], latitude, longitude, altitude, course, speed, comment)) 
    print(message)

AIS = aprslib.IS("KI5GVH", host="rotate.aprs.net", port=14580, skip_login=False)
AIS.filter = "s/O"  # http://www.aprs-is.net/javAPRSFilter.aspx

AIS.connect(blocking=False)
print("Connected to APRS-IS.")
AIS.consumer(callback, raw=True, blocking=True)
print("APRS consumer linked.")
time.sleep(15)
print("Terminating APRS-IS Session.")
#AIS.disconnect
# by default `raw` is False, then each line is ran through aprslib.parse()
#while (True):
#    time.sleep(1)

