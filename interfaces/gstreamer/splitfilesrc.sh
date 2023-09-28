# This has the same problem as multifilesrc.
# The docs show this being used with videos, though.
gst-launch-1.0 splitfilesrc location='test*.mkv' ! matroskademux ! h264parse ! avdec_h264 ! videoconvert ! xvimagesink
