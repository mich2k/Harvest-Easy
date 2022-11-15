#!/bin/bash

echo BEGIN DEL
sudo docker rm -vf $(sudo docker ps -aq)
sudo docker rmi -f $(sudo docker images -aq)
echo OK
