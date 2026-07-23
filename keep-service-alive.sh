#!/usr/bin/env bash

while true; do
  curl -s https://cashola.onrender.com/ > /dev/null
  echo "$(date  '+%Y-%m-%dT%H:%M:%S') Ping sent!"
  sleep 900
done
