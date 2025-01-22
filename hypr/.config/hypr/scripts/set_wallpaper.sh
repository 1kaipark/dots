set_wallpaper() {
  swww img "$1" \
    --transition-bezier .43,1.19,1,.4 \
    --transition-fps 60 \
    --transition-type "grow" \
    --transition-duration 0.7 \
    --invert-y \
    --transition-pos "$(hyprctl cursorpos)"
}

set_wallpaper "$1"
