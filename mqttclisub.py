import pymongo
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
'''
COMMAND FOR mosquitto_pub:
    mosquitto_pub -h localhost -t baseTopic/sub1 -m '{ "name": "testcol", "val":"testval" }'
'''

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mqtt.subscribe("baseTopic/sub1")
    mqtt.subscribe("baseTopic/sub2")


    mqtt.message_callback_add("baseTopic/sub1", sub1)
    mqtt.message_callback_add("baseTopic/sub2", sub2)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload, "utf-8"))

# custom callback for receiving data from baseTopic/sub1
def sub1(client, userdata, msg):
    print("from topic sub1: " + str(msg.payload, "utf-8"))
    print(str(client))

    json_msg = json.loads(str(msg.payload, "utf-8"))
    result = posts.insert_one(json_msg)
    print('One post: {0}'.format(result.inserted_id))

def sub2(client, userdata, msg):
    print("from topic sub2: " + str(msg.payload, "utf-8"))

# initialize the mongo DataBase
mongo = MongoClient('localhost', 27017)
# connect to test_db
# if test_db doesn't exist, this also creates it.
db = mongo.test_db
# define which collection we will use:
posts = db.posts


mqtt = mqtt.Client()
mqtt.on_connect = on_connect
mqtt.on_message = on_message

mqtt.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt.loop_start()
while(True):
    if(input(':')):
        res = posts.find({'hat':'stat'})

        for item in res:
            print(item)
