## Blink Temperature Logger
This code detects when the sensor is pressed and if it is, the light blinks and the current temperature reading of the sensor is outputted and logged to a CSV file.

Prerequisites:

 - python3 RPi GPiO Library
 - python3-pip
 - Adafruit Python DHT Library

This script assumes that you have the touch sensor connected to pin 19, the temperature/Humidity reader to pin 17, and the LED to pin 27 on the GPiO interface.
