import socket
import re
import time

# def getdata():
#     s.listen(5)                 # Now wait for client connection.
#     while True:
#        c, addr = s.accept()     # Establish connection with client.
#        data = c.recv(4096)
#        c.close()                # Close the connection
#        break
#     return data

def premik(s, h):
    x = h / 2.5

    if s >= 0:
        x2 = x
        x1 = x * (1 - abs(s) / 90)
    elif s < 0:
        x1 = x
        x2 = x * (1 - abs(s) / 90)
    
    GPIO.setwarnings(False)

    motor_levo = 19 #Pin motorja 1
    motor_desno = 6 #Pin motorja 2

    #GPIO initialize
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Motor1,GPIO.OUT)
    GPIO.setup(Motor2,GPIO.OUT)

    p1 = GPIO.PWM(motor_desno,100)
    p2 = GPIO.PWM(motor_levo,100)

    p1.start(0)
    p2.start(0)

    p1.ChangeDutyCycle(x1)
    p2.ChangeDutyCycle(x2)

    time.sleep(2)

    p1.stop()
    p2.stop()

    GPIO.cleanup()


s = socket.socket()         # Create a socket object
host = '' # socket.gethostname() # Get local machine name
port = 12346
s.bind((host, port))        # Bind to the port

s.listen(5)
c, addr = s.accept()
smer = ''
hitrost = ''
i_p = 0

while True:
    ukaz = c.recv(4098).decode("utf-8")
    print(ukaz)
    temp_array = re.findall("[-+]?\d*\.\d+|\d+", ukaz)
    smer = float(temp_array[0])
    hitrost = float(temp_array[1])
    # print("Smer:", smer)
    # print("Hitrost:", hitrost)
    premik(smer, hitrost)
    time.sleep(1)

c.close()
