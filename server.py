#!/usr/bin/env python3
import asyncore
import socket

class Player:
	def __init__(self, socket, ID):
		self.socket= socket
		self.ID= ID	

class EchoHandler(asyncore.dispatcher_with_send):

	def handle_read(self):
		data = self.recv(1024)
		data = str(data).strip()
		print("accept from clint")
		print('message is '+data)
		if 'HELO' in data:
			piece= data.split(' ')
			player= Player(self ,piece[1])
			players.append(player)
		elif 'FUCKYOU' in data:
			for each in players:
				if each.socket is not self:
					each.socket.send(data.encode('utf-8'))
class EchoServer(asyncore.dispatcher):

	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

	def handle_accepted(self, sock, addr):
		handler = EchoHandler(sock)

if __name__== "__main__":
	players=[]
	server = EchoServer('0.0.0.0', 9999)
	asyncore.loop()
