import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions
import time

global OPPONENT_SELECTION
OPPONENT_SELECTION = None

global player_id
player_id = input("Please input your player_id (1/2): ")

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  options = SubscribeOptions(noLocal=True)
  global player_id
  if player_id == "1":
    topic = "ece180d/rps/2"
  elif player_id == "2":
    topic = "ece180d/rps/1"
  client.subscribe(topic, options=options)


# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')


# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
  # print('Received message: "' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))
  global OPPONENT_SELECTION
  OPPONENT_SELECTION = str(message.payload)[2:-1]


# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

while True:
    time.sleep(1)
    USER_SELECTION = None
    while USER_SELECTION not in ["ROCK", "PAPER", "SCISSORS"]:
        USER_SELECTION = input("Select from ROCK, PAPER, SCISSORS ......")
        USER_SELECTION = USER_SELECTION.upper()

    client.publish("ece180d/rps/" + str(player_id), USER_SELECTION)

    while OPPONENT_SELECTION == None:
        print("Waitng for opponent...")
        time.sleep(1)

    print("Selected: " + USER_SELECTION)
    print("Opponent: " + OPPONENT_SELECTION)

    if USER_SELECTION == OPPONENT_SELECTION:
        print("TIE!")
    elif USER_SELECTION == "ROCK":
        if OPPONENT_SELECTION == "PAPER":
            print("YOU LOSE!")
        elif OPPONENT_SELECTION == "SCISSORS":
            print("YOU WIN!")
    elif USER_SELECTION == "PAPER":
        if OPPONENT_SELECTION == "SCISSORS":
            print("YOU LOSE!")
        elif OPPONENT_SELECTION == "ROCK":
            print("YOU WIN!")
    else:
        if OPPONENT_SELECTION == "ROCK":
            print("YOU LOSE!")
        elif OPPONENT_SELECTION == "PAPER":
            print("YOU WIN!")



# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()