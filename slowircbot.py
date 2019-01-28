#!/bin/python3

# Inspired by Aswin Ganesh
# https://agzuniverse.blogspot.com/2016/05/irc-bot-in-python-tutorial.html

import sys
import math
import time
import socket
server="irc.freenode.net"
botnick="SlowDownBot"
channel="#testslowbot"

#Establish connection
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server,6667))
irc.setblocking(False)
time.sleep(1)
irc.send(("USER "+botnick+" "+botnick+" "+botnick+" :Hello! I am a test bot!\r\n").encode())
time.sleep(1)
irc.send(("NICK "+botnick+"\n").encode())
time.sleep(1)
irc.send(("JOIN "+channel+"\n").encode())

print("starting...")
time.sleep(1)

timer=0
writingmode=1
waitingtime=30*2
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
	if str(text).lower().find(":@hi")!=-1:
		irc.send(("PRIVMSG "+channel+" :Hello!\r\n").encode())
	# end testing

	# pig
	if str(text).find("PRIVMSG "+channel) != -1:
		hasbeenactive=1
		if writingmode != 1:
			irc.send(("PRIVMSG "+channel+" :Please stop posting for "+str( math.floor((waitingtime - timer)/2) )+" seconds.\r\n").encode())

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
		
	print(str(text))
	text=""

