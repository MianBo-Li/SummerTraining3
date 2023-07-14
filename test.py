import cv2
import time
import threading
from keras.engine.saving import model_from_json
from keras.preprocessing.image import img_to_array
import numpy as np
import imutils
import os

from oldcare.facial import FaceUtil
from oldcare.msgQueue import send_message_to_process

# Global variables
facial_recognition_model_path = 'Model/face_recognition_hog.pickle'
facial_expression_model_path = 'Model/face_expression.json'
facial_expression_model_weights_path = 'Model/face_expression_weights.h5'
output_stranger_path = 'supervision/strangers'
output_smile_path = 'supervision/emotion/smile'
output_sad_path = 'supervision/emotion/sad'
label_mapping = {0: 'Happy', 1: 'Neutral', 2: 'Sad'}
skip_interval = 5
frame_count = 0
FACIAL_EXPRESSION_TARGET_WIDTH = 28
FACIAL_EXPRESSION_TARGET_HEIGHT = 28
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 360
strangers_timing = 0
strangers_start_time = 0
strangers_limit_time = 2
facial_expression_timing = 0
facial_expression_start_time = 0
facial_expression_limit_time = 2
src = 'rtmp://114.116.242.87:1985/live/test'
vs = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
time.sleep(2)
faceUtil = FaceUtil(facial_recognition_model_path)
json_file = open(facial_expression_model_path, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(facial_expression_model_weights_path)
frame_buffer=[]
BATCH_SIZE=16
loaded_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])


# Define a function for facial expression analysis
def facial_expression_analysis(frame, gray, face_location_list, names, categories):
    # FPS calculation variables
    frame_counter = 0
    start_time = time.time()
    for ((left, top, right, bottom), name, category) in zip(face_location_list, names, categories):
        rectangle_color = (0, 0, 0)
        if category == 'old_people':
            rectangle_color = (255, 0, 0)
        elif category == 'employee':
            rectangle_color = (128, 128, 128)
        elif category == 'volunteer':
            rectangle_color = (0, 255, 0)
        else:
            rectangle_color = (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)

        if 'Unknown' in names:
            if strangers_timing == 0:
                strangers_timing = 1
                strangers_start_time = time.time()
            else:
                strangers_end_time = time.time()
                difference = strangers_end_time - strangers_start_time
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if difference < strangers_limit_time:
                    print('[INFO] %s, 房间, 陌生人仅出现 %.1f 秒. 忽略.' % (current_time, difference))
                else:
                    event_desc = '陌生人出现!!!'
                    invasion_msg = {
                        "event_date": current_time,
                        "event_type:": "Stranger Invasion!!!!",
                        "event_desc": '%s, 陌生人出现!!!' % current_time,
                        "event_img": output_stranger_path
                    }
                    send_message_to_process(invasion_msg)
                    print('[EVENT] %s, 陌生人出现!!!' % current_time)
                    cv2.imwrite(
                        os.path.join(output_stranger_path, 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))), frame)
        else:
            strangers_timing = 0

        if name != 'Unknown' and category == 'old_people':
            roi = gray[top:bottom, left:right]
            roi = cv2.resize(roi, (FACIAL_EXPRESSION_TARGET_WIDTH, FACIAL_EXPRESSION_TARGET_HEIGHT))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            predictions = loaded_model.predict(roi)
            label = np.argmax(predictions[0])
            facial_expression_label = label_mapping[label]

            if facial_expression_label == 'Happy':
                if facial_expression_timing == 0:
                    facial_expression_timing = 1
                    facial_expression_start_time = time.time()
                else:
                    facial_expression_end_time = time.time()
                    difference = facial_expression_end_time - facial_expression_start_time

                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if difference < facial_expression_limit_time:
                    print('[INFO] %s, 房间, %s仅笑了 %.1f 秒. 忽略' % (current_time, name, difference))
                else:
                    event_desc = '%s正在笑' % name
                    print('[EVENT] %s, 房间, %s正在笑.' % (current_time, name))
                    smile_msg = {
                        "event_date": current_time,
                        "event_type:": "Smile",
                        "event_desc": ' %s,  %s正在笑.' % (current_time, name),
                        "event_img": output_smile_path
                    }
                    send_message_to_process(smile_msg)
                    cv2.imwrite(os.path.join(output_smile_path, 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                                frame)

            elif facial_expression_label == 'Sad':
                if facial_expression_timing == 0:
                    facial_expression_timing = 1
                    facial_expression_start_time = time.time()
                else:
                    facial_expression_end_time = time.time()
                    difference = facial_expression_end_time - facial_expression_start_time

                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if difference < facial_expression_limit_time:
                    print('[INFO] %s,  %s仅伤心了 %.1f 秒. 忽略' % (current_time, name, difference))
                else:
                    event_desc = '%s正在笑' % name
                    print('[EVENT] %s,  %s正在伤心.' % (current_time, name))
                    sad_msg = {
                        "event_date": current_time,
                        "event_type:": "Sad",
                        "event_desc": ' %s,  %s正在伤心.' % (current_time, name),
                        "event_img": output_sad_path
                    }
                    send_message_to_process(sad_msg)
                    cv2.imwrite(os.path.join(output_sad_path, 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                                frame)
            else:
                facial_expression_timing = 0

        final_label = name + ': ' + facial_expression_label
        cv2.putText(frame, final_label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Calculate and display FPS
        frame_counter += 1
        elapsed_time = time.time() - start_time
        fps = frame_counter / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Show the processed frame
        cv2.imshow("Checking Strangers and Ole People's Face Expression", frame)


# Define a function for video processing
def process_video():
    vs = cv2.VideoCapture(0)  # Create a video processor instance

    while True:
        (grabbed, frame) = vs.read()
        frame_buffer.append(frame)
        if len(frame_buffer)==BATCH_SIZE:
            for frame in frame_buffer:
                frame = imutils.resize(frame, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_location_list, names, categories = faceUtil.get_face_location_and_name(frame)

                facial_expression_analysis(frame, gray, face_location_list, names, categories)

        # Press 'ESC' for exiting video
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    vs.release()
    cv2.destroyAllWindows()


# Start the video processing thread
video_thread = threading.Thread(target=process_video)
video_thread.start()

# Wait for the video processing thread to complete
video_thread.join()
