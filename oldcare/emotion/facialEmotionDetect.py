# -*- coding: utf-8 -*-
'''
陌生人识别模型和情感分析模型的结合的主程序

用法：

'''
from cv2 import CAP_FFMPEG
from keras.engine.saving import model_from_json

from oldcare.Enum import Stream
# 导入包
from oldcare.facial import FaceUtil
from keras.preprocessing.image import img_to_array
import cv2
import time
import numpy as np
import os
import imutils
from oldcare.msgQueue import send_message_to_process

# 全局变量
facial_recognition_model_path = 'Model/face_recognition_hog.pickle'
facial_expression_model_path = 'Model/face_expression.json'
facial_expression_model_weights_path = 'Model/face_expression_weights.h5'

output_stranger_path = 'supervision/strangers'
output_smile_path = 'supervision/emotion/smile'
output_sad_path = 'supervision/emotion/sad'

label_mapping = {0: 'Happy', 1: 'Neutral', 2: 'Sad'}

skip_interval = 5

# 全局常量
FACIAL_EXPRESSION_TARGET_WIDTH = 28
FACIAL_EXPRESSION_TARGET_HEIGHT = 28

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 360

# 控制陌生人检测
strangers_timing = 0  # 计时开始
strangers_start_time = 0  # 开始时间
strangers_limit_time = 2  # if >= 2 seconds, then he/she is a stranger.

# 控制情感分析
facial_expression_timing = 0  # 计时开始
facial_expression_start_time = 0  # 开始时间
facial_expression_limit_time = 2  # if >= 2 seconds, he/she is smiling


def facial_expression_analysis(video_type,src):
    # 得到当前时间
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))
    print('[INFO] %s 陌生人检测程序和表情检测程序启动了.' % current_time)
    # 初始化摄像头
    # FPS calculation variables
    start_time = time.time()
    last_capture_stronger_time=time.time()
    last_capture_smile_time=time.time()
    last_capture_sad_time=time.time()

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

    # 初始化人脸识别模型
    faceUtil = FaceUtil(facial_recognition_model_path)
    # Load the model architecture from JSON file
    json_file = open(facial_expression_model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # Load the model weights
    loaded_model.load_weights(facial_expression_model_weights_path)

    # Compile the loaded model (if required)
    loaded_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    print('[INFO] 开始检测陌生人和表情...')
    # 不断循环
    counter = 0
    while True:
        counter += 1
        # grab the current frame
        (grabbed, frame) = vs.read()

        if counter % skip_interval != 0:
            continue

        # if we are viewing a video and we did not grab a frame, then we
        # have reached the end of the video
        if video_type == Stream.VIDEO and not grabbed:
            break

        if video_type == Stream.CAM:
            frame = cv2.flip(frame, 1)

        frame = imutils.resize(frame, width=VIDEO_WIDTH,
                               height=VIDEO_HEIGHT)  # 压缩，加快识别速度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale，情感分析

        face_location_list, names, categories = faceUtil.get_face_location_and_name(frame)

        # 处理每一张识别到的人脸
        for ((left, top, right, bottom), name, category) in zip(face_location_list,
                                                                names,
                                                                categories):

            # 将人脸框出来
            rectangle_color = (0, 0, 0)
            if category == 'old_people':
                rectangle_color = (255, 0, 0)
            elif category == 'employee':
                rectangle_color = (128, 128, 128)
            elif category == 'volunteer':
                rectangle_color = (0, 255, 0)
            else:
                rectangle_color = (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom),
                          rectangle_color, 2)

            # 陌生人检测逻辑
            if 'Unknown' in names:  # alert
                if strangers_timing == 0:  # just start timing
                    strangers_timing = 1
                    strangers_start_time = time.time()
                else:  # already started timing
                    strangers_end_time = time.time()
                    difference = strangers_end_time - strangers_start_time

                    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.localtime(time.time()))

                    if difference < strangers_limit_time:
                        print('[INFO] %s, 房间, 陌生人仅出现 %.1f 秒. 忽略.'
                              % (current_time, difference))
                    else:  # strangers appear
                        event_desc = '陌生人出现!!!'
                        invasion_msg = {
                            "event_date": current_time,
                            "event_type:": "Stranger Invasion!!!!",
                            "event_desc": '%s, 陌生人出现!!!' % current_time,
                            "event_img": output_stranger_path
                        }
                        print('[EVENT] %s, 陌生人出现!!!'
                              % current_time)
                        if time.time() - last_capture_stronger_time > 5:
                            send_message_to_process(invasion_msg)
                            cv2.imwrite(os.path.join(output_stranger_path,
                                                     'snapshot_%s.jpg'
                                                     % (time.strftime('%Y%m%d_%H%M%S'))), frame)
                            last_capture_stronger_time=time.time()
            else:
                # everything is ok
                strangers_timing = 0

            # 表情检测逻辑
            # 如果不是陌生人，且对象是老人
            if name != 'Unknown' and category == 'old_people':
                # 表情检测逻辑
                roi = gray[top:bottom, left:right]
                roi = cv2.resize(roi, (FACIAL_EXPRESSION_TARGET_WIDTH,
                                       FACIAL_EXPRESSION_TARGET_HEIGHT))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # determine facial expression
                predictions = loaded_model.predict(roi)
                label = np.argmax(predictions[0])
                facial_expression_label = label_mapping[label]

                if facial_expression_label == 'Happy':  # alert
                    if facial_expression_timing == 0:  # just start timing
                        facial_expression_timing = 1
                        facial_expression_start_time = time.time()
                    else:  # already started timing
                        facial_expression_end_time = time.time()
                        difference = facial_expression_end_time - facial_expression_start_time

                    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.localtime(time.time()))
                    if difference < facial_expression_limit_time:
                        print('[INFO] %s, 房间, %s仅笑了 %.1f 秒. 忽略'
                              % (current_time,
                                 name, difference))
                    else:  # he/she is really smiling
                        event_desc = '%s正在笑' % name
                        print('[EVENT] %s, 房间, %s正在笑.'
                              % (current_time, name))
                        smile_msg = {
                            "event_date": current_time,
                            "event_type:": "Smile",
                            "event_desc": ' %s,  %s正在笑.'
                                          % (current_time, name),
                            "event_img": output_smile_path
                        }
                        if time.time()-last_capture_smile_time>5:
                            send_message_to_process(smile_msg)
                            cv2.imwrite(os.path.join(output_smile_path,
                                                     'snapshot_%s.jpg'
                                                     % (time.strftime('%Y%m%d_%H%M%S'))), frame)
                            last_capture_smile_time=time.time()

                elif facial_expression_label == 'Sad':
                    if facial_expression_timing == 0:  # just start timing
                        facial_expression_timing = 1
                        facial_expression_start_time = time.time()
                    else:  # already started timing
                        facial_expression_end_time = time.time()
                        difference = facial_expression_end_time - facial_expression_start_time

                    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.localtime(time.time()))
                    if difference < facial_expression_limit_time:
                        print('[INFO] %s,  %s仅伤心了 %.1f 秒. 忽略'
                              % (current_time,
                                 name, difference))
                    else:  # he/she is really smiling
                        event_desc = '%s正在笑' % name
                        print('[EVENT] %s,  %s正在伤心.'
                              % (current_time, name))
                        sad_msg = {
                            "event_date": current_time,
                            "event_type:": "Sad",
                            "event_desc": ' %s,  %s正在伤心.'
                                          % (current_time, name),
                            "event_img": output_sad_path
                        }
                        if time.time()-last_capture_sad_time>5:
                            send_message_to_process(sad_msg)
                            cv2.imwrite(os.path.join(output_sad_path,
                                                     'snapshot_%s.jpg'
                                                     % (time.strftime('%Y%m%d_%H%M%S'))), frame)
                            last_capture_sad_time=time.time()
                else:  # everything is ok
                    facial_expression_timing = 0

            else:  # 如果是陌生人，则不检测表情
                facial_expression_label = ''

            # 人脸识别和情感分析都结束后，把表情和人名写上
            # (同时处理中文显示问题)

            final_label = name + ': ' + facial_expression_label
            cv2.putText(frame, final_label, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 0, 255), 2)

            # Calculate and display FPS
            elapsed_time = time.time() - start_time
            fps = counter / elapsed_time
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # show our detected faces along with smiling/not smiling labels
            cv2.imshow("Checking Strangers and Ole People's Face Expression",
                       frame)

        # Press 'ESC' for exiting video
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    # cleanup the camera and close any open windows
    vs.release()
    cv2.destroyAllWindows()
