#!/bin/bash

# Get Bluetooth power status (1 = on, 0 = off)
BT_POWER=$(blueutil -p)

if [ "$BT_POWER" = "1" ]; then
  # Bluetooth is ON - check for connected devices
  CONNECTED_DEVICES=$(blueutil --connected 2>/dev/null)

  if [ -n "$CONNECTED_DEVICES" ]; then
    # Devices are connected
    ICON="󰂱"  # Bluetooth connected icon
    # Count connected devices
    COUNT=$(echo "$CONNECTED_DEVICES" | grep -c "address")
    LABEL="$COUNT"
  else
    # Bluetooth on but no devices connected
    ICON="󰂯"  # Bluetooth on icon
    LABEL=""
  fi
else
  # Bluetooth is OFF
  ICON="󰂲"  # Bluetooth off icon
  LABEL=""
fi

sketchybar --set $NAME icon="$ICON" label="$LABEL"
