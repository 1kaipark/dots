#!/bin/bash 

echo $(pacman -Qq | wc -l)
