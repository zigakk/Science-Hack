import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = 'localhost' # Get local machine name
port = 42666

s.connect((host, port))
s.send(b'-0.5001 0.666')
s.close                     # Close the socket when done
