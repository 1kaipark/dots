#!/bin/bash 

quotes=$(curl -s "https://zenquotes.io/api/quotes")
quote=$(echo "$quotes" | jq -r '.[0]')
body=$(echo "$quote" | jq -r '.q')
author=$(echo "$quote" | jq -r '.a')


echo "'$body' - $author"

