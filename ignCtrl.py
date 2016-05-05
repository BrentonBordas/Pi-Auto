#--Used to shutdown PI via IO pins--#
#Todd Farr's awesome python project
#23022016
import RPi.GPIO as GPIO
import time
import os  # will need to shutdown
#import time
#sets the gpio pin to the "board" standard
GPIO.cleanup()  #####this is falsely used at the beggining of code###
#it only cleans up ports used in THIS program
# new at python i will use it as a precaution
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.IN)
GPIO.setup([12,40],GPIO.OUT)
#counter = 0
try:
	while GPIO.input(37):
		print "connected"
		GPIO.output(12, GPIO.HIGH)
	GPIO.output(12, GPIO.LOW)
	print "insead of printing send a shutdown code"
	GPIO.output(40, GPIO.HIGH)
	time.sleep(10) 
	GPIO.output(40, GPIO.LOW)
	os.system("sudo shutdown -r now")
#def my_callback_one(channel):
#    print('Callback one')
#
#def my_callback_two(channel):
#    print('Callback two')
#
#GPIO.add_event_detect(channel, GPIO.RISING)
#GPIO.add_event_callback(channel, my_callback_one)
#GPIO.add_event_callback(channel, my_callback_two)
except KeyboardInterrupt:
	#any code you want for keyboard exit ctrl c
	print "\n keyboard interrupt \n. \n.. \n ... \n ...."
#except:
	#catch all
#	print "Other error occured"
finally:
	GPIO.cleanup()
	print "end of code"
