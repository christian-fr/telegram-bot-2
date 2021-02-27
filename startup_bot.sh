#!/bin/bash

cd "$(dirname "$0")"

./kill_bot.sh

/usr/bin/python3 signalBot.py & echo "$!" > /tmp/signal-bot.pid

