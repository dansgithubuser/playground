# This works!
gst-launch-1.0 splitmuxsrc location='test*.mkv' ! decodebin ! videoconvert ! xvimagesink
