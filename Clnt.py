import socket
import time

host = 'localhost'
port = 9999
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send("HELO elqwer\n")
while 1:
	s.send('FUCKYOU client message2')
	print(str(s.recv(1024)))
	time.sleep(0.5)
s.close()
