#!/usr/bin/env python3
# 28-Apr-2012
# wibblemyflibble@gmail.com
# reallyrose
# Python IRCEirtaBot
# Probably useless, poor thing.


# 03.03.2022: modified by polprog, converted to python3 and tested on espernet/libera
# Most functions operating on data want bytes object, some of them are not yet converted
# I just needed a base for a link title bot so I took this. Fixed up the network code a bit
# This may be easily extended as needed.
# until 07.03.2022: further modifications, refactor code

import time, socket, sys, string, re, random, string
import signal, traceback
from urllib.request import urlopen
from urllib.error import URLError
from collections import defaultdict
from random import choice
from datetime import datetime


import urltitle
import networking
import abspqmcdu

# Errors taken up to E004
# Infos taken up to I006


version    = '1.0.12 python3.5'

TheChosen  =  eval(open ( 'TheChosen.txt' ).read ())  # People that can do special things
IgnoreUser =  eval(open ( 'IgnoreUser.txt' ).read ()) # People to be ignore by the bot
botnick    =  'lolprog'
#channel    =  '#!/bin/bash'
channel    =  '#polprog'
password   =  ''
port       =  6667
server     =  'irc.esper.net'
#cmdprefix  =  '+++'
cmdprefix  = '!'
starttime  = datetime.now()




print("binprog version", version, "starting on", str(starttime))
print("Bot operators:" + str(TheChosen))
print("Ignores:" + str(IgnoreUser))
print("Bot nickname:", botnick, "command prefix is", cmdprefix)


# Connecting to a server:
print("Opening socket to IRC server", str(server)+":"+str(port), end='')
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

irc.connect ( ( server, port ) )
irc.settimeout(1.0)
print("Done.")

#print(irc.recv ( 4096 ))


# Set nick

running = True


def ircsend(data):
        irc.send(data.encode('utf-8'))
        print(">", data, end='')

# Many Functions, fun for all the family:

def Volunteer (): # For potential volunteers

	global User

	ircsend (
                'PRIVMSG ' + User +
                ' : Why not become one of the awesome Green Shirts for xxxxxx! http://xxxxxx.com/volunteer \r\n'
        )

	ircsend (
                'PRIVMSG ' + User +
                ' : If you have questions, highlight rooose or reallyrose (Just say the name into chat) or if she isn\'t here, email volunteer@xxxxxx.com \r\n'
        )

def Quit (): # only quit when I say so

        global TheChosen

        QUser = data [1:data.find('!')] #Slice
        print(QUser,  "requested quit...")
        if QUser in TheChosen:
                ircsend ('PRIVMSG ' + channel +
                        ' :I002 disconnecting from remote. Bye bye! \r\n')

                ircsend('QUIT\r\n')

                global running

                running = False # quit program

        else:
                ircsend ('PRIVMSG ' + channel + ' :E001 permission denied\r\n') # if not...

def Source():
         ircsend ('PRIVMSG ' + channel + ' :I004 https://github.com/polprog/binprog\r\n')

                
def GreetNew (): # Greet new users

	global IgnoreUser
	global User

	if data.find ( 'JOIN ' ) != -1:

		if User in IgnoreUser:

			pass

		else:

			ircsend (
                                'PRIVMSG ' + channel +
                                ' :Welcome to ' + channel + ', ' + User + '\r\n'
                        )
			
def Cat (data): # function to pull a random cat picture from a dictionary of cat pictures in a txt file

	cats = ['=^.^=', '~=[,,_,,]:3', '^-.-^J', '>:3', '=^w^=', '__mnm^^']
	random.seed(datetime.now())
	PickCat = random.choice ( cats )
        # post it
	ircsend(
                'PRIVMSG ' + channel +
                ' :I006 kitteh! ' + PickCat + '\r\n'
        )
	
def Version(data):
	ircsend (
                'PRIVMSG ' + channel +
                ' :I004 binprog version '+version+', cmdprefix is '+cmdprefix+'\r\n')

def Help (data): # Halp!
        user = data [1:data.find('!')] #Slice
        ircsend ('PRIVMSG ' + user +
                        ' :I005 Command prefix is '+cmdprefix+'; Available commands: ath - hangup (oper only), help - this, t <url]> - print url title, uptime - print uptime, version - bot version, ping - ping back, cat - send a kitteh \r\n')




def sigint_handler(signal, frame):
    print('Interrupted. Gracefully closing IRC socket...')
    ircsend("QUIT binprog closing (caught ^C)\r\n")
    while True:
            data = irc.recv(4096)
            if(data == b''):
                    print("Server closed connection. Exiting!")
                    break
            print(data)
    sys.exit(0)
    
signal.signal(signal.SIGINT, sigint_handler)

# Core code

state = "connecting"

lasturl = ''


print("Taking nick", botnick)
ircsend('NICK ' + botnick + '\r\n')
ircsend('USER ' + botnick + ' ' + botnick + ' ' + botnick + ' :BeepBeep\r\n')

#TODO: rewrite to process packets line by line.

while running:
        
        #print("Waiting for data...")

        data = b''
        while True:
                try:
                        data = data + irc.recv(128)
                except socket.timeout:
                        pass
                        break
        data = data.decode('utf-8')
        #print("Received", len(data), "bytes in this round...")
                
        User = data [ 1:data.find ('!') ] #Slice user out 
        print (data, end="")

        #GreetNew ()
        
        # Don't join chan til server has finished spamming
        if data.find ('End of /MOTD ') != -1 and state == "connecting":
                state = "connected"
                ircsend('JOIN ' + channel + '\r\n')

        if data.find ('End of /NAMES list.' ) != -1: # don't reg til joined chan
                if password != '':
                        print("Attepmting to identify to NickServ...")
                        ircsend('PRIVMSG NickServ :IDENTIFY '
                                + ' ' + password + '\r\n')
                Version(data) #send a version string as hello
                
        if data.find ( 'PING :' ) != -1: # ping/pong server
                pingloc = data.find( 'PING :' )
                pingpayload = data[pingloc:].split()[1]
                ircsend('PONG ' + pingpayload + '\r\n')
                

        try:
                posted_urls = re.findall("PRIVMSG.*(https?://[^ ]*)", data)
                if posted_urls != []:
                        #print("user", User, "posted url", posted_urls)
                        lasturl = posted_urls[0]
                        try:
                                title = urltitle.UrlTitle(data)
                                #print("URL TITLE:", title)
                                ircsend('PRIVMSG ' + channel + " :Title: " + title + "\r\n")
                                continue
                        except URLError:
                                pass
                        
                
                if data.find ( (cmdprefix + "ath") ) != -1:
                        Quit ()

                elif data.find ( (channel + ' :' + cmdprefix + 'help') ) != -1:
                        Help (data)

                elif data.find ( (channel + ' :' + cmdprefix + 'dns') ) != -1:
                        cmdloc = data.find ( (channel + ' :' + cmdprefix + 'dns') )
                        addrname = data[cmdloc:].split()[2]
                        print("addrname=", addrname)
                        ircsend('PRIVMSG ' + channel + " :" + networking.dns_lookup(addrname) + "\r\n")

                elif data.find ( (channel + ' :' + cmdprefix + 'rdns') ) != -1:
                        cmdloc = data.find ( (channel + ' :' + cmdprefix + 'rdns') )
                        addrname = data[cmdloc:].split()[2]
                        print("addrname=", addrname)
                        ircsend('PRIVMSG ' + channel + " :" + networking.rdns_lookup(addrname) + "\r\n")

                elif data.find ( (channel + ' :' + cmdprefix + 'abspqmcdu') ) != -1:
                        cmdloc = data.find ( (channel + ' :' + cmdprefix + 'abspqmcdu') )
                        addrname = data[cmdloc:].split()[2]
                        print("addrname=", addrname)
                        ircsend('PRIVMSG ' + channel + " :" + abspqmcdu.abspqmcdu(addrname) + "\r\n")

                        
                elif data.find (( channel + ' :' + cmdprefix + 't')) != -1:
                        try:
                                title = urltitle.UrlTitle(data)
                        
                        except URLError as e:
                                ircsend('PRIVMSG ' + channel +
                                          " :E003 urllib error: "+str(e.reason)+"\r\n")
                                continue
                        
                        if(title == -1):
                                ircsend('PRIVMSG ' + channel +
                                          " :E002 not a supported uniform resource locator\r\n")
                                continue
                        if(title == -2):
                                ircsend('PRIVMSG ' + channel +
                                          " :E004 sorry, cannot find a title tag!\r\n")
                        
                        if len(title) > 80:
                                title = title[:80] + " [trunc'd]"
                                print(title)
                        ircsend('PRIVMSG ' + channel + " :Title: " + title + "\r\n")
                        
                elif data.find ( (channel + ' :' + cmdprefix + 'uptime') ) != -1:
                                uptime = datetime.now() - starttime
                                ircsend('PRIVMSG ' + channel + " :I001 uptime is " + str(uptime) + "\r\n")
                elif data.find ( (channel + ' :' + cmdprefix + 'version') ) != -1:
                                Version(data)
                                
                elif data.find ( (channel + ' :' + cmdprefix + 'ping') ) != -1:
                        ircsend('PRIVMSG ' + channel + " :I003 go ping yourself "+User+"\r\n")
                        
                elif data.find ( (channel + ' :' + cmdprefix + 'cat') ) != -1:
                        Cat(data)

                elif data.find ( (channel + ' :' + cmdprefix + 'src') ) != -1:
                        Source()

                #elif data.find ( (channel + ' :' + cmdprefix + 'xxx').encode('utf-8') ) != -1:
                #        raise ValueError()

        except Exception as e:
                print("Non critical exception:")
                traceback.print_exc()
                print("End of stack trace")
                ircsend('PRIVMSG ' + channel + " :E999 command failed with uncaught exception\r\n")
