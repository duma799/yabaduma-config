#!/bin/sh

if [ "$SENDER" = "front_app_switched" ]; then
  sketchybar --set "$NAME" icon=">" label="$INFO"
fi
