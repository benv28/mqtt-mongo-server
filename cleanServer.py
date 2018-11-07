'''
DEPLOYMENT:
    pip install paho-mqtt
    pip install pymongo
    python3 cleanServer.py

    **make sure mongoDB is installed with the mongo daemon running 
        - see website for platform specific installation
Ubuntu Istallation:
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
14.04:
    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
16.04:
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
18.04:
    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

sudo apt-get update

sudo apt-get install -y mongodb-org

to start mongodb:  sudo service mongod start
to stop: sudo service mongod stop
to restart: sudo service mongod restart

mongo shell: mongo

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
