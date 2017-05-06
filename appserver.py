#! /usr/bin/env python3
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from os import curdir, sep
import mimetypes
import cgi
import threading
import sqlite3
import json

PORT = 8001

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		if self.path=="/index":
			self.path="/index.html"

		try:
			f = open(curdir + sep + self.path, 'rb')
			mimetype, _ = mimetypes.guess_type(self.path)
			try:
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			except:
				print ("Connection Aborted: Established connection has been dropped")
			return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			try:
				conn = sqlite3.connect('test.db')
			except:
				print ("Database connection failed")

			if self.path == "/Form":
				form = cgi.FieldStorage(
					fp=self.rfile,
					headers=self.headers,
					environ={'REQUEST_METHOD':'POST',
					'CONTENT_TYPE':self.headers['Content-Type'],
				})

				try:
					self.send_response(200)
					self.end_headers()
					message = "Under Development"
					self.wfile.write(message.encode("utf-8"))
				except:
					print ("Unable to send response: process error")

			if self.path == "/searchDetails":
				try:
					print ("searchDetail")
					self.wfile.write("searchDetail:Detail".encode("utf-8"))
				except:
					print ("Unable to fetch search detail")

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass

try:
	server = ThreadedTCPServer(('', PORT), myHandler)
	print ('Started httpserver on port ' , PORT)
	
	ip,port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	allow_reuse_address = True
	server.serve_forever()

except KeyboardInterrupt:
	print ('CTRL + C RECEIVED - Shutting down the REST server')
	server.socket.close()