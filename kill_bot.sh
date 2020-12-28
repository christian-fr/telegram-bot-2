#!/bin/bash

pid=$(cat /tmp/telegram-bot.pid)
if [ "$(ps -o comm= -p "$pid")" = "python3" ]; then
    kill $pid
else echo "telegram-bot is dead!"
fi
