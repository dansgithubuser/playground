gst-launch-1.0 v4l2src ! videoconvert ! x264enc ! matroskamux ! filesink location=test.mkv
