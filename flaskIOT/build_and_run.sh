#!/bin/bash
echo STOP BEGIN
sudo docker stop $(sudo docker ps -aq)
echo STOP DONE

echo BUILD BEGIN
sudo docker build -t mick2k1/iotflask:latest .
echo BUILD DONE

echo RUN BEGIN
sudo docker run --name iotproj -d -p 5000:5000 mick2k1/iotflask:latest
echo RUN DONE
