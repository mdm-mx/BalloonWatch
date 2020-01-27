import aprslib  # https://aprs-python.readthedocs.io/en/stable/examples.html
import logging
import boto3

logging.basicConfig(level=logging.WARNING)
sqs_client = boto3.client('sqs')
server_ipaddress = ""
def callback(packet):
    #message = aprslib.parse(packet)
    global sqs_client
    global server_ipaddress
    response = sqs_client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/682422205370/aprsBalloon',
        DelaySeconds=10,
        MessageBody=(
            str(packet)
        )
    )
    if str(AIS.sock.getpeername()[0]) != server_ipaddress:
        logging.warning("Connected to APRS-IS Server at http://" + str(AIS.sock.getpeername()[0]) + ":14501/")
    server_ipaddress = str(AIS.sock.getpeername()[0])
    print("Receive from " + server_ipaddress + ", Sqs Enqueue: " + response['MessageId'] + " " + str(packet))

# Check client connection status at http://rotate.aprs.net:14501/
AIS = aprslib.IS("KI5GVH", passwd="23460", host="rotate.aprs.net", port=14580, skip_login=False)
AIS.filter = "s/O"  # http://www.aprs-is.net/javAPRSFilter.aspx  
AIS.connect(blocking=False)
print(("Connected to APRS-IS Server at http://" + str(AIS.sock.getpeername()[0]) + ":14501/"))
AIS.consumer(callback, raw=True, blocking=True, immortal=True)


