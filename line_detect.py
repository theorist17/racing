import time
import wiringpi

HIGH   = 1
LOW    = 0
INPUT  = 0
OUTPUT = 1 

IN1_PIN = 1
IN2_PIN = 4
IN3_PIN = 5
IN4_PIN = 6

LEFT_TRACER_PIN  = 10
RIGHT_TRACER_PIN = 11

MAX_SPEED = 20 #20
AVG_SPEED = 15 #15
MIN_SPEED = 0

GO_VALUE    = (AVG_SPEED, MIN_SPEED, AVG_SPEED, MIN_SPEED, 'GO')
STOP_VALUE  = (MIN_SPEED, MIN_SPEED, MIN_SPEED, MIN_SPEED, 'STOP')
UTURN_VALUE = (AVG_SPEED, MIN_SPEED, MIN_SPEED, AVG_SPEED, 'UTURN')

trig = 28
echo = 29
uturn = 0 # making U-turn or not
exit = 0
enter = 0

def initMotor():
    wiringpi.pinMode(IN1_PIN, OUTPUT)
    wiringpi.pinMode(IN2_PIN, OUTPUT)
    wiringpi.pinMode(IN3_PIN, OUTPUT)
    wiringpi.pinMode(IN4_PIN, OUTPUT)

    wiringpi.softPwmCreate(IN1_PIN, MIN_SPEED, MAX_SPEED)
    wiringpi.softPwmCreate(IN2_PIN, MIN_SPEED, MAX_SPEED)
    wiringpi.softPwmCreate(IN3_PIN, MIN_SPEED, MAX_SPEED)
    wiringpi.softPwmCreate(IN4_PIN, MIN_SPEED, MAX_SPEED)

def initSensor():
    wiringpi.pinMode(LEFT_TRACER_PIN, INPUT)
    wiringpi.pinMode(RIGHT_TRACER_PIN, INPUT)            
    initMotor()
    wiringpi.delay(1000)

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

if __name__ == '__main__':
    try:
        wiringpi.wiringPiSetup()                          
        initSensor()
        initultra()
        while True:
            LValue = wiringpi.digitalRead(LEFT_TRACER_PIN)
            RValue = wiringpi.digitalRead(RIGHT_TRACER_PIN)
            
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

            #print("distance : ", distance, "cm")
            if distance <= 30:
                uturn = 1
            	
            if uturn == 1:
                if (LValue == LOW) and (RValue == HIGH):
                    exit = 1
                    print(" exit 1")
                if (LValue == LOW) and (RValue == LOW) and (exit == 1):
                    exit = 2
                    print(" exit 2")
                if (LValue == HIGH) and (RValue == LOW) and (exit == 2):
                    exit = 3
                    print(" exit 3")
                if (LValue == LOW) and (RValue == LOW) and (exit == 3):
                    exit = 0
                    print(" exit 0")
                    uturn = 0
                controlMotor(UTURN_VALUE)
                wiringpi.delay(1)
                continue
             
            print('LTracer - %d, RTracer - %d\n' % (LValue, RValue))
            if (LValue == HIGH) and (RValue == LOW):
                print(" left detect ")
                wiringpi.softPwmWrite(IN1_PIN, MIN_SPEED)
                wiringpi.softPwmWrite(IN2_PIN, AVG_SPEED)
                wiringpi.softPwmWrite(IN3_PIN, AVG_SPEED)
                wiringpi.softPwmWrite(IN4_PIN, MIN_SPEED)
                wiringpi.delay(15) #30
            elif (LValue == LOW) and (RValue == HIGH):
                print(" right detect ")
                wiringpi.softPwmWrite(IN1_PIN, AVG_SPEED)
                wiringpi.softPwmWrite(IN2_PIN, MIN_SPEED)
                wiringpi.softPwmWrite(IN3_PIN, MIN_SPEED)
                wiringpi.softPwmWrite(IN4_PIN, AVG_SPEED)
                wiringpi.delay(15)
            elif (LValue == LOW) and (RValue == LOW):
                wiringpi.softPwmWrite(IN1_PIN, AVG_SPEED)
                wiringpi.softPwmWrite(IN2_PIN, MIN_SPEED)
                wiringpi.softPwmWrite(IN3_PIN, AVG_SPEED)
                wiringpi.softPwmWrite(IN4_PIN, MIN_SPEED)
                print(" go!")
                wiringpi.delay(15)
            
                            

    except KeyboardInterrupt:
        wiringpi.softPwmWrite(IN1_PIN, MIN_SPEED)
        wiringpi.softPwmWrite(IN2_PIN, MIN_SPEED)
        wiringpi.softPwmWrite(IN3_PIN, MIN_SPEED)
        wiringpi.softPwmWrite(IN4_PIN, MIN_SPEED)
        print(" stop!")
