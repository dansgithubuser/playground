# Frames are missing from the beginning of the 2nd vid.
# Is it "playing" both at the same time?
# This is maybe supposed to be used with images rather than videos?
gst-launch-1.0 multifilesrc location='test%d.mkv' ! matroskademux ! h264parse ! avdec_h264 ! videoconvert ! xvimagesink
