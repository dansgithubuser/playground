# appropriate in Ubuntu 22 with Wayland
touch output.mkv
sudo ffmpeg -y -f kmsgrab -i - -vf 'hwmap=derive_device=vaapi,hwdownload,format=bgr0' output.mkv
