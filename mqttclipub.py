import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# custom callback for receiving data from baseTopic/sub1
def sub1(client, userdata, msg):
    print("from topic sub1: " + str(msg.payload))

def sub2(client, userdata, msg):
    print("from topic sub2: " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

while(True):
    invar = input('value to be published: ')
    client.publish("baseTopic/sub1", str(invar))
