gst-launch-1.0 filesrc location=test.mkv ! matroskademux ! h264parse ! avdec_h264 ! videoconvert ! xvimagesink
