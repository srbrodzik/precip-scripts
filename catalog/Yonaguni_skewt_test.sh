#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: test.sh [filename]"
    exit 1
fi
   
curl --location --request POST 'https://filereceiver.cwb.gov.tw/api/file' \
--header 'Content-Type: multipart/form-data' \
--form 'username=account' \
--form 'apikey=asdgjkl234wer98dsjklsddf' \
--form 'vdir=/test' \
--form 'upload_file=@/home/snowband/brodzik/precip/raw/sounding_csu/png_images/$1'
