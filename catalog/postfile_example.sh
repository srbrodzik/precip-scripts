curl --location --request POST 'https://filereceiver.cwb.gov.tw/api/file' \
--header 'Content-Type: multipart/form-data' \
--form 'username=account' \
--form 'apikey=asdgjkl234wer98dsjklsddf' \
--form 'vdir=/test' \
--form 'upload_file=@/file/path/test.txt'
