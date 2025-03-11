#!/bin/bash

echo $(uptime -p | sed -e 's/up //;s/ hours,/h/;s/ hour,/h/;s/ minutes/m/;s/ minute/m/;s/ days,/d/;s/ day,/d/')
