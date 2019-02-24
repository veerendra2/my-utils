#!/bin/bash
# Author: Veerendra Kakumanu
# Description: A simple tool to removes all docker containers and docker images

sudo docker rm -f `docker ps -a | tail -n+2 | awk '{print $1}'`
sudo docker rmi -f `docker images | tail -n+2 | awk '{print $1}'`
