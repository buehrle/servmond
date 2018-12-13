#!/usr/bin/python3

import sys, os, time, atexit, socket
from subprocess import run, PIPE
from pathlib import Path
from threading import Thread

config = None

settings = {"interval":"10",
            "user":"",
            "server":""}

commands = {}

results = {}

stop = False

def query_worker() :
    global results

    while not stop :
        print("ssh " + settings["user"] + "@" + settings["server"] + " " + command_list)
        p = run("ssh " + settings["user"] + "@" + settings["server"] + " " + command_list, shell=True, stdout=PIPE, encoding='utf-8')

        for num, result in enumerate(p.stdout.split("\n")) :
            results[list(commands.keys())[num]] = result
        time.sleep(int(settings["interval"]))

def cleanup() :
    global stop
    stop = True

atexit.register(cleanup)

if len(sys.argv) == 1 :
    print("No config file provided. Exiting.")
    sys.exit(1)
else : config = Path(str(sys.argv[1]))

try :
    config = open(config)
except FileNotFoundError :
    print("Config file not found. Exiting.")
    sys.exit(1)

print("Parsing config file...")

config_line = config.readline()

while config_line :
    args = config_line.split(None, 2)
    if args[0] == "cmd" :
        commands[args[1]] = args[2]
    else :
        settings[args[0]] = args[1]
    config_line = config.readline()

print("Finished.")

command_list = ""

for command in commands.values() :
    command_list += command.strip() + "; "

Thread(target=query_worker).start()

server_address = '/tmp/servmond'

try :
    os.unlink(server_address)
except : None

print("Starting query daemon...")

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(server_address)
server.listen(1)

print("Started.")

while not stop :
    connection, address = server.accept()
    try :
        query = connection.makefile().readline().strip()
        if query in results :
            connection.sendall((results[query] + "\n").encode('utf-8'))
        elif query in commands:
            connection.sendall("Loading...".encode('utf-8'))
        else :
            connection.sendall("Command not specified.".encode('utf-8'))
    finally :
        connection.close()