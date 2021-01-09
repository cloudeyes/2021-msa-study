#!/bin/sh

docker container kill microlab
docker container rm microlab
docker image rm cloudeyes/micropy-lab:3.9
docker system prune -f
