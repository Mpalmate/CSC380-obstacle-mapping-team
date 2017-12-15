# This file is used to establish a connection and send a file to another rover.
# The other rover must run networking_client after this file is run to work properly.

import socket                   # Import socket module
import os
import gopigo

s = socket.socket()             # Create a socket object
host = 'kat.local'              # Get local machine name, can change for machine running file
port = 12345                    # Reserve a port for your service
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Wait for client connection

while True:
    conn, addr = s.accept()                    # Establish a connection with the client
    print 'Got connection from', addr 
    data = conn.recv(1024)
    print ('Server received', repr(data))   # Confirm a connection was successful

    f = open('file_name_here', 'rb')  # Open the file you want to send
    l = f.read(1024)
    while(l):
        conn.send(l)                           # Send the file
        print('Sent ', repr('l'))           # Confirm the desired file was sent
        l = f.read(1024)
    f.close()

    print('Done sending')
    conn.close()
s.close()
