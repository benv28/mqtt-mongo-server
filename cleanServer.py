'''
DEPLOYMENT:
    pip install paho-mqtt

'''
MONGO_HOST = "localhost"
MONGO_PORT = 27017
TOPIC = "baseTopic/sub1"
MOSQUITTO_HOST = "localhost"
MOSQUITTO_PORT = 1883
import pymongo
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import datetime

'''
class log(Document):
    content = StringField(required=True)
     = StringField(required=True, max_length=50)
    published = DateTimeField(default=datetime.datetime.now)
'''
#BEGIN INIT - MONGO
mongo = MongoClient(MONGO_HOST, MONGO_PORT)
#declare which db to use
db = mongo.testbed_db
#declare which collections to use
posts = db.posts
logs = db.logs


#BEGIN INIT - MQTT

# callback for when the client receives a CONNACK response from broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    logs.insert_one({'status' : 'CONNECTED'})

    #on connection, subscribe to the topic and add custom callback
    mqtt.subscribe(TOPIC)
    mqtt.message_callback_add(TOPIC, BasicMongoStore)

# custom callback for receiving data on TOPIC - stores to mongoDB
def BasicMongoStore(client, userdata, msg):
    print("from topic "+ TOPIC + ": " + str(msg.payload, "utf-8"))
    try:
        jsonMSG = json.loads(str(msg.payload, "utf-8"))
        result = posts.insert_one(jsonMSG)
        print("Inserted post {0} to DB".format(result.inserted_id))
        # note that the mongoDB default objectid incorporates timestamping for each inserted object
    except ValueError:
        print("Error: incoming data is not in valid JSON format")
        event = {'data':  str(msg.payload, "utf-8") ,  'error' : 'INVALID_JSON'}
        
        logs.insert_one(event)

#default callback - if something goes wrong
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload, "utf-8"))

mqtt = mqtt.Client("server1")
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect(MOSQUITTO_HOST, MOSQUITTO_PORT, 60)

# Begin listening
mqtt.loop_forever()
while(True):
    2 + 2

# never reached (to change)
mqtt.loop_stop()
