#!/bin/bash

export WEATHER_API_KEY=""
export LATITUDE=""
export LONGITUDE=""
export CITY_ID=""

export FONT_FILE=""

cd "$(dirname "$0")"

./kill_bot.sh
/usr/bin/python3.6 startup_bot.py & echo "$!" > /tmp/telegram-bot.pid

