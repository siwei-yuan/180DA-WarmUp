import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions
import time
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_1,
    K_2,
    K_3,
    K_r,
    KEYDOWN,
    QUIT,
)
pygame.init()


font = pygame.font.Font('freesansbold.ttf', 32)


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
  print("OPPONENT SELECTED" + OPPONENT_SELECTION)


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
time.sleep(1)
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

running = True
USER_SELECTION = None
RESULT = None
SELECTED = False

screen = pygame.display.set_mode([600, 500])

while running:

    screen.fill((255, 255, 255))

    img = pygame.image.load("rps.jpg")
    img = pygame.transform.scale(img, (600, 200))
    rect = img.get_rect()
    screen.blit(img, rect)

    text = font.render('1.ROCK', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (100, 200)
    screen.blit(text, textRect)

    text = font.render('2.PAPER', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (300, 200)
    screen.blit(text, textRect)

    text = font.render('3.SCISSORS', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (500, 200)
    screen.blit(text, textRect)


    if not SELECTED:
        text = font.render('Press 1/2/3 to select...', True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (300, 350)
        screen.blit(text, textRect)
    else :
        text = font.render('You selected: ' + USER_SELECTION + "...", True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (300, 350)
        screen.blit(text, textRect)
    
 

    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_1 and not SELECTED:
                print("YOU SELECTED ROCK")
                USER_SELECTION = "ROCK"
            if event.key == K_2 and not SELECTED:
                print("YOU SELECTED PAPER")
                USER_SELECTION = "PAPER"
            if event.key == K_3 and not SELECTED:
                print("YOU SELECTED SCISSORS")
                USER_SELECTION = "SCISSORS"
            if event.key == K_r:
                USER_SELECTION = None
                RESULT = None
                SELECTED = False
                OPPONENT_SELECTION = None


    if USER_SELECTION == "ROCK":
        pygame.draw.circle(screen, (0, 0, 255), (100, 250), 10)
    elif USER_SELECTION == "PAPER":
        pygame.draw.circle(screen, (0, 255, 0), (300, 250), 10)
    elif USER_SELECTION == "SCISSORS":
        pygame.draw.circle(screen, (255, 0, 0), (500, 250), 10)

    if USER_SELECTION and not SELECTED:
        client.publish("ece180d/rps/" + str(player_id), USER_SELECTION)
        SELECTED = True
        

    
    if OPPONENT_SELECTION and SELECTED:
        text = font.render('Opponent selected: ' + OPPONENT_SELECTION, True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (300, 380)
        screen.blit(text, textRect)


    if USER_SELECTION == OPPONENT_SELECTION and USER_SELECTION != None and OPPONENT_SELECTION != None:
        RESULT = "TIE"
    elif USER_SELECTION == "ROCK":
        if OPPONENT_SELECTION == "PAPER":
            RESULT = "LOSE"
        elif OPPONENT_SELECTION == "SCISSORS":
            RESULT = "WIN"
    elif USER_SELECTION == "PAPER":
        if OPPONENT_SELECTION == "SCISSORS":
            RESULT = "LOSE"
        elif OPPONENT_SELECTION == "ROCK":
            RESULT = "WIN"
    elif USER_SELECTION == "SCISSORS":
        if OPPONENT_SELECTION == "ROCK":
            RESULT = "LOSE"
        elif OPPONENT_SELECTION == "PAPER":
            RESULT = "WIN"

    if RESULT == "WIN":
        text = font.render('YOU WIN', True, (255, 0, 0))
    elif RESULT == "LOSE":
        text = font.render('YOU LOSE', True, (255, 0, 0))
    elif RESULT == "TIE":
        text = font.render('TIE', True, (255, 0, 0))

    if RESULT != None:
        textRect = text.get_rect()
        textRect.center = (300, 300)
        screen.blit(text, textRect)


    pygame.display.update()


# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()