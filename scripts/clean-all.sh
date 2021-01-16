#!/bin/sh
find . -type d \( -name 'debug' -o -name 'Debug' -o -name '__pycache__' -o -name '.mypy_cache' -o -name '.pytest_cache' -o -name 'node_modules' \) -exec rm -rf {} \; > /dev/null
