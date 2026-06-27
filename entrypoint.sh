#!/bin/sh

mkdir -p /config
mkdir -p /config/logs

if [ ! -f /config/tracearr_configuration.json ]; then
    cp /app/config/tracearr_configuration.json \
       /config/tracearr_configuration.json
fi

exec "$@"