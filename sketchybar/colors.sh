#!/bin/bash

hex_to_argb() {
    local hex="${1#\#}"
    echo "0xff${hex}"
}

if [ -f ~/.cache/wal/colors.sh ]; then
    source ~/.cache/wal/colors.sh

    export BAR_COLOR=$(hex_to_argb "$background")
    export ITEM_BG_COLOR=$(hex_to_argb "$color0")
    export ACCENT_COLOR=$(hex_to_argb "$color1")
    export ICON_COLOR=$(hex_to_argb "$foreground")
    export LABEL_COLOR=$(hex_to_argb "$foreground")
    export POPUP_BACKGROUND_COLOR=$(hex_to_argb "$color0")
    export POPUP_BORDER_COLOR=$(hex_to_argb "$color8")
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
