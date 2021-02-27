#!/bin/bash

mkdir -p /home/$USER/.local/share/signal-cli/phonebook

FILE=/home/$USER/.local/share/signal-cli/phonebook/phonebook.json

# check if phonebook file already exists - if not, open editor (nano) to insert numbers and names,
# {"<+49number>": "<name_shorthand>", "<number2>": "<name2_shorthand>"}

if test -f "$FILE"; then
  echo "$FILE exists already."
else
  echo "{" > $FILE
  echo "  \"+491234567\": \"<name here>\"," >> $FILE
  echo "  \"+493456789\": \"<name2 here>\"" >> $FILE
  echo "}" >> $FILE
  nano $FILE
fi
