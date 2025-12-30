#!/bin/bash

if ! command -v blueutil &> /dev/null; then
    sketchybar --set "$NAME" icon="󰂲" label="N/A"
    exit 0
fi

BT_POWER=$(blueutil -p)

if [ "$BT_POWER" = "1" ]; then
  CONNECTED_DEVICES=$(blueutil --connected 2>/dev/null)

  if [ -n "$CONNECTED_DEVICES" ]; then
    ICON="󰂱"
    COUNT=$(echo "$CONNECTED_DEVICES" | grep -c "address")
    LABEL="$COUNT"
  else
    ICON="󰂯"
    LABEL=""
  fi
else
  ICON="󰂲"
  LABEL=""
fi

sketchybar --set "$NAME" icon="$ICON" label="$LABEL"
