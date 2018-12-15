#!/bin/python3

import os, socket, sys

if len(sys.argv) > 1 :
    if sys.argv[1] == "-h" or sys.argv[1] == "--help" :
        print(
"""Usage: servmond-query TARGET COMMAND
                 
TARGET:   The machine servmond is monitoring
COMMAND:  The cached ssh command to query""")
        exit(0)

if len(sys.argv) < 3 :
    print("Please specify a target machine as well as a command.")
    sys.exit(1)
else :
    machine = str(sys.argv[1])
    command = str(sys.argv[2])

server_address = '/tmp/servmond_' + machine

connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try :
    connection.connect(server_address)
    connection.sendall((command + "\n").encode('utf-8'))
    print(connection.makefile().readline().strip())
except :
    print("Connection to daemon failed. Invalid target machine?")
    exit(1)