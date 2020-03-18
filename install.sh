#!/bin/bash

git pull origin master

module load Python/3.8.2-gimkl-2020a
pip3 install --user slackclient

if [ ! -f "config.json" ]; then
    echo `{"api_token":"","maintainers":{},"channel":"","path":"/log.txt"}` > "config.json"
fi
