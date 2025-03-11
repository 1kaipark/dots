#!/bin/bash

# Fetch weather data in JSON format
weather_data=$(curl -s "https://wttr.in/?format=j1")

# Extract the required fields using jq
weather_code=$(echo "$weather_data" | jq -r '.current_condition[0].weatherCode')
temp_C=$(echo "$weather_data" | jq -r '.current_condition[0].temp_C')
description=$(echo "$weather_data" | jq -r '.current_condition[0].weatherDesc[0].value')

# Output the results
echo "$weather_code|$temp_C|$description"
