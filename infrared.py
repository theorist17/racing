import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
irpin = 16
led1pin = 21 
led2pin = 12

GPIO.setup(irpin, GPIO.IN)
GPIO.setup(led1pin, GPIO.OUT)
GPIO.setup(led2pin, GPIO.OUT)

GPIO.output(led1pin, GPIO.LOW)
GPIO.output(led2pin, GPIO.LOW)

try:
	while True:
		x = GPIO.input(irpin)
		print(x)
		time.sleep(0.1)
		if x != 1:
			GPIO.output(led1pin, GPIO.HIGH)
			GPIO.output(led2pin, GPIO.LOW)
		else:
			GPIO.output(led1pin, GPIO.LOW)
			GPIO.output(led2pin, GPIO.HIGH)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()

