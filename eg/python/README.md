# Python Examples

This folder contains a couple examples of remote controlling a Minecraft server
in Python. This list of examples will grow in the future; if you come up with a
neat demo, give me a pull request and I'll add it here!

# mcclient.py

The module `mcclient.py` provides a client interface to connect to the
`minecraft-control` server, and it's what all these examples use. See its
documentation for usage information, or just look at the examples!

```python
from mcclient import MinecraftClient

client = MinecraftClient("localhost", 2001, "secret")

# Provide functions to handle events.
client.add_handler("auth_ok", on_auth_ok)
client.add_handler("auth_error", on_auth_error)
client.add_handler("server_message", on_message)

client.connect()
client.start()
```

# Examples

## 01-gamemode.py

![01-gamemode.py](https://raw.github.com/kirsle/minecraft-control/master/eg/python/screenshots/01-gamemode.png)

This implements a white list of players that are allowed to use "game mode
commands" to toggle their game mode, *without* needing to be the server
operator.

Provide the whitelisted player names as command line options, for example
to whitelist notch and dinnerbone:

```
python 01-gamemode.py localhost 2001 secret notch dinnerbone
```

In-game, players can send a message consisting of `!creative` or
`!survival` to switch their game modes respectively. Only users who
appear in the whitelist can do this; other users will be told they're
not allowed.

## 02-rivescript.py

![02-rivescript.py](https://raw.github.com/kirsle/minecraft-control/master/eg/python/screenshots/02-rivescript.png)

This implements a [RiveScript](http://www.rivescript.com/) chatbot as a
Minecraft "player". It uses the `/tellraw` command to send messages that
appear like a normal player. Players can talk to the bot by prefixing a
message with the bot's name (Aiden).

You'll need to `pip install python-rivescript` to get the RiveScript
module.

```
python 02-rivescript.py localhost 2001 secret
```
