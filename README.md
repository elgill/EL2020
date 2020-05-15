## Fire and Gas Detector
This project uses 4 sensors to detect dangerous situations, and  can sound an alarm and text the user if the scenario is detected.

**Supplies:**

 - Raspberry Pi 
 - Breadboard 
 - Jumper wires 
 - MQ-2 Gas Smoke Sensor Module
 - MQ-5 Combustible Gas Detector 
 - MQ-7 CO Carbon Monoxide Detector Sensor
 - Module Flame Detection Sensor Module Analog to Digital Converter
 - Buzzer Alarm Sensor Module

**Setup:**
![https://i.imgur.com/5AuBMjt.jpg](https://i.imgur.com/5AuBMjt.jpg)

For each sensor there is a vcc you can hook up to the 3.3v(yellow wires), and a ground(black wires). After that, we must connect the DO to the GPIO for each device.  Hook up the alarm to pin 4,  the flame detector to pin 5, the smoke pin to pin 21, the combustible gas pin to 13, and the carbon monoxide detector to pin 26. 
Then we will be hooking up the analog to digital converter. On the top line of connections, we will be connecting all of the pins to the GPIO. The first 2 go to the 3.3v, next the ground pin, then SPISCLK, then SPIMISO, then SPIMOSI, SPICE0, and finally another ground pin. The connect the bottom right to the AO of the carbon monoxide detector and we're done wiring it up.

Once you have that, you must go into the log folder, and type sqlite3. Type 

> CREATE TABLE log (time DATETIME, density DOUBLE);

 Then we must do 

> .save log.db

**Files**

The log.py is the script that runs the smoke detector, while flaskServer.py runs the web interface connected to it. 