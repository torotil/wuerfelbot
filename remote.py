# -*- coding: utf-8 -*-
import socket
import time
from random import randint

class Game:
	
	def __init__(self, conn, player, name):
		self.p = player
		self.host = conn
		self.active = False
		self.finished = False
		self.name = name

	def handleMsg(self, line):
		line = line.strip()
		parts = line.split(" ", 3)
		if parts:
			method = self.lookupMethod(parts[0]) or self.do_UNKNOWN
			if len(parts) > 1:
				return method(parts[1:len(parts)])
			else:
				return method()
		else:
			raise SyntaxError, 'bad syntax'    
		
	def lookupMethod(self, command):
		return getattr(self, 'do_' + command.upper(), None)
			
	def do_HELO(self, rest):
		self.send("AUTH %s" % self.name)
	
	def send(self, msg):
		print ">>> %s" % msg
		self.socketf.write("%s\n" % msg)
	
	def do_TURN(self, rest):
		if not self.active:
			print "Begin turn"
			self.p.beginTurn(int(rest[0]), int(rest[1]) )
			self.active = True
		self.take_turn()
	
	def take_turn(self):
		if self.p.decide():
			self.send('ROLL %d' % randint(1,60))
		else:
			print "End turn with SAVE"
			self.active = False
			self.send('SAVE')
	
	def do_THRW(self, rest):
		n = int(rest[0])
		if(self.active == True):
			if (n == 6):
				self.active = False
				print "End turn with 6"
			else:
				self.p.thrown(n)
		else:
			self.p.op_threw(n)
			
	def do_WIN(self, rest):
		self.finished = True
			
	def do_DEF(self, rest):
		self.finished = True
	
	def do_DENY(self, rest):
		self.finished = True

	def do_UNKNOWN(self, rest):
		raise NotImplementedError, "received unknown command"        
	
	def play(self):
		connected = False
		count = 0
		while connected == False:
			count = count + 1
			print "Trying to connect (%d) …" % count
			try:
				self.socket = socket.create_connection(self.host, 30)
				self.socketf = self.socket.makefile('w', 0)
				connected = True
			except:
				print "Versuch", count, ": Verbindung konnte nicht hergestellt werden"
				time.sleep(5)    
		print "connected!"
		empty = 1
		try:
			while self.finished == False:
				command = self.socketf.readline().strip()
				if (command):
					print "<<< " + command
					self.handleMsg(command)
				else:
					if empty > 10:
						print 'too many empty lines - aborting'
						break
					print 'empty line %d - aborting' % empty
					empty += 1
					time.sleep(1)
		finally:
			self.socket.close()
			print "Socket closed"
