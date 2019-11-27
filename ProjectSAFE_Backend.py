import paho.mqtt.client as mqtt
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


Cred = credentials.Certificate("./ServiceAccountKey.json")
Default = firebase_admin.initialize_app(Cred)
db = firestore.client()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    global Connected
    Connected = True


def on_message_Lat(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    global Lat
    Lat = float(msg.payload)


def on_message_Lon(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    global Lon
    Lon = float(msg.payload)


def on_message_Dan(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    global Dan
    Dan = int(msg.payload)


def on_message_Sat(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    global Sat
    Sat = int(msg.payload)


def send_data_Firebase():
    print(Lat)
    print("Sending to Firestore...")
    doc_ref = db.collection(u'Wolf').document()
    doc_ref.set({
        u'Lat': Lat,
        u'Lon': Lon,
        u'Date': i
    })
    print("Sended...")


Connected = False
global i
i = 0


Broker_Server = "m16.cloudmqtt.com"
User = "qfvclmgw"
Password = "jkmvpBfiQJQL"
Port = 11126


client = mqtt.Client("AlphaWolf")
client.username_pw_set(User, password=Password)
client.on_connect = on_connect
# client.on_message = on_message
client.connect(Broker_Server, port=Port)


client.loop_start()


while Connected is not True:
    time.sleep(0.1)


client.subscribe("Wolf/Lat")
client.subscribe("Wolf/Lon")
client.subscribe("Wolf/Dan")
client.subscribe("Wolf/Sat")
client.message_callback_add("Wolf/Lat", on_message_Lat)
client.message_callback_add("Wolf/Lon", on_message_Lon)
client.message_callback_add("Wolf/Dan", on_message_Dan)
client.message_callback_add("Wolf/Sat", on_message_Sat)
send_data_Firebase()


while True:
    time.sleep(1)
