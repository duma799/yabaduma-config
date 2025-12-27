#!/bin/bash
# battery.sh - Battery Status Plugin for SketchyBar
#
# Description: Displays battery percentage with dynamic icon
# Dependencies: None (uses built-in macOS pmset)
# Update Frequency: Every 120 seconds

# Get battery percentage with validation
PERCENTAGE=$(pmset -g batt | grep -Eo '[0-9]+%' | head -1 | tr -d '%')
PERCENTAGE=${PERCENTAGE:-0}  # Default to 0 if empty

CHARGING=$(pmset -g batt | grep 'AC Power')

case "${PERCENTAGE}" in
  9[0-9]|100) ICON=""
  ;;
  [6-8][0-9]) ICON=""
  ;;
  [3-5][0-9]) ICON=""
  ;;
  [1-2][0-9]) ICON=""
  ;;
  *) ICON=""
esac

if [[ -n "$CHARGING" ]]; then
  ICON=""
fi

sketchybar --set "$NAME" icon="$ICON" label="${PERCENTAGE}%"
