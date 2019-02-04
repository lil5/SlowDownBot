#!/bin/python3

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm

# Inspired by Aswin Ganesh
# https://agzuniverse.blogspot.com/2016/05/irc-bot-in-python-tutorial.html

import sys
import getopt
import math
import time
import socket
import re

# PURPLE = '\033[95m'
# CYAN = '\033[96m'
# DARKCYAN = '\033[36m'
# BLUE = '\033[94m'
# GREEN = '\033[92m'
# YELLOW = '\033[93m'
# RED = '\033[91m'
# BOLD = '\033[1m'
# UNDERLINE = '\033[4m'
# END = '\033[0m'

iskick=0
isban=0
waitingtime=30
server="irc.freenode.net"
port=6667
botnick="SlowDownBot"
channel="#testslowbot"

# CLI Arguments
try:
	opts, args = getopt.getopt(
		sys.argv[1:],
		"hkbs:p:n:c:t:",
		["help", "kick", "ban", "server=", "port=", "nick=", "channel=", "time="]
	)
except getopt.GetoptError:
	print('slowircbot.py [options]')
	sys.exit(2)
for opt, arg in opts:
	if opt in ('-h','--help'):
		print('''\
slowircbot.py [options]

\033[1mOPTIONS:\033[0m
-h, --help    Show this help message
-k, --kick    Kick people who do not respect the curfew (default off)
-b, --ban     Ban people who do not respect the curfew (default off)
-s, --server  IRC Server (default irc.freenode.net)
-p, --port    IRC Server Port (default 6667)
-n, --nick    Nick of bot (default SlowDownBot)
-c, --channel Channel to enforce curfew on (with #)
-t, --time    Waiting time of curfew in seconds (default 30)
		''')
		sys.exit()
	elif opt in ('-k', '--kick'):
		iskick=1
	elif opt in ('-b', '--ban'):
		isban=1
	elif opt in ('-s', '--server'):
		server=str(arg)
	elif opt in ('-p', '--port'):
		port=int(arg)
	elif opt in ('-n', '--nick'):
		botnick=str(arg)
	elif opt in ('-c', '--channel'):
		channel=str(arg)
	elif opt in ('-t', '--time'):
		waitingtime=int(arg)

#Establish connection
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server,port))
irc.setblocking(False)
time.sleep(1)
irc.send(("USER "+botnick+" "+botnick+" "+botnick+" :Hello! I am a slowdown bot!\r\n").encode())
time.sleep(1)
irc.send(("NICK "+botnick+"\n").encode())
time.sleep(1)
irc.send(("JOIN "+channel+"\n").encode())

print("starting...")
time.sleep(1)

timer=0
writingmode=1
waitingtime=waitingtime*2
hasbeenactive=0

while 1:
	time.sleep(0.5)
	try:
		text=irc.recv(2040)
	except Exception:
		pass
	if str(text).find("PING") != -1:
		irc.send(("PONG "+str(text).split()[1]+"\r\n").encode())

	# testing
	# if str(text).lower().find(":@hi")!=-1:
	# 	irc.send(("PRIVMSG "+channel+" :Hello!\r\n").encode())
	# end testing

	# police
	if str(text).find("PRIVMSG "+channel) != -1:
		print(str(text))
		hasbeenactive=1
		if writingmode != 1 and timer > 2:
			# get nick of curfew breaker
			try:
			    evilnick = re.search(':.{2,16}(?=!)', str(text)).group(0)[1:]
			except Exception:
			    print('No nick found')
			else:
				# policing evilnick
				if iskick == 1:
					irc.send(('KICK '+channel+' '+evilnick+' :Posting during curfew.\r\n').encode())
					print('Kicking '+evilnick)
				elif isban == 1:
					irc.send(('BAN '+channel+' '+evilnick+' :Posting during curfew.\r\n').encode())
					print('Banning '+evilnick)
				else:
					irc.send(("PRIVMSG "+channel+" :"+evilnick+" Curfew is in effect for "+str( math.floor((waitingtime - timer)/2) )+" seconds.\r\n").encode())

	# street lights
	if timer == waitingtime:
		timer=0
		if writingmode == 1 and hasbeenactive == 1:
			irc.send(("PRIVMSG "+channel+" :Please stop posting for "+str( math.floor(waitingtime/2) )+" seconds.\r\n").encode())
			writingmode = 0
		elif writingmode !=1:
			if hasbeenactive == 1:
				irc.send(("PRIVMSG "+channel+" :"+str( math.floor(waitingtime/2) )+" seconds are up.\r\n").encode())
			writingmode = 1
			hasbeenactive = 0
	else:
		timer+=1

	# testing
	# print(str(text))
	text=""
