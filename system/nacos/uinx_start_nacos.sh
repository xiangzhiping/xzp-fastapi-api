#!/bin/bash

NACOS_BIN_DIR="/opt/nacos/bin"

cd "$NACOS_BIN_DIR" || { echo "?????????? $NACOS_BIN_DIR"; exit 1; }

./startup.sh -m standalone


