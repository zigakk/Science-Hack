# coding: utf-8

import RPi.GPIO as IO          # calling header file which helps us use GPIO’s of PI

import time                             # calling time to provide delays in program

IO.setwarnings(False)            #do not show any warnings

x=50                                      #integer for storing the duty cycle value

IO.setmode (IO.BCM)           #we are programming the GPIO by BCM pin numbers. (PIN35 as‘GPIO19’)

IO.setup(13,IO.OUT)         # initialize GPIO13 as an output.
IO.setup(19,IO.IN)             # initialize GPIO19 as an input.
IO.setup(26,IO.IN)             # initialize GPIO26 as an input.

p = IO.PWM(13,100)        #GPIO13 as PWM output, with 100Hz frequency
p.start(100)                            #generate PWM signal with 0% duty cycle

while 1:                             #execute loop forever
    print("We are in for a while!")

    p.ChangeDutyCycle(100)                 #change duty cycle for changing the brightness of LED.
    if(IO.input(26) == False):           #if button1 is pressed
        print("Right button press")
        if(x<50):
            x=x+1                                 #increment x by one if x<50
            time.sleep(0.2)                   #sleep for 200ms

    if(IO.input(19) == False):         #if button2 is pressed
        print("Left button press")
        if(x>0):
            x=x-1                                #decrement x by one if x>0
            time.sleep(0.2)                 #sleep for 200ms
