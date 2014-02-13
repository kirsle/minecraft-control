#!/usr/bin/env python

from __future__ import print_function

import sys
import re

# pip install python-rivescript
from rivescript import RiveScript

# Import the minecraft-control client library.
from mcclient import MinecraftClient

"""02-rivescript.py: A chatterbot for Minecraft! The bot goes by the name 'Aiden'
and responds to chat messages directed at him, i.e. begin a message with the word
Aiden or @Aiden and he'll respond (if he has a trigger for that message).

This is just a proof of concept example, so the RiveScript code is streamed into
the bot from this file instead of from external .rive files.

Usage: 02-rivescript.py [--debug] <host> <port> <password>
Ex:    02-rivescript.py localhost 2001 secret"""

# Get the whitelist.
if len(sys.argv) == 1:
    print("Usage: 01-gamemode.py <list of users to whitelist>")
    sys.exit(1)

debug = False
host, port, password = None, None, None

if sys.argv[1] == "--debug":
    debug = True
    host, port, password = sys.argv[2:5]
else:
    host, port, password = sys.argv[1:4]

# Initialize the RiveScript bot.
# http://www.rivescript.com/
bot = RiveScript()
bot.stream("""
+ (hello|hi|hey|yo)
- Hello, <id>!
- Hi there, <id>!
- Hey, <id>!

+ (how are you|how you doing)
- Great, you?
- Good.

+ (good|great|awesome)
- Awesome!

+ (not good|not great)
- Aww. =(

+ my name is *
- <set name=<formal>>Nice to meet you, <get name>!

+ (who am i|what is my name)
* <get name> != undefined => Your name is <get name>, seeker!
- I do not know your name.

+ call me *
@ my name is <star>

+ *
- <noreply>
""".split("\n"))
bot.sort_replies()

# Connect to the server.
client = MinecraftClient(
    debug    = debug,
    host     = host,
    port     = port,
    password = password,
)

def on_authed(client):
    print("Authentication successful!")
    bot_message("Hello everyone! I'm a RiveScript bot!")

def on_error(client, error):
    print("Failed to authenticate: {}".format(error))

def on_message(client, message):
    print("Saw server message: {}".format(message))

    # Look for user messages.
    match = re.search(r'<(.+?)> @?aiden (.+?)$', message.lower())
    if match:
        username = match.group(1)
        message  = match.group(2)
        print("Detected message to the bot: <{}> {}".format(username, message))

        reply = bot.reply(username, message)
        if not "<noreply>" in reply:
            bot_message(reply)

def bot_message(message):
    """Send a message 'from' the bot."""
    # Format the message with /tellraw. Here we'll expand it out for easy reading but it has
    # to be condensed into a single line for Minecraft!
    client.sendline(condense_nbt('''
        tellraw @a {
            text:"<Aiden>",
            color:yellow,
            extra:[
                {
                    text:" ''' + message + '''",
                    color:white
                }
            ]
        }
    '''))

# Helper function that condenses down a complex command into a single line.
def condense_nbt(message):
    # Strip the spaces off each line.
    lines   = message.split("\n")
    stripped = list()
    for line in lines:
        stripped.append(line.strip(" "))

    return "".join(stripped)


# Attach the handlers.
client.add_handler("auth_ok", on_authed)
client.add_handler("auth_error", on_error)
client.add_handler("server_message", on_message)

# Connect!
client.connect()
client.start()