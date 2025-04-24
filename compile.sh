#!/bin/sh


arg1=$1
arg2=$2
all_params="$*"
echo "All parameters as one string: $all_params"
g++ $all_params

