import RPi.GPIO as GPIO
import time

def Forward (time_forward):
    GPIO.setwarnings(False)
    x=20
    Motor1 = 13 #Pin motorja 1
    Motor2 = 15 #Pin motorja 2
    
    #GPIO initialize
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Motor1,GPIO.OUT)
    GPIO.setup(Motor2,GPIO.OUT)
    
    p1 = GPIO.PWM(Motor1,100)
    p2 = GPIO.PWM(Motor2,100)
    
    p1.start(0)
    p2.start(0)

    p1.ChangeDutyCycle(x)
    p2.ChangeDutyCycle(x)

    time.sleep(time_forward)

    p1.stop()
    p2.stop()

    GPIO.cleanup()
    
def Turn (time_turn, direction):
    GPIO.setwarnings(False)
    x=20
    Motor1 = 13 #Pin motorja 1
    Motor2 = 15 #Pin motorja 2
    
    #GPIO initialize
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Motor1,GPIO.OUT)
    GPIO.setup(Motor2,GPIO.OUT)
    
    p1 = GPIO.PWM(Motor1,100)
    p2 = GPIO.PWM(Motor2,100)
    
    p1.start(0)
    p2.start(0)

    if (direction):
        p1.ChangeDutyCycle(x)
        p2.ChangeDutyCycle(-x)
    else:
        p1.ChangeDutyCycle(-x)
        p2.ChangeDutyCycle(x)

    time.sleep(time_turn)

    p1.stop()
    p2.stop()

    GPIO.cleanup()