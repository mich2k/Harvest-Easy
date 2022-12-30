#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <image_name>"

else
source delete_all.sh
source build.sh $1
fi
