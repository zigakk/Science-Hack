import socket
import re
import time

def getdata():
    s.listen(5)                 # Now wait for client connection.
    while True:
       c, addr = s.accept()     # Establish connection with client.
       data = c.recv(4096)
       c.close()                # Close the connection
       break
    return data

s = socket.socket()         # Create a socket object
host = '' # socket.gethostname() # Get local machine name
port = 42666
s.bind((host, port))        # Bind to the port

smer = ''
hitrost = ''
i_p = 0

while True:
    ukaz = getdata().decode("utf-8")
    temp_array = re.findall("[-+]?\d*\.\d+|\d+", ukaz)
    smer = float(temp_array[0])
    hitrost = float(temp_array[1])
    # print("Smer:", smer)
    # print("Hitrost:", hitrost)
    premik(smer, hitrost)
    time.sleep(1)
