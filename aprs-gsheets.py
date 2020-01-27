# https://aprs-python.readthedocs.io/en/stable/examples.html
import aprslib
import time
import json
import pygsheets
import traceback
import logging

logging.basicConfig(level=logging.DEBUG) # level=10

# Settings
WatchedCalls = ["KI5GVH-12","KI5GVH-11"]
MyCall = "KI5GVH"
gc = pygsheets.authorize(service_file='google.json')
sh = gc.open('MDM-6-Track')
wks = sh[0]

lastTimeStamp = 0
lastAltitude = 0
#PacketFilter = "b/KI5GVH-12"    # http://www.aprs-is.net/javAPRSFilter.aspx
PacketFilter = "s/O"  # http://www.aprs-is.net/javAPRSFilter.aspx

def callback(packet):
    global wks
    global lastAltitude
    global lastTimeStamp

    message = aprslib.parse(packet)
    formattedMessage = "{}, {}, {}, {}, {}m heading {} at {}mph :{}"
    fromCall = message['from']
    latitude = ""
    longitude = ""
    altitude = ""
    timestamp = time.time()  # default 
    speed = ""
    course = ""
    comment = ""
    if 'latitude' in message and 'longitude' in message:
        latitude = round(message['latitude'], 4)
        longitude = round(message['longitude'], 4)
    if 'speed' in message:
        speed = round(message['speed'], 0)
    if 'course' in message:
        course = message['course']
    if 'comment' in message:
        comment = message['comment']                
    if 'altitude' in message:
        altitude = round(message['altitude'],0)
    if 'timestamp' in message:
        timestamp = round(message['timestamp'],0)
    timeDelta = 0
    altDelta = 0 
    verticalSpeed = 0
    try:
        timeDelta = timestamp - lastTimeStamp
        altDelta = altitude - lastAltitude
        verticalSpeed = 0 
        if timeDelta > 0 :
            verticalSpeed = round(altDelta / timeDelta, 2)
    except:
        print("ignored: " + str(packet))

    #print(timestamp, fromCall, latitude,longitude,altitude,speed,course,comment)
    print (formattedMessage.format(timestamp, fromCall, latitude, longitude, altitude, course, speed, comment)) 
    #print(message)
    if fromCall in WatchedCalls:
        wks.insert_rows(wks.rows, values=[timestamp,fromCall,latitude,longitude,altitude,speed,course,verticalSpeed,comment], inherit=True)
        lastTimeStamp = timestamp
        lastAltitude = altitude

# Check client connection status at http://rotate.aprs.net:14501/
AIS = aprslib.IS(MyCall, host="rotate.aprs.net", port=14580, skip_login=False)
AIS.filter = PacketFilter  

AIS.connect(blocking=False)
print("Connected to APRS-IS.")
AIS.consumer(callback, raw=True, blocking=True, immortal=True)
