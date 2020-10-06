# rpi-kano-bneta
Raspberry Pi OS service to control [BNeta GU10 RGBW](https://www.builders.co.za/Fasteners-Fixtures-%26-Security/Security/Electronic-Security/Bneta-GU10-Smart-Multi-Wifi-LED-Bulb-%286W%29/p/000000000000705676) light bulbs with a [Kano Harry Potter Wand](https://kano.me/us/store/products/coding-wand).

# Setup

1. Flash light bulb with Tasmota firmware using [tuya-convert](https://github.com/ct-Open-Source/tuya-convert).
   - I played it safe, and only flashed one at first.
   - Once flashed, you can check the information page on the tasmota configuration site hosted at the device's IP address, and see if it has enough space to load the latest firmware version. If it has, you can do a OTA update.
2. Get a [Tasmota template](https://templates.blakadder.com/bulb.html) for your light bulb.
   - The [BNeta GU10 RGBW template](https://templates.blakadder.com/bneta_IO-WIFI-GU10S.html) on the site didn't work for my light bulb, and the pictures didn't look the same. I saw a picture of a light bulb that looked almost exactly the same, tried its' template, and all the functionality worked as expected.
3. [Setup Home Assistant on the Raspberry Pi](https://www.home-assistant.io/docs/installation/raspberry-pi/).
   - [Setup Home Assistant to run after boot](https://community.home-assistant.io/t/autostart-using-systemd/199497)
4. Install mosquitto by running `sudo apt-get install mosquitto` in a terminal.