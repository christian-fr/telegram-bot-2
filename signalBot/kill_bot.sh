#!/bin/bash

pid=$(cat /tmp/signal-bot.pid)
if [ "$(ps -o comm= -p "$pid")" = "python3" ]; then
    kill $pid
else echo "signal-bot is dead!"
fi
