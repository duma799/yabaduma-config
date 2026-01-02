#!/bin/bash

hex_to_argb() {
    local hex="${1#\#}"
    echo "0xff${hex}"
}

lighten_hex() {
    local hex="${1#\#}"
    local amount="${2:-20}"
    local r=$((16#${hex:0:2}))
    local g=$((16#${hex:2:2}))
    local b=$((16#${hex:4:2}))
    r=$(( r + amount > 255 ? 255 : r + amount ))
    g=$(( g + amount > 255 ? 255 : g + amount ))
    b=$(( b + amount > 255 ? 255 : b + amount ))
    printf "0xff%02x%02x%02x" $r $g $b
}

if [ -f ~/.cache/wal/colors.sh ]; then
    source ~/.cache/wal/colors.sh

    export BAR_COLOR=$(hex_to_argb "$background")
    export ITEM_BG_COLOR=$(hex_to_argb "$background")
    export ACCENT_COLOR=$(hex_to_argb "$color1")
    export ICON_COLOR=$(hex_to_argb "$color4")
    export LABEL_COLOR=$(hex_to_argb "$color6")
    export POPUP_BACKGROUND_COLOR=$(hex_to_argb "$background")
    export POPUP_BORDER_COLOR=$(hex_to_argb "$color1")
    export SHADOW_COLOR="0x80000000"
else
    export BAR_COLOR="0x00000000"
    export ITEM_BG_COLOR="0xf01e3a5f"
    export ACCENT_COLOR="0xff5f87af"
    export ICON_COLOR="0xffDFE5F3"
    export LABEL_COLOR="0xffDFE5F3"
    export POPUP_BACKGROUND_COLOR="0xff1e3a5f"
    export POPUP_BORDER_COLOR="0xff5f87af"
    export SHADOW_COLOR="0x80000000"
fi
