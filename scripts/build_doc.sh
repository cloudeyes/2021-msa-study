#!/bin/sh
git checkout docs
cd src/doc
make clean
make -W -b html
git checkout main
