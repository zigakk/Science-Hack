from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import re
import time
import socket               # Import socket module


angles = []
velocities = []

s = socket.socket()         # Create a socket object
host = "88.200.37.141"                   # Get local machine name
port = 12346                # Reserve a port for your service.
s.connect((host, port))
num_of_players = 0

class SimpleEcho(WebSocket):

    def __init__(self, *args):
        super().__init__(*args)
        self.num_of_players = 0

    def handleMessage(self):
        # echo message back to client
        inp = self.data
        inp = list(map(int, re.findall(r'(-?[\d]+)', inp)))
        print(inp)
        angles.append(inp[0])
        velocities.append(inp[1])

        print(self.data)
        self.sendMessage(self.data + " " + str(self.num_of_players))

    def handleConnected(self):
        self.num_of_players += 1
        print(self.address, 'connected')

    def handleClose(self):
        self.num_of_players -= 1
        print(self.address, 'closed')

# print("ziga connect")
server = SimpleWebSocketServer('', 12345, SimpleEcho)
start = time.time()
while True:
    server.serveonce()
    diff = time.time() - start
    if diff > 2 and angles:
        # print("sending to PI")
        avg_angle = sum(angles) / len(angles)
        avg_velocity = sum(velocities) / len(velocities)

        s.send("{} {}".format(avg_angle, avg_velocity).encode('utf-8'))

        angles = []
        velocities = []

        start = time.time()

s.close()                     # Close the socket when done

