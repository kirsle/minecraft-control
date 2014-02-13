# Python Examples

This folder contains a couple examples of remote controlling a Minecraft server
in Python. This list of examples will grow in the future; if you come up with a
neat demo, give me a pull request and I'll add it here!

# mcclient.py

The module `mcclient.py` provides a client interface to connect to the
`minecraft-control` server, and it's what all these examples use. See its
documentation for usage information, or just look at the examples!

# Examples

## 01-gamemode.py

This implements a white list of players that are allowed to use "game mode
commands" to toggle their game mode, *without* needing to be the server
operator.

Provide the whitelisted player names as command line options, for example
to whitelist notch and dinnerbone:

```
python 01-gamemode.py localhost 2001 secret notch dinnerbone
```

## 02-rivescript.py

This implements a [RiveScript](http://www.rivescript.com/) chatbot as a
Minecraft "player". It uses the `/tellraw` command to send messages that
appear like a normal player. Players can talk to the bot by prefixing a
message with the bot's name (Aiden).

You'll need to `pip install python-rivescript` to get the RiveScript
module.

```
python 02-rivescript.py localhost 2001 secret
```
