#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as db
import sys
import smtplib

#Assign GPIO pins
redPin = 27
greenPin = 26
tempPin = 17
#buttonPin = 19

#SMTP Variables
eFROM = "freenas.gillin@gmail.com"
eTO = "6312751202@vtext.com"
Subject = "Temperature Alert"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

#Temp and Humidity Sensor
tempSensor = Adafruit_DHT.DHT11
#LED Variables--------------------------------------------------------
#Duration of each Blink
blinkDur = .1
#Number of times to Blink the LED
blinkTime = 7
#---------------------------------------------------------------------
#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
#GPIO.setup(buttonPin, GPIO.IN)

#Alert Threshold
low=70
high=80

def inRange(inRange):
	GPIO.output(redPin, not inRange)
	GPIO.output(greenPin, inRange)

def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def connectDB():
	try:
		con=db.connect('log/tempLog.db')
	except db.Error as e:
		print("Error %s:" % e.args[0])
#	finally:
#		if con:
#			con.close()
	return con

def readFHum(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor,tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}'.format(temperature)
		hum = '{0:0.1f}'.format(humidity)
	else:
		print('Error Reading Sensor')
	return tempFahr,hum

def sendAlarm(t):
	print('wee woo wee woo')
	eMessage = 'Subject: {}\n\n{}'.format(Subject, "The temperature in the room is "+t+"*F!")
	server.login("freenas.gillin@gmail.com", "ptzxeaqwmvelffas")
	server.sendmail(eFROM, eTO, eMessage)
	server.quit


try:
	with open("./log/tempLog.csv", "a") as log:
		start=time.time()
		con=connectDB()
		cur=con.cursor()
		while True:
#			input_state = GPIO.input(buttonPin)
			if True:
#				for i in range (blinkTime):
#					oneBlink(redPin)
				time.sleep(.2)
				temp,hum = readFHum(tempPin)
#				hum = readHum(tempPin)
				query='INSERT INTO tempHum (Time, Temperature, Humidity) VALUES (\"'+time.strftime("%Y-%m-%d %H:%M:%S")+'\", \"'+str(temp)+'\", \"'+str(hum)+'%\");'
#				print(query)
				cur.execute(query)
				con.commit()
				if low <= float(temp) <= high:
					inRange(True)
				else:
					inRange(False)
					sendAlarm(temp)
				print("Temperature: ",str(temp),"*F Humidity: ",str(hum)+"%")
				#log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp),str(hum)))
				#log.flush()
				#os.fsync(log)

				#adjusts to make it actually 60 seconds
				time.sleep(60-((time.time() - start) % 60))

except KeyboardInterrupt:
	os.system('clear')
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()
	con.close()
