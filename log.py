import RPi.GPIO as GPIO
import os
import time
import sqlite3 as db
import sys
import smtplib

GPIO.setmode(GPIO.BCM)

#SMTP Variables
eFROM = "freenas.gillin@gmail.com"
Subject = "Alarm condition detected!"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

#time in seconds between two email alerts sent out
alarmdelay = 60



alarmPin = 4
lastalarm = 0

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq7_dpin = 26
mq7_apin = 0

#
flamePin = 5
smokePin = 21
combustGasPin = 13


GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system


GPIO.setup(alarmPin, GPIO.OUT)
GPIO.output(alarmPin, GPIO.HIGH)

def connectDB():
	try:
		con=db.connect('log/log.db')
	except db.Error as e:
		print("Error %s:" % e.args[0])
#	finally:
#		if con:
#			con.close()
	return con
	

def action(pin):
	if(pin == flamePin):
		print("Flame Detected!")
	elif (pin == smokePin):
		print('Smoke detected!')
	elif (pin == combustGasPin):
		print("Combustible gas detected!")
	else:
		print("unknown detected")
		
	activeAlarm()
	
	return
	

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(mq7_dpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(flamePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(smokePin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(combustGasPin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(flamePin, GPIO.RISING)
GPIO.add_event_callback(flamePin, action)

GPIO.add_event_detect(smokePin, GPIO.RISING)
GPIO.add_event_callback(smokePin, action)

GPIO.add_event_detect(combustGasPin, GPIO.RISING)
GPIO.add_event_callback(combustGasPin, action)

def sendAlarm():
	print('wee woo wee woo')
	eMessage = 'Subject: {}\n\n{}'.format(Subject, "Alarm Condition!")
	server.login("freenas.gillin@gmail.com", "ptzxeaqwmvelffas")
	eTO = "6312751202@vtext.com"
	server.sendmail(eFROM, eTO, eMessage)
	server.quit

def activeAlarm():
	GPIO.output(alarmPin, GPIO.LOW)
	time.sleep(1)
	GPIO.output(alarmPin, GPIO.HIGH)
	global lastalarm
	if ((lastalarm+60)<time.time()):
		lastalarm=time.time()
		sendAlarm()


def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout



try:
	print("Calibrating..")
	time.sleep(20)
	start=time.time()
	con=connectDB()
	cur=con.cursor()
	while True:
			COlevel=readadc(mq7_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)

			if GPIO.input(mq7_dpin):
				print("Monitoring active")
				time.sleep(1)
			else:
				activeAlarm()
				print("CO is detected")
				print("Current CO AD vaule = " +str("%.2f"%((COlevel/1024.)*5))+" V")
				print("Current CO density is:" +str("%.2f"%((COlevel/1024.)*100))+" %")
				time.sleep(0.5)
			query='INSERT INTO log (time, density) VALUES (\"'+time.strftime("%Y-%m-%d %H:%M:%S")+'\", \"'+str("%.2f"%((COlevel/1024.)*100))+'\");'
			cur.execute(query)
			con.commit()
			
			
except KeyboardInterrupt:
	os.system("clear")
	GPIO.cleanup()
	con.close()