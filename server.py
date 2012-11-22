#!/usr/bin/env python3
import asyncore
import socket
import sqlite3
class gamedb:
	def __init__(self, name = 'lcdb'):
		self.conn = sqlite3.connect(name)
		c = self.conn.cursor()
		try:
			c.execute('create table game (data text)')
		except sqlite3.OperationalError:
			print('Table already exist.')

	def add(self, data):
		c = self.conn.cursor()
		c.execute('insert into game values (?)',(data,))
		self.conn.commit()
		c.close

class Player:
	def __init__(self, socket, ID):
		self.socket = socket
		self.ID = ID
		self.ready = 0

class EchoHandler(asyncore.dispatcher_with_send):
	def handle_read(self):
		data = self.recv(1024)
		data = data.decode().strip();
		print('accept from clint')
		print('message is '+data)
		splited = data.split()
		header = splited[0]
		if len(splited) > 1:
			body = data[len(header):]
			db.add(body) #TODO: Use db for specific data.
		if 'HELO' == header:
			players.append(Player(self, body))
		elif 'MGHG' == header:
			for each in players:
				if each.socket is not self:
					msg = data+' '+str(each.ID)
					each.socket.sendall(msg.encode())
		elif 'READY' == header:
			for each in players:
				if each.socket is self:
					print('set ready '+each.ID)
					each.ready = 1
			allready = 1
			for each in players:
				print(each.ID+' is '+str(each.ready))
				allready *= each.ready
			if allready is 1:
				print('all clients are ready')
				for each in players:
					print('send start message')
					startmsg = 'START'.encode()
					each.socket.sendall(startmsg.strip())
		else:
			print('Unknown message! The header is '+header)
			for each in players:
				each.socket.sendall(data.encode())

class EchoServer(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

	def handle_accepted(self, sock, addr):
		handler = EchoHandler(sock)

if __name__ == "__main__":
	db = gamedb()
	players = []
	server = EchoServer('0.0.0.0', 9999)
	asyncore.loop()
