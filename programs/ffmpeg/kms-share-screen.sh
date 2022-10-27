# appropriate in Ubuntu 22 with Wayland
# requires rtsp-server.py running
sudo ffmpeg -f kmsgrab -i - -vf 'hwmap=derive_device=vaapi,hwdownload,format=bgr0' -f rtsp -muxdelay 0.1 rtsp://localhost:8554/screen
