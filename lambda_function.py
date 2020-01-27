import json
import aprslib  # https://aprs-python.readthedocs.io/en/stable/examples.html
import time

def lambda_handler(event, context):
    getAprsFeed()
    return {
        'statusCode': 200,
        'body': json.dumps('Ending Aprs Execution!')
    }

def callback(packet):
    #print(aprslib.parse(packet))
    print(packet)

def getAprsFeed():
    AIS = aprslib.IS("KI5GVH", host="rotate.aprs.net", port=14580, skip_login=False)
    AIS.filter = "s/O"  # balloon symbol only
    # IS.filter = "g/APLIG*"  # ToCall =  LightAPRS    # https://github.com/hessu/aprs-deviceid/blob/master/tocalls.yaml
    # IS.filter = "b/KI5GVH*/K6RPT*"  # From a list of calls

    AIS.connect(blocking=True)
    AIS.consumer(callback, raw=True)
    print("Connected.")
    time.sleep(15)
    AIS.close()
    #while (True):
    #    time.sleep(1)

