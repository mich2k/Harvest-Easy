#!/bin/bash
echo STOP BEGIN
sudo docker stop $(sudo docker ps -aq)
echo STOP DONE

echo BUILD BEGIN
sudo docker build -t myflask:latest .
echo BUILD DONE


echo RUN BEGIN
sudo docker run -d -p 5000:5000 myflask:latest
echo RUN DONE
