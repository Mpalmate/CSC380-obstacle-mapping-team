import socket

s = socket.socket()
host = 'kat.local'
port = 12345

s.connect((host, port))
s.send("Hello, server!")

with open('file_name_here', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        f.write(data)

f.close()
print('Successfully got the file')
s.close()
print('Connection closed')
