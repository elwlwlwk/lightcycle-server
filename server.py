#!/usr/bin/env python3
import asyncore
import socket
import sqlite3
class gamedb:
	def __init__(self, name='lcdb'):
		self.conn=sqlite3.connect(name)
		c=self.conn.cursor()
		try:
			c.execute('create table game (data text)')
		except sqlite3.OperationalError:
			print('Table already exist.')

	def add(self, data):
		c=self.conn.cursor()
		c.execute('insert into game values (?)',(data,))
		self.conn.commit()
		c.close

class Player:
	def __init__(self, socket, ID):
		self.socket = socket
		self.ID = ID

class EchoHandler(asyncore.dispatcher_with_send):
	def handle_read(self):
		data = self.recv(1024)
		data = str(data).strip()
		print('accept from clint')
		print('message is '+data)
		header = data.split()[0]
		body = data.split()[1]
		db.add(body) #TODO: Use db for specific data.
		if 'HELO' == header:
			players.append(Player(self, body))
		elif 'FUCKYOU' == header:
			for each in players:
				if each.socket is not self:
					each.socket.send(data.encode('utf-8'))
		else:
			print('Unknown message! The header is '+header)

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
	db=gamedb()
	players = []
	server = EchoServer('0.0.0.0', 9999)
	asyncore.loop()
