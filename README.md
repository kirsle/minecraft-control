# Minecraft Control

![02-rivescript.py](https://raw.github.com/kirsle/minecraft-control/master/eg/python/screenshots/02-rivescript.png)

This is a simple Python telnet server that wraps the Minecraft server and
forwards its input/output over a TCP connection. It allows for remotely
controlling the Minecraft server over telnet, or from an automated program
(bots, anyone?)

It supports authentication, so the TCP server may listen on a public facing
port and require a password to log in. Currently the supported login methods
are plain text, or a secure challenge-response algorithm using MD5 or SHA1
hashing, computed like for example:

```python
sha1(challenge + sha1(password))
```

By default the TCP server listens on the loopback address and uses plain
text passwords. It's recommended that you edit the `settings.ini` and use
`md5` or `sha1` as the authentication method if you're going to run the
server on a public-facing port (to prevent possible network sniffing for
passwords).

Set the server address to `0.0.0.0` in `settings.ini` for it to listen on
all interfaces.

# Usage

```bash
minecraft-control [options] java -jar minecraft_server.jar nogui
```

This is also confirmed to work under Windows, either with the .jar file or
the .exe file. For example (assuming you already have python.exe and java.exe
in your `%Path%`):

```
python minecraft-control minecraft_server.1.7.4.exe nogui
```

## Options

* `--help, -h, -?`: Show the full help, and exit.
* `--version, -v`: Show the version number, and exit.
* `--debug`: Turn on debugging.
* `--config, -c <file>`: Use a different config file (default is `settings.ini`)
* `--cd, -d <password>`: Change directories before executing the Minecraft server.

After the command line options, enter the normal command you run to start the
Minecraft server, e.g. `java -jar minecraft_server.jar nogui`. This is the
command that `minecraft-control` will run and wrap the input/output from.

# Configuration

Edit the file `settings.ini` to configure the host and port that the TCP
server will listen on. By default it only listens on the loopback device
(`127.0.0.1`) on port 2001. Change to `0.0.0.0` to listen on all interfaces.

The `[auth]` section is where you set up the authentication password. Read
the comments in `settings.ini` for usage information.

# Client Library and Examples

There's a Python client library called `mcclient.py` located in the
[eg/python](https://github.com/kirsle/minecraft-control/tree/master/eg/python)
directory, and a couple of example scripts that use the client module to do
some neat things.

# Remote Controlling Minecraft

Once configured, run the command like in the Usage section above. It will
start the Minecraft server and begin listening on the TCP port. You can then
telnet to that port, authenticate yourself, and begin controlling Minecraft.

Typical telnet flow (where `<<<` are messages from the server, and `>>>` are
your messages sent *to* the server):

```
$ telnet localhost 2001
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
<<< AUTH_METHOD plain
>>> AUTH secret
<<< AUTH_OK
>>> seed
<<< [19:29:17] [Server thread/INFO]: Seed: 1849169679655839604
>>> stop
<<< [19:29:23] [Server thread/INFO]: Stopping the server
<<< [19:29:23] [Server thread/INFO]: Stopping server
<<< [19:29:23] [Server thread/INFO]: Saving players
<<< [19:29:23] [Server thread/INFO]: Saving worlds
<<< [19:29:23] [Server thread/INFO]: Saving chunks for level 'world'/Overworld
<<< [19:29:23] [Server thread/INFO]: Saving chunks for level 'world'/Nether
<<< [19:29:23] [Server thread/INFO]: Saving chunks for level 'world'/The End
<<< [19:29:24] [Server Shutdown Thread/INFO]: Stopping server
<<< [19:29:24] [Server Shutdown Thread/INFO]: Saving players
<<< [19:29:24] [Server Shutdown Thread/INFO]: Saving worlds
Connection closed by foreign host.
```

## TCP Server Protocol

The protocol is extremely simple (and is only used for authentication, really).
Once the connected client has passed the authentication phase, *all* output from
the Minecraft server is broadcasted to all authenticated clients, and all *input*
from the authenticated clients is sent into the Minecraft server as standard
input.

The authentication phase supports these commands:

**From the Server:**

* `AUTH_METHOD <method> [challenge]`

The server sends this to newly connected clients. It is the value of the auth
method from `settings.ini` to inform the client as to how they should proceed.

If the auth method is not `plain`, then a random challenge is sent in this
message as well, to be used with the challenge-response authentication.

* `AUTH_OK`, `AUTH_ERROR`

The server will send this message in response to an `AUTH` command sent by
the client. The messages indicate successful and unsuccessful authentication
attempts, respectively.

* `UNKNOWN_COMMAND`

If the client sends anything other than an `AUTH` command during the auth
phase, the server will say this.

**From the Client:**

* `AUTH <password>`

The client provides the authentication password. The server will either reply
with `AUTH_OK` or `AUTH_ERROR`.

# AUTHOR

Noah Petherbridge, http://www.kirsle.net/

# LICENSE

```
Minecraft Control
Copyright (C) 2014 Noah Petherbridge

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
```
