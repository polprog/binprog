
   |_  . ._   _   _  _   _
   :_; | | | |_| |  |_| |_|
             :           /;

binprog is a small IRC bot written in python.
Originally based on LoriBot [1], I have improved
the network code and changed the functionality.

< ME> 2 hours 9 minutes to write irc bot
< ME> formidable

Configuration and usage:
-------------------------'

Edit binprog.py to set these variables:
botnick    =  'xxxxxxxxx'  # Bot nickame
channel    =  '#xxxxxxxx'  # Channel name the bot operates on
password   =  '---------'  # NickServ pw
port       =  6667
server     =  'xxxxxxxxxx' # IRC server and port
cmdprefix  =  '!'          # Command prefix (any string)

The operator and ignore lists are eval'd from the two text files. Use

$ echo "['oper1','oper2'...]" > TheChosen.txt

to add oper1 and oper2 as bot operators (yes, this is a python list that the
eval evals)

Then register the nickname witn NickServ and start.

./binprog.py

Commands
---------'

Currently the most important function the bot supports is titling pasted links.
Use the 'ath' command to make it gracefully disconnect. use 'help' or read the source code
to see the list of commands.

Expanding
----------'

The commands can be added as python functions. Take a look at existing ones
to see how it's done. In short, the while loop searches incoming data for commands,
then parses the line for information. More complicated behavior can be exported
to functions which optionally take the data chunk as a parameter.

Todo
-----'

Cleanup and modularize code, add a more sophisticated command parser to allow for
registering pairs of "command":"python function" kind

Add youtube API for pasting video titles

1 - https://gist.github.com/pikpik/2705658
