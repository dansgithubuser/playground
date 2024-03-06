gst-launch-1.0 libcamerasrc ! queue ! v4l2convert ! v4l2h264enc ! video/x-h264,level='(string)4' ! h264parse ! queue ! mpegtsmux ! filesink location=test.ts
