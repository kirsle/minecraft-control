# Minecraft Controller

This is a simple Python telnet server that wraps the Minecraft server and
forwards its input/output over a TCP connection. It allows for remotely
controlling the Minecraft server over telnet, or from an automated program
(bots, anyone?)

It supports authentication, so the TCP server may listen on a public facing
port and require a password to log in. Currently the supported login methods
are plain text, or an MD5 or SHA1 hash. Plans for a challenge-response
authentication algorithm will be added shortly.

This project is still in early development. The authentication mechanism isn't
very secure atm (because it's all over cleartext TCP, even with hashed
passwords).

# Usage

```bash
python minecraft-controller.py [options] java -jar minecraft_server.jar nogui
```

## Options

* `--help, -h, -?`: Show the full help, and exit.
* `--version, -v`: Show the version number, and exit.
* `--debug, -d`: Turn on debugging.
* `--config, -c <file>`: Use a different config file (default is `settings.ini`)
* `--md5 <password>`: Generate the MD5 hash of a password, and exit.
* `--sha1 <password>`: Generate the SHA1 hash of a password, and exit.

After the command line options, enter the normal command you run to start the
Minecraft server, e.g. `java -jar minecraft_server.jar nogui`. This is the
command that `minecraft-control` will run and wrap the input/output from.

# Configuration

Edit the file `settings.ini` to configure the host and port that the TCP
server will listen on. By default it only listens on the loopback device
(`127.0.0.1`) on port 2001. Change to `0.0.0.0` to listen on all interfaces.

The `[auth]` section is where you set up the authentication password. Read
the comments in `settings.ini` for usage information.

**Note:** authentication isn't very secure at the moment, so I recommend at
the time that you do NOT have this listen on a public facing port. A more
secure challenge/response auth mechanism will be added in the near future.

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

* `AUTH_METHOD <method>`

The server sends this to newly connected clients. It is the value of the auth
method from `settings.ini` to inform the client as to how they should proceed.

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
RiveScript-Python
Copyright (C) 2013 Noah Petherbridge

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
