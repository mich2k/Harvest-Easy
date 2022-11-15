#!/bin/bash

echo $0

if [ $# -ne 1 ]; then
    echo "Usage: $0 <image_name>"

else

img=$1
tag=latest


echo STOP BEGIN
sudo docker stop $(sudo docker ps -aq)
echo STOP DONE

echo BUILD BEGIN
sudo docker build -t $img:$tag .
echo BUILD DONE


echo RUN BEGIN
sudo docker run -d -p 5000:5000 $img:$tag
echo RUN DONE


fi


