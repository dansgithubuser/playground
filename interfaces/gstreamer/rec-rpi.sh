gst-launch-1.0 -e libcamerasrc ! queue \
! v4l2convert \
! v4l2h264enc extra-controls=encode,video_bitrate=640000 ! video/x-h264,level='(string)4' \
! h264parse ! queue \
! mpegtsmux ! filesink location=test.ts

# check v4l2-ctl -d 11 --list-ctrls-menu for what to put in h264 encode extra-controls
