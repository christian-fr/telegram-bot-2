#!/bin/bash

cd "$(dirname "$0")"

./kill_bot.sh

/usr/bin/python3 startup_bot.py & echo "$!" > /tmp/telegram-bot.pid

