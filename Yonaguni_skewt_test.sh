#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: test.sh [filename]"
    exit 1
fi
   
curl --location --request POST 'https://filereceiver.cwb.gov.tw/api/file' \
--header 'Content-Type: multipart/form-data' \
--form 'username=precip' \
--form 'apikey=e860d5ea77ba4a7b218a992a01520917' \
--form 'vdir=/precip/SkewT' \
--form 'upload_file=@/home/disk/meso-home/brodzik/PRECIP/DATA/soundings/csu/png/$1'
