# rpi-kano-bneta
Raspberry Pi OS service to control Tasmota RGBW flashed light bulbs with a [Kano Harry Potter Wand](https://kano.me/us/store/products/coding-wand) using Bluetooth and the MQTT protocol.

# Setup

1. (Optional) [Setup Home Assistant Core on the Raspberry Pi](https://www.home-assistant.io/docs/installation/raspberry-pi/).
   - [Setup Home Assistant Core to run after boot](https://community.home-assistant.io/t/autostart-using-systemd/199497).
2. Install Mosquitto
   - Run `sudo apt-get install mosquitto` in a terminal.
   - (Optional) Install the MQTT integration for Home Assistant Core and setup with Mosquitto broker.
3. Flash light bulb with Tasmota firmware using [tuya-convert](https://github.com/ct-Open-Source/tuya-convert).
   > I played it safe, and only flashed one at first.
   - Once flashed, you can check the information page on the site hosted at the device's IP address, and see if it has enough space to load the latest firmware version. If it has, do an OTA update.
   - Get a [Tasmota template](https://templates.blakadder.com/bulb.html) for your light bulb and paste it in the Template field at `http://%DEVICE_IP%/co?`.
     > The [BNeta GU10 RGBW template](https://templates.blakadder.com/bneta_IO-WIFI-GU10S.html) on the site didn't work for my [BNeta GU10 RGBW 6W](https://www.builders.co.za/Fasteners-Fixtures-%26-Security/Security/Electronic-Security/Bneta-GU10-Smart-Multi-Wifi-LED-Bulb-%286W%29/p/000000000000705676) light bulbs, the picture doesn't even look like the same model. I saw a picture of another light bulb that looked almost exactly the same as the ones I have, so I guessed it couldn't hurt to try [its' template](https://templates.blakadder.com/brilliantsmart_20888.html) before forcing it open to have a look at the GPIO connections. Thankfully all the functionality worked as expected.
   - Setup MQTT on the Tasmota flashed device
     - (Optional) Run Command `SetOption19 1` to enable Home Assistant Auto Discovery 