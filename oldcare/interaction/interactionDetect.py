# -*- coding: utf-8 -*-
'''
义工是否和老人有互动主程序

用法： 
python testingvolunteeractivity.py
python testingvolunteeractivity.py --filename tests/desk_01.mp4
'''
import os
from cv2 import CAP_FFMPEG
from oldcare.facial import FaceUtil
from scipy.spatial import distance as dist
from oldcare.msgQueue import send_message_to_process
from oldcare.Enum import globalEnum, Stream
import cv2
import time
import imutils

model_path = 'Model/face_recognition_hog.pickle'
output_activity_path = 'supervision/activity'
FACE_ACTUAL_WIDTH = 20  # cm
VIDEO_WIDTH = 320
VIDEO_HEIGHT = 180
ACTUAL_DISTANCE_LIMIT = 100  # cm


def draw_face_labels(frame, face_location_list, names, categories):
    for ((left, top, right, bottom), name, category) in zip(face_location_list, names, categories):
        person_type = category
        rectangle_color = (0, 0, 0)
        if person_type == 'old_people':
            rectangle_color = (255, 0, 0)
        elif person_type == 'employee':
            rectangle_color = (128, 128, 128)
        elif person_type == 'volunteer':
            rectangle_color = (0, 255, 0)
        else:
            rectangle_color = (255, 0, 0)

        text = f"{name} ({category})"
        cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)


def detect_volunteer_interaction(path, video_type, src):
    pixel_per_met0ric = None

    # FPS calculation variables
    start_time = time.time()

    if video_type == Stream.CAM:
        vs = cv2.VideoCapture(0)
        time.sleep(2)
    elif video_type == Stream.URL:
        vs = cv2.VideoCapture(src, CAP_FFMPEG)
        time.sleep(2)
    elif video_type == Stream.VIDEO:
        vs = cv2.VideoCapture(src)
    else:
        quit()

    skip_interval = 5
    faceUtil = FaceUtil(path)
    last_capture_time = time.time() - 30

    print('[INFO] 开始检测义工和老人是否有互动...')
    counter = 0
    while True:
        counter += 1
        (grabbed, frame) = vs.read()
        counter += 1
        if counter % skip_interval != 0:
            continue

        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_location_list, names, categories = faceUtil.get_face_location_and_name(gray_frame)

        volunteer_centroids = [((right + left) // 2, (top + bottom) // 2) for
                               ((left, top, right, bottom), name, category) in
                               zip(face_location_list, names, categories) if category == 'volunteer']
        volunteer_name = [name for name, category in zip(names, categories) if category == 'volunteer']
        old_people_centroids = [((right + left) // 2, (top + bottom) // 2) for
                                ((left, top, right, bottom), name, category) in
                                zip(face_location_list, names, categories) if category == 'old_people']
        old_people_name = [name for name, category in zip(names, categories) if category == 'old_people']

        draw_face_labels(frame, face_location_list, names, categories)

        for i in volunteer_centroids:
            for j_index, j in enumerate(old_people_centroids):
                pixel_distance = dist.euclidean(i, j)
                face_pixel_width = sum([i[2] - i[0] for i in face_location_list]) / len(face_location_list)
                pixel_per_metric = face_pixel_width / FACE_ACTUAL_WIDTH
                actual_distance = pixel_distance / pixel_per_metric

                if actual_distance < ACTUAL_DISTANCE_LIMIT:
                    cv2.line(frame, (int(i[0]), int(i[1])), (int(j[0]), int(j[1])), (255, 0, 255), 2)
                    label = 'distance: %dcm' % actual_distance
                    cv2.putText(frame, label, (frame.shape[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    print(
                        f'[EVENT] {current_time}, {old_people_name[j_index]} 正在与 {volunteer_name[j_index]} 义工交互.')
                    if time.time() - last_capture_time > 5:
                        interaction_msg = {"old_people": old_people_name[j_index],
                                           "volunteer": volunteer_name[j_index],
                                           "event_date": current_time,
                                           "event_type:": "interaction",
                                           "event_desc": f' {current_time}, {old_people_name[j_index]} '
                                                         f'正在与 {volunteer_name[j_index]} 义工交互.',
                                           "event_img":output_activity_path
                                           }
                        send_message_to_process(interaction_msg)
                        cv2.imwrite(
                            os.path.join(output_activity_path, 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                            frame)
                        last_capture_time = time.time()
                # Calculate and display FPS
        elapsed_time = time.time() - start_time
        fps = counter / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Checking Strangers and Ole People's Face Expression",
                   frame)

        # Press 'ESC' for exiting video
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    # cleanup the camera and close any open windows
    vs.release()
    cv2.destroyAllWindows()

