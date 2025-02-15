#!/bin/bash

disk_usage=$(df -h / | awk 'NR==2 {print $3 "/" $2}')

