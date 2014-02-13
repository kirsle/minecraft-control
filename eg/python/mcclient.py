#!/usr/bin/env python

from __future__ import print_function
import socket
import hashlib
import time

"""mcclient.py: A client library for minecraft-control."""

# Quick methods for making MD5 or SHA1 hashes.
def md5(message):
    h = hashlib.md5()
    h.update(message)
    return h.hexdigest()

def sha1(message):
    h = hashlib.sha1()
    h.update(message)
    return h.hexdigest()

class MinecraftClient(object):
    """A client library for the minecraft-control server."""


    def __init__(self, host, port, password, methods=None, debug=False):
        """Create a connection to a minecraft-control server.

        * `host` and `port` provide the server information for connecting.
        * `password` is the authentication password.
        * `methods` is the list of acceptable auth methods that the server
          must support one of (to prevent accidentally leaking the password
          if the server uses plain authentication and you aren't expecting it).
        * `debug` turns on some debug messages.
        """
        self.host     = host
        self.port     = int(port)
        self.password = password
        self.debug    = debug
        self.methods  = methods

        # Handlers.
        self.handlers = dict()

        # Current state.
        self.auth_method = None
        self.authed      = False
        self.challenge   = None


    def say(self, message):
        """Emit a debug message."""
        if self.debug:
            print("[DEBUG] {}".format(message))


    def add_handler(self, event, handler):
        """Add an event handler.

        Supported handlers and their arguments are:

        * auth_ok(self):
          Called when the auth handshake is successfully completed. You can now
          get/receive messages from the Minecraft server.
        * auth_error(self, error_message):
          Called when an authentication error was received, i.e. that the
          password is invalid OR the server uses an auth method not in the
          `methods` whitelist. The `error_message` will tell you which it is.
        * server_message(self, message):
          A line of text from the Minecraft server was received.
        """
        self.handlers[event] = handler


    def _event(self, event, *args):
        """Call an event handler."""
        if event in self.handlers:
            self.handlers[event](self, *args)


    def connect(self):
        """Establishes the connection to the minecraft-control server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def start(self):
        """Start an infinite loop of `do_one_loop()`"""
        while self.do_one_loop():
            time.sleep(0.01)


    def do_one_loop(self):
        """Perform a single event loop with the server."""
        data = self.sock.recv(4192)
        if data == "":
            self.say("The server has gone away!")
            self.sock.close()

            # Reset the state.
            self.auth_method = None
            self.authed      = False
            self.challenge   = None
            return False

        data = data.strip()
        self.say("<<< {}".format(data))

        # Are we authed yet?
        if not self.authed:
            # Look for the auth method packet.
            if data.startswith("AUTH_METHOD"):
                fields = data.split(" ")
                if len(fields) > 1: # sanity test
                    auth_method = fields[1]

                    # Is the auth method acceptable?
                    if type(self.methods) == list:
                        if not auth_method in self.methods:
                            # Not ok!
                            error = "Server is using an auth method that we aren't allowing: {}".format(auth_method)
                            self.say(error)
                            self._event("auth_error", error)
                            return False

                    # Store the auth method used.
                    self.auth_method = auth_method

                    # Is there a challenge?
                    if len(fields) >= 3:
                        self.challenge = fields[2]

                    # Send the password.
                    self._send_auth()

            elif data.startswith("AUTH_OK"):
                # Password accepted!
                self.authed = True
                self._event("auth_ok")

            elif data.startswith("AUTH_ERROR"):
                # Password error!
                self._event("auth_error", "Password not accepted by server.")
        else:
            # We're in!
            self._event("server_message", data)

        return True


    def sendline(self, line):
        """Send a line of text to the server, with an implied line feed ending."""
        self.say(">>> {}".format(line))
        self.sock.send("{}\n".format(line))


    def send(self, text):
        """Send a raw message to the server. No line ending is added."""
        self.say(">>> {}".format(text))
        self.sock.send(text)


    def _send_auth(self):
        """Send the AUTH packet to log in."""
        response = None

        if self.auth_method == "plain":
            response = self.password
        elif self.auth_method == "hmac-md5":
            response = md5(self.challenge + md5(self.password))
        elif self.auth_method == "hmac-sha1":
            response = sha1(self.challenge + sha1(self.password))
        else:
            raise Exception("Server is using unsupported auth method: {}".format(self.auth_method))

        self.sendline("AUTH {}".format(response))