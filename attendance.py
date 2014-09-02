#!/home/darshil/MyApp/env/bin/python
from app import app, db, mail
from app.models import User, Logs
from time import sleep
import os
import RPi.GPIO as GPIO
from subprocess import *
import datetime
strpath = "/home/darshil/"
strfile = "webcam"
IRPin=17
LEDRed=22
LEDGrn=23
global flagProx
flagProx=False
debug = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(IRPin, GPIO.IN)
GPIO.setup(LEDRed, GPIO.OUT)
GPIO.setup(LEDGrn, GPIO.OUT)
GPIO.output(LEDGrn, GPIO.LOW);
GPIO.output(LEDRed, GPIO.LOW);

def run_cmd(cmd):
   p = Popen(cmd, shell=True, stdout=PIPE)
   output = p.communicate()[0]
   return output

def capture():
   GPIO.output(LEDRed, GPIO.LOW)
   os.system("sudo fswebcam --device /dev/video0 --input 0 --resolution 352x288 --save "+
               strpath+strfile+".jpg --skip 2")
   GPIO.output(LEDRed, GPIO.HIGH)

def scan():
   scanned=''
   count=0
   global flagProx
   while scanned=='' and flagProx:
      count = count + 1
      capture()
      scanned=run_cmd("zbarimg "+strpath+strfile+".jpg")
      GPIO.output(LEDRed, GPIO.HIGH);
      if count == 10:
         flagProx=False

   flagProx=False
   user_obj = db.session.query(User).filter_by(qr_data = scanned[8:-1]).all()
   if scanned!='':
          GPIO.output(LEDGrn, GPIO.HIGH);
          GPIO.output(LEDRed, GPIO.LOW);
          sleep(8)
          if debug == True:
             print "Scanned hash %s User ID %s" % (scanned, user_obj[0].get_id())
          return user_obj[0].get_id()

def blinkRED():
   GPIO.output(LEDGrn, GPIO.LOW)
   GPIO.output(LEDRed, GPIO.HIGH)
   sleep(0.2)
   GPIO.output(LEDRed, GPIO.LOW)
   sleep(0.8)

if __name__ == "__main__":
   while True:
      if (GPIO.input(IRPin)):
         global flagProx
         flagProx=True
         userid=scan()
         logger = Logs()
         logger.user_id = userid
         logger.timestamp = datetime.datetime.now()
         db.session.add(logger)
         db.session.commit()
         # Here goes something to add for Front-end
      else:
         blinkRED() # When nothing is there blink red LED with some predefined period
