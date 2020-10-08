from kano_wand.kano_wand import Shop, Wand, PATTERN
import moosegesture as mg
import paho.mqtt.client as mqtt
import json
import time
import random
import math

class GestureWand(Wand):
    time = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gestures = {
            ("UR", "DR"): "lumos",
            ("U", "R", "D", "R"): "lumos",
            ("DL", "UL"): "nox",
            ("D", "L", "U", "L"): "nox",
            ("DR", "DL"): "engorgio",
            ("R", "D", "L", "D"): "engorgio",
            ("UL", "UR"): "reducto",
            ("L", "U", "R", "U"): "reducto"
        }

        self.spell = None
        self.pressed = False
        self.positions = []
    
    def post_connect(self):
        self.subscribe_button()
        self.subscribe_position()

    def on_position(self, x, y, pitch, roll):
        ms = round(time.time_ns() / 1000000)
        # print(f"x:{x},y:{y},p:{pitch},r:{roll},ms:{ms}")
        if self.pressed:
            self.positions.append(tuple([x, -1 * y]))
    
    def on_button(self, pressed):
        # print(f"button:{pressed}")
        self.pressed = pressed

        if pressed:
            self.spell = None
            self.time = time.time_ns()
            self.positions = []
        else:
            # If releasing the button, get the gesture
            norm = self.min_max_normalize(self.positions)
            # print(norm)
            ms = round((time.time_ns() - self.time) / 1000)
            print(ms)
            gesture = mg.getGesture(norm)
            closest = mg.findClosestMatchingGesture(gesture, self.gestures, maxDifference=1)

            if closest != None:
                # Just use the first gesture in the list using the gesture key
                self.spell = self.gestures[closest[0]]
                self.vibrate(PATTERN.SHORT)
            # Print out the gesture
            print(f"{gesture}: {self.spell}")
    
    def min_max_normalize(self, tuple_array):
        x = [i[0] for i in tuple_array]
        y = [i[1] for i in tuple_array]
        minx = min(x)
        miny = min(y)
        return [(x - minx, y - miny) for (x,y) in tuple_array]

class Light():
    power = None
    dimmer = None
    color = None
    ct = None

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    # client.subscribe("$SYS/#")

devices = set()

def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")
    split = msg.topic.split("/")
    if split[0] == "homeassistant" and split[1] == "light":
        strpayload = str(msg.payload).replace("\\","")
        config = json.loads(strpayload[strpayload.index("b'")+2:-1])
        
        light = Light()
        light.power = config["cmd_t"]
        light.dimmer = config["bri_cmd_t"]
        light.color = config["rgb_cmd_t"]
        light.ct = config["clr_temp_cmd_t"]
        
        devices.add(light)
        # print(light)

def publish_all(client, cmnd, payload):
    for device in list(devices):
        client.publish(getattr(device, cmnd), payload)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("homeassistant/#")
    client.subscribe("stat/#")
    client.loop_start()

    shop = Shop(wand_class=GestureWand)
    wands = []

    try:
        while len(wands) == 0:
            print("Scanning...")
            wands = shop.scan(connect=True)
        
        wand = wands[0]
        while wand.connected:
            sleep = random.uniform(0.1, 0.2)
            if wand.spell is "lumos":
                publish_all(client, "power", "On")
            elif wand.spell is "nox":
                publish_all(client, "power", "Off")
            elif wand.spell is "engorgio":
                publish_all(client, "dimmer", "+")
            elif wand.spell is "reducto":
                publish_all(client, "dimmer", "-")
            wand.spell = None
            time.sleep(sleep)

    except KeyboardInterrupt as e:
        for wand in wands:
            wand.disconnect()
        client.loop_stop()

main()