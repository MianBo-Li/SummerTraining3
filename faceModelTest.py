# -*- coding: utf-8 -*-
'''
测试人脸识别模型

用法：
python testingfacerecognition.py
python testingfacerecognition.py --filename room_01.mp4
'''
from cv2 import CAP_FFMPEG

# import the necessary packages
from oldcare.facial import FaceUtil
import imutils
import cv2
import time
import argparse

# FPS calculation variables
start_time = time.time()
frame_counter = 0

# 全局变量
facial_recognition_model_path = 'Model/face_recognition_hog.pickle'
# url = 'rtmp://114.116.242.87:1985/live/test'
url = None
# 初始化摄像头
if not url:
    # vs = cv2.VideoCapture(url, CAP_FFMPEG)
    vs = cv2.VideoCapture(0)
    time.sleep(2)
else:
    vs = cv2.VideoCapture(url,CAP_FFMPEG)

# 初始化人脸识别模型
faceutil = FaceUtil(facial_recognition_model_path)

font_path = 'font/Yahei.ttf'

font = cv2.FONT_HERSHEY_TRIPLEX

# 不断循环
while True:
    # grab the current frame
    (grabbed, frame) = vs.read()

    # if we are viewing a video, and we did not grab a frame, then we
    # have reached the end of the video
    if url and not grabbed:
        break

    if not url:
        frame = cv2.flip(frame, 1)

    # resize the frame, convert it to grayscale, and then clone the
    # original frame, so we can draw on it later in the program
    frame = imutils.resize(frame, width=600)

    face_location_list, names, categories = faceutil.get_face_location_and_name(frame)

    # loop over the face bounding boxes
    for ((left, top, right, bottom), name, category) in zip(
            face_location_list,
            names,
            categories):
        # display label and bounding box rectangle on the output frame
        text = f"{name} ({category})"
        cv2.putText(frame, text, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 0, 255), 2)

    # Calculate and display FPS
    frame_counter += 1
    elapsed_time = time.time() - start_time
    fps = frame_counter / elapsed_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # show our detected faces along with labels
    cv2.imshow("Face Recognition", frame)

    # Press 'ESC' for exiting video
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()
