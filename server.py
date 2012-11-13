#!/usr/bin/env python3
import socketserver
class MyTCPHandler(socketserver.StreamRequestHandler):
	def handle(self):
		self.data=self.rfile.readline().strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		self.request.sendall(self.data.upper())

if __name__=="__main__":
	HOST,PORT="",9999
	server=socketserver.TCPServer((HOST,PORT),MyTCPHandler)
	server.serve_forever()
