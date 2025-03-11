# #!/bin/bash
# 
# wallpapers="$HOME/Pictures/wall/"
# # monitors="$(hyprctl monitors | grep Monitor | awk '{print $2}')"
# monitors="$(xrandr --query | grep " connected" | awk '{print $1}')"
# 
# for monitor in $monitors; do
#   wallpaper="$(find $wallpapers -type f | shuf -n 1)"
#   echo "$monitor, $wallpaper"
#   swww img -o "$monitor" --transition-duration 0.3 --transition-type grow --transition-fps 60 "$wallpaper"
# done
#
#
# Chatgpt cuz fuk bash scripting xd
#
#
#!/bin/bash

wallpapers="$HOME/Pictures/wall/"
history_file="/tmp/swww_last_wallpaper"
monitors="$(xrandr --query | grep " connected" | awk '{print $1}')"

# Load the last used wallpaper if the file exists
if [[ -f "$history_file" ]]; then
  last_wallpaper=$(cat "$history_file")
else
  last_wallpaper=""
fi

# Get all wallpapers
all_wallpapers=($(find "$wallpapers" -type f))

for monitor in $monitors; do
  # Pick a random wallpaper that is not the same as the last one
  wallpaper="$last_wallpaper"
  while [[ "$wallpaper" == "$last_wallpaper" ]]; do
    wallpaper="${all_wallpapers[RANDOM % ${#all_wallpapers[@]}]}"
  done

  echo "$monitor, $wallpaper"
  swww img -o "$monitor" --transition-duration 0.3 --transition-type grow --transition-fps 60 "$wallpaper"

  # Save the wallpaper to history
  echo "$wallpaper" > "$history_file"
done
