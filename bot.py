#!/usr/bin/python

import config
import irclib
import math
import re
import string
import thread
import threading
import time

#irclib.DEBUG = 1

def welcome(connection, event):
	server.send_raw("as auth " + config.gamesurge_user + " " + config.gamesurge_pass)
	server.send_raw("MODE " + nick + " +x")
	server.join(config.channel)

def drop(connection, event):
	print 'I see a drop'

def nickchange(connection, event):
	print 'I see a nickchange'

def pubmsg(connection, event):
	print 'I see a message'

def checkConnection():
	global connectTimer
	if not server.is_connected():
		connect()
	server.join(config.channel)

def connect():
	server.connect(config.network, config.port, nick, ircname = name)

network = 'irc.gamesurge.net'
port = 6667
channel = '#tf2.pug.nahl.dev'
nick = 'TF2HL-AdminBot'
name = 'BOT'

restart = 0
initTime = int(time.time())
initTimer = threading.Timer(0, None)
lastUserPrint = time.time()
minimums = {}
minuteTimer = time.time()
printTimer = threading.Timer(0, None)

# Create an IRC object
irc = irclib.IRC()

# Create a server object, connect and join the channel
server = irc.server()
connect()

irc.add_global_handler('dcc_disconnect', drop)
irc.add_global_handler('disconnect', drop)
irc.add_global_handler('kick', drop)
irc.add_global_handler('nick', nickchange)
irc.add_global_handler('part', drop)
irc.add_global_handler('pubmsg', pubmsg)
irc.add_global_handler('privnotice', pubmsg)
irc.add_global_handler('pubnotice', pubmsg)
irc.add_global_handler('quit', drop)
irc.add_global_handler('welcome', welcome)

# Jump into an infinite loop
while not restart:
    irc.process_once(0.2)
    if time.time() - minuteTimer > 60:
        minuteTimer = time.time()
        checkConnection()

connectTimer.cancel()
