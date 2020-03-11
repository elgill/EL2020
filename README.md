## Temerature and Humidity Log
This code reads a temperature and humidity sensor once a minute, logs it in a sqlite database, the current temperature reading and humidity of the sensor is outputted, and it is compared against a threshold. If it is within the constraints, the green LED is lit, otherwise, the red LED is lit and a text message alert is sent containing the temperature.

Prerequisites:

 - python3 RPi GPiO Library
 - python3-pip
 - Adafruit Python DHT Library

This script assumes that you have the the temperature/Humidity reader connected to pin 17, the green LED to pin 26 and the red LED to pin 27 on the GPiO interface.
