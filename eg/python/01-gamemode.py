#!/usr/bin/env python

from __future__ import print_function

import sys
import re

# Import the minecraft-control client library.
from mcclient import MinecraftClient

"""01-gamemode.py: A command that lets a whitelist of users change their game
modes with a special 'command' issued in chat.

Usage: 01-gamemode.py [--debug] <host> <port> <password> <list of users to whitelist>
Ex:    01-gamemode.py localhost 2001 secret notch dinnerbone"""

# Get the whitelist.
if len(sys.argv) == 1:
    print("Usage: 01-gamemode.py <list of users to whitelist>")
    sys.exit(1)

debug = False
host, port, password = None, None, None
whitelist = []

if sys.argv[1] == "--debug":
    debug = True
    host, port, password = sys.argv[2:5]
    whitelist = [x.lower() for x in sys.argv[5:]]
else:
    host, port, password = sys.argv[1:4]
    whitelist = [x.lower() for x in sys.argv[4:]]

# Connect to the server.
client = MinecraftClient(
    debug    = debug,
    host     = host,
    port     = port,
    password = password,
)

def on_authed(client):
    print("Authentication successful!")
    client.sendline("say 01-gamemode.py demo started. Whitelist: {}".format(str(whitelist)))

def on_error(client, error):
    print("Failed to authenticate: {}".format(error))

def on_message(client, message):
    print("Saw server message: {}".format(message))

    # Look for people joining the game.
    if "joined the game" in message:
        match = re.search(r': (.+?) joined the game', message)
        if match:
            username = match.group(1)
            client.sendline("say Welcome, {}!".format(username))

    # Look for user commands.
    match = re.search(r'<(.+?)> (!\w+)', message)
    if match:
        username = match.group(1)
        command  = match.group(2)
        print("Detected command use: <{}> {}".format(username, command))

        # Whitelisted user?
        if username.lower() in whitelist:
            # Process the commands.
            if command == "!creative":
                client.sendline("gamemode 1 {}".format(username))
            elif command == "!survival":
                client.sendline("gamemode 0 {}".format(username))
            else:
                client.sendline("say Unsupported command. Valid ones are: !creative !survival")
        else:
            client.sendline("say Command ignored; not whitelisted.")

# Attach the handlers.
client.add_handler("auth_ok", on_authed)
client.add_handler("auth_error", on_error)
client.add_handler("server_message", on_message)

# Connect!
client.connect()
client.start()