#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: TEAMR_to_FC.sh [filename]"
    exit 1
fi
   
curl --location --request POST 'https://filereceiver.cwb.gov.tw/api/file' \
--header 'Content-Type: multipart/form-data' \
--form 'username=precip' \
--form 'apikey=e860d5ea77ba4a7b218a992a01520917' \
--form 'vdir=/precip/TEAMR' \
--form 'upload_file=@/home/disk/monsoon/precip/radar/TEAM-R/forCatalog/'$1
