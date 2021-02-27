#!/bin/bash

mkdir -p /home/$USER/.local/share/openweather/


FILE=/home/$USER/.local/share/openweather/openweather_config.json

# check if config file already exists - if not, open editor (nano) to insert api keys,
# latitude, longitude, city id

if test -f "$FILE"; then
  echo "$FILE exists already."
else
  echo "{" > /home/$USER/.local/share/openweather/openweather_config.json
  echo "  \"WEATHER_API_KEY\": \"<your openweather api key here>\"," >> /home/$USER/.local/share/openweather/openweather_config.json
  echo "  \"LATITUDE\": \"<latitude here>\"," >> /home/$USER/.local/share/openweather/openweather_config.json
  echo "  \"LONGITUDE\": \"<logitude here>\"," >> /home/$USER/.local/share/openweather/openweather_config.json
  echo "  \"CITY_ID\": \"<city id here>\"" >>/home/$USER/.local/share/openweather/openweather_config.json
  echo "}" >> /home/$USER/.local/share/openweather/openweather_config.json
  nano /home/$USER/.local/share/openweather/openweather_config.json
fi
