#!/bin/sh
set -e

python3 migrate.py
exec python3 src/main.py
