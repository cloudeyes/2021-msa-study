#!/bin/sh
docker run -d --name microlab --hostname microlab -p 12222:22 -p 18888:8888 -v /home/ykkim/install:/users/smprc/install -v /home/ykkim/notebooks:/users/smprc/notebooks cloudeyes/micropy-lab:3.9
