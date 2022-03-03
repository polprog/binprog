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


import time, socket, sys, string, re, random, string
import signal, traceback
from urllib.request import urlopen
from urllib.error import URLError
from collections import defaultdict
from random import choice
from datetime import datetime
import urltitle


# Errors taken up to E004
# Infos taken up to I006


version    = '1.0.6 python3.5'

TheChosen  =  eval(open ( 'TheChosen.txt' ).read ())  # People that can do special things
IgnoreUser =  eval(open ( 'IgnoreUser.txt' ).read ()) # People to be ignore by the bot
botnick    =  'xxxxxxxxx'  # Bot nickame
channel    =  '#xxxxxxxx'  # Channel name the bot operates on
password   =  '---------'  # NickServ pw
port       =  6667
server     =  'xxxxxxxxxx' # IRC server
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

print("Taking nick", botnick)
irc.send ( ('NICK ' + botnick + '\r\n').encode('utf8') )
irc.send(('USER ' + botnick + ' ' + botnick + ' ' + botnick + ' :BeepBeep\r\n').encode('utf-8'))


running = True



# Many Functions, fun for all the family:

def Volunteer (): # For potential volunteers

	global User

	irc.send (
                'PRIVMSG ' + User +
                ' : Why not become one of the awesome Green Shirts for xxxxxx! http://xxxxxx.com/volunteer \r\n'
        )

	irc.send (
                'PRIVMSG ' + User +
                ' : If you have questions, highlight rooose or reallyrose (Just say the name into chat) or if she isn\'t here, email volunteer@xxxxxx.com \r\n'
        )

def Quit (): # only quit when I say so

        global TheChosen

        QUser = data [ 1:data.find ( b'!' ) ].decode('utf-8') #Slice
        print(QUser,  "requested quit...")
        if QUser in TheChosen:
                irc.send (
                        ('PRIVMSG ' + channel +
                        ' :I002 disconnecting from remote. Bye bye! \r\n'
                ).encode('utf-8'))

                irc.send(('QUIT\r\n').encode('utf-8'))

                global running

                running = False # quit program

        else:
                irc.send ( ('PRIVMSG ' + channel + ' :E001 permission denied\r\n').encode('utf-8') ) # if not...

def GreetNew (): # Greet new users

	global IgnoreUser
	global User

	if data.find ( 'JOIN ' ) != -1:

		if User in IgnoreUser:

			pass

		else:

			irc.send (
                                'PRIVMSG ' + channel +
                                ' :Welcome to ' + channel + ', ' + User + '\r\n'
                        )
			
def Cat (data): # function to pull a random cat picture from a dictionary of cat pictures in a txt file

	cats = ['=^.^=', '~=[,,_,,]:3', '^-.-^J', '>:3', '=^w^=', '__mnm^^']
	random.seed(datetime.now())
	PickCat = random.choice ( cats )
        # post it
	irc.send ((
                'PRIVMSG ' + channel +
                ' :I006 kitteh! ' + PickCat + '\r\n').encode('utf-8')
        )
	
def Version(data):
	irc.send ((
                'PRIVMSG ' + channel +
                ' :I004 binprog version '+version+', cmdprefix is '+cmdprefix+'\r\n').encode('utf-8')
        )

def Help (data): # Halp!
        user = data [ 1:data.find ( b'!' ) ].decode('utf-8') #Slice
        irc.send (
                ('PRIVMSG ' + user +
                        ' :I005 Command prefix is '+cmdprefix+'; Available commands: ath - hangup (oper only), help - this, t <url]> - print url title, uptime - print uptime, version - bot version, ping - ping back, cat - send a kitteh \r\n').encode('utf-8')
                )




def sigint_handler(signal, frame):
    print('Interrupted. Gracefully closing IRC socket...')
    irc.send("QUIT binprog closing (caught ^C)\r\n".encode('utf-8'))
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

while running:
        
#        print("Waiting for data...")

        data = b''
        while True:
                try:
                        data = data + irc.recv(128)
                except socket.timeout:
                        pass
                        break
                
 #       print("Received", len(data), "bytes in this round...")
                
        User = data [ 1:data.find ( b'!' ) ].decode('utf-8') # Slice
        print (data.decode('utf-8'), end="")

        #GreetNew ()
        
        # Don't join chan til server has finished spamming
        if data.find (b'End of /MOTD ') != -1 and state == "connecting":
                state = "connected"
                irc.send(('JOIN ' + channel + '\r\n').encode('utf-8'))

        if data.find ( b'End of /NAMES list.' ) != -1: # don't reg til joined chan
                print("Attepmting to identify to NickServ...")
                print(('PRIVMSG NickServ :IDENTIFY ' + 
                           ' ' + password + '\r\n').encode('utf-8'))
                irc.send(('PRIVMSG NickServ :IDENTIFY '
                           + ' ' + password + '\r\n').encode('utf-8'))
                Version(data) #send a version string as hello
        if data.find ( b'PING' ) != -1: # ping/pong server
                irc.send(('PONG ' + data.split()[1].decode('utf-8') + '\r\n').encode('utf-8'))

        try:
                posted_urls = re.findall("PRIVMSG.*(https?://[^ ]*)", data.decode('utf-8'))
                if posted_urls != []:
                        #print("user", User, "posted url", posted_urls)
                        lasturl = posted_urls[0]
                        try:
                                title = urltitle.UrlTitle(data)
                                #print("URL TITLE:", title)
                                irc.send(('PRIVMSG ' + channel + " :Title: " + title + "\r\n").encode('utf-8'))
                                continue
                        except URLError:
                                pass
                        
                
                if data.find ( (cmdprefix + "ath").encode('utf-8') ) != -1:
                        Quit ()

                elif data.find ( (channel + ' :' + cmdprefix + 'help').encode('utf-8') ) != -1:
                        Help (data)
                
                elif data.find (( channel + ' :' + cmdprefix + 't').encode('utf-8')) != -1:
                        #print("Processing title...", end='')
                        try:
                                title = urltitle.UrlTitle(data)
                        
                        except URLError as e:
                                irc.send(('PRIVMSG ' + channel +
                                          " :E003 urllib error: "+str(e.reason)+"\r\n").encode('utf-8'))
                                continue
                        
                        if(title == -1):
                                irc.send(('PRIVMSG ' + channel +
                                          " :E002 not a supported uniform resource locator\r\n").encode('utf-8'))
                                continue
                        if(title == -2):
                                irc.send(('PRIVMSG ' + channel +
                                          " :E004 sorry, cannot find a title tag!\r\n").encode('utf-8'))
                        
                        if len(title) > 80:
                                title = title[:80] + " [trunc'd]"
                                print(title)
                        irc.send(('PRIVMSG ' + channel + " :Title: " + title + "\r\n").encode('utf-8'))
                        
                elif data.find ( (channel + ' :' + cmdprefix + 'uptime').encode('utf-8') ) != -1:
                                uptime = datetime.now() - starttime
                                irc.send(('PRIVMSG ' + channel + " :I001 uptime is " + str(uptime) + "\r\n").encode('utf-8'))
                elif data.find ( (channel + ' :' + cmdprefix + 'version').encode('utf-8') ) != -1:
                                Version(data)
                                
                elif data.find ( (channel + ' :' + cmdprefix + 'ping').encode('utf-8') ) != -1:
                        irc.send(('PRIVMSG ' + channel + " :I003 go ping yourself "+User+"\r\n").encode('utf-8'))
                elif data.find ( (channel + ' :' + cmdprefix + 'cat').encode('utf-8') ) != -1:
                        Cat(data)

                #elif data.find ( (channel + ' :' + cmdprefix + 'xxx').encode('utf-8') ) != -1:
                #        raise ValueError()

        except Exception as e:
                print("Non critical exception:")
                traceback.print_exc()
                print("End of stack trace")
                irc.send(('PRIVMSG ' + channel + " :E999 command failed with uncaught exception\r\n").encode('utf-8'))
