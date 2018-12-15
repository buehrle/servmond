#!/bin/python3

import os, socket, sys

if len(sys.argv) == 1 :
    print("Please specify a command.")
    sys.exit(1)
else : command = str(sys.argv[1])

server_address = '/tmp/servmond'

connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try :
    connection.connect(server_address)
    connection.sendall((command + "\n").encode('utf-8'))
    print(connection.makefile().readline().strip())
except :
    print("Connection to daemon failed.")
    exit(1)