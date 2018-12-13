#!/usr/bin/python3

import sys, os, time, atexit
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
        p = run("ssh " + settings["user"] + "@" + settings["server"] + " '" + command_list + "'", shell=True, stdout=PIPE, encoding='ascii')

        for num, result in enumerate(p.stdout.split()) :
            results[list(commands.keys())[num]] = result
        print(results)
        time.sleep(int(settings["interval"]))

if len(sys.argv) == 1 :
    print("No config file provided. Exiting.")
    sys.exit(1)
else : config = Path(str(sys.argv[1]))

try :
    config = open(config)
except FileNotFoundError :
    print("Config file not found. Exiting.")
    sys.exit(1)

config_line = config.readline()

while config_line :
    args = config_line.split(None, 2)
    if args[0] == "cmd" :
        commands[args[1]] = args[2]
    else :
        settings[args[0]] = args[1]
    config_line = config.readline()

command_list = ""

for command in commands.values() :
    command_list += command.strip() + "; "

Thread(target=query_worker).start()

pipe_command_path = "/tmp/servmond_command"
pipe_result_path = "/tmp/servmond_result"

if not os.path.exists(pipe_command_path) :
    os.mkfifo(pipe_command_path)

if not os.path.exists(pipe_result_path) :
    os.mkfifo(pipe_result_path)

pipe_command = open(pipe_command_path, 'r')
pipe_result = None

while not stop :
    command = pipe_command.readline()
    pipe_result = open(pipe_result_path, 'w')
    pipe_result.write(results[command] + "\n")
    pipe_result.close()