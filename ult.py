import time
import wiringpi
HIGH = 1
LOW = 0
INPUT = 0
OUTPUT =1
IN1_PIN = 1
IN2_PIN = 4
IN3_PIN = 5
IN4_PIN = 6

MAX_SPEED   = 50
AVG_SPEED   = 30
MIN_SPEED   = 0

GO_VALUE    = (AVG_SPEED, MIN_SPEED, AVG_SPEED, MIN_SPEED, 'GO')
STOP_VALUE  = (MIN_SPEED, MIN_SPEED, MIN_SPEED, MIN_SPEED, 'STOP')
UTURN_VALUE = (AVG_SPEED, MIN_SPEED, MIN_SPEED, AVG_SPEED, 'UTURN')

trig = 28
echo = 29

def controlMotor(value):
    wiringpi.softPwmWrite(IN1_PIN, value[0])
    wiringpi.softPwmWrite(IN2_PIN, value[1])
    wiringpi.softPwmWrite(IN3_PIN, value[2])
    wiringpi.softPwmWrite(IN4_PIN, value[3])
    print('control - %s\n' % value[4])
    wiringpi.delay(30)
def initultra():
    wiringpi.pinMode(trig, OUTPUT)
    wiringpi.pinMode(echo, INPUT)
def initMotor():
    wiringpi.pinMode(IN1_PIN, OUTPUT)
    wiringpi.pinMode(IN2_PIN, OUTPUT)
    wiringpi.pinMode(IN3_PIN, OUTPUT)
    wiringpi.pinMode(IN4_PIN, OUTPUT)
    
    wiringpi.softPwmCreate(IN1_PIN, MIN_SPEED, MAX_SPEED)
    wiringpi.softPwmCreate(IN2_PIN, MIN_SPEED, MAX_SPEED)
    wiringpi.softPwmCreate(IN3_PIN, MIN_SPEED, MAX_SPEED)
    wiringpi.softPwmCreate(IN4_PIN, MIN_SPEED, MAX_SPEED)
    
    wiringpi.delay(1000)
if __name__ == '__main__':
    try:
        wiringpi.wiringPiSetup()
        initMotor()
        initultra()
        while True:
            wiringpi.digitalWrite(trig, False)
            time.sleep(0.5)
            wiringpi.digitalWrite(trig, True)
            time.sleep(0.00001)
            wiringpi.digitalWrite(trig, False)

            while wiringpi.digitalRead(echo) == 0:
                pulse_start = time.time()
	
            while wiringpi.digitalRead(echo) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)

            print("distance : ", distance, "cm")
            if distance <= 30:	
                controlMotor(UTURN_VALUE)
                wiringpi.delay(100)
            else:
                controlMotor(GO_VALUE)
                wiringpi.delay(100)

    except KeyboardInterrupt:
        controlMotor(STOP_VALUE)
        print("stop")
