gst-launch-1.0 -e v4l2src ! video/x-raw,width=800,height=600 ! queue \
! videoconvert \
! v4l2h264enc extra-controls=encode,video_bitrate=640000 ! video/x-h264,level='(string)4' \
! h264parse ! queue \
! mpegtsmux ! filesink location=test2.ts
