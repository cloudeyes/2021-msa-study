#!/bin/bash
set -m # turn on bash's job control
/usr/sbin/sshd -D &
sudo -u smprc /bin/bash -c "source ~/.bash_profile && conda activate lab && jupyter-lab"
fg %1

