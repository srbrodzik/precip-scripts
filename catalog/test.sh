#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Usage: test.sh [filename]"
    exit 1
fi
   
echo "file = $1";
