#!/usr/bin/python3

import sys
from pathlib import Path

config = None

if len(sys.argv) == 1 :
    print("No config file provided. Exiting.")
    sys.exit(1)
else : config = Path(str(sys.argv[1]))

try :
    config = open(config)
except FileNotFoundError :
    print("Config file not found. Exiting.")
    sys.exit(1)

while 