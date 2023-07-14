# -*- coding: utf-8 -*-
"""
使用dlib实现人脸检测
"""
import face_recognition
import cv2
import pickle
import os

from cv2 import CV_8UC3


class FaceUtil:
    # 超参数
    detection_method = 'hog'  # either 'hog' or 'cnn'. default is hog.
    tolerance = 0.3

    def __init__(self, encoding_file_path=None):
        """
        为人脸识别这个类初始化一个实例
        :param encoding_file_path: None
        """

        if encoding_file_path:
            self.load_embeddings(encoding_file_path)

    # load embeddings
    def load_embeddings(self, encoding_file_path):
        """
        从所给路径加载人脸模型，读取人脸信息
        :param encoding_file_path: 人脸模型文件的位置
        :return:
        """
        # load the known faces and embeddings
        print("[INFO] loading face encodings...")
        self.data = pickle.loads(open(encoding_file_path, "rb").read())

    # face detection
    def get_face_location(self, image):
        """
        检测图像中人脸的位置
        :param image: BGR格式的图像
        :return:face_location_list (list):表示每个检测到的人脸的边界框坐标的元组列表，格式为（左、上、右、下）。
        """
        face_location_list = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_locations = face_recognition.face_locations(
            gray, number_of_times_to_upsample=1,
            model=self.detection_method)
        # 人脸位置
        for (top, right, bottom, left) in face_locations:
            face_location_list.append((left, top, right, bottom))

        return face_location_list

    # face recognition
    def get_face_location_and_name(self, image):
        """
        检测图像中人脸的位置并进行识别
        :param image: BGR格式的图像
        :return: tuple:包含三个列表的元组
                - face_location_list (list):表示每个检测到的人脸的边界框坐标的元组列表，格式为（左、上、右、下）。
                - names (list):与每个检测到的面孔相对应的已识别名称列表。如果未识别出面孔，则指定“未知”作为名称。
                - categories (list): 与每个检测到的面孔相对应的类别列表。
        """
        # convert the input frame from BGR to RGB

        if image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then
        # compute the facial embeddings for each face
        boxes = face_recognition.face_locations(
            image, model=self.detection_method)
        encodings = face_recognition.face_encodings(image, boxes)

        # initialize the list of names and categories for each face detected
        names = []
        categories = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to
            # our known encodings
            matches = face_recognition.compare_faces(
                self.data["encodings"], encoding,
                tolerance=self.tolerance)
            name = "Unknown"
            category = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then
                # initialize a dictionary to count the total number
                #  of times each face was matched
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count
                # for each recognized face
                for i in matched_idxs:
                    match_name, match_category = self.data["names"][i]
                    counts[match_name] = counts.get(match_name, 0) + 1

                # determine the recognized face with the largest
                # number of votes (note: in the event of an unlikely
                # tie Python will select first entry in the
                # dictionary)
                name = max(counts, key=counts.get)
                category = match_category

            # update the list of names
            names.append(name)
            categories.append(category)

        face_location_list = []
        for (top, right, bottom, left) in boxes:
            face_location_list.append((left, top, right, bottom))

        return face_location_list, names, categories

    @staticmethod
    def save_embeddings(image_paths, output_encoding_file_path):
        """
        通过已经收集到的人脸信息训练模型并保存

        :param image_paths: 人脸信息数据集的路径 从项目根目录开始的相对路径即可
        :param output_encoding_file_path: 要输出的模型的位置
        :return:
        """
        # error msg
        global suitable_image_found
        warning = ''

        # Check if the output file already exists
        file_exists = os.path.isfile(output_encoding_file_path)

        # Load existing data if the file exists
        if file_exists:
            with open(output_encoding_file_path, "rb") as f:
                existing_data = pickle.load(f)
            known_encodings = existing_data["encodings"]
            known_names = existing_data["names"]
        else:
            known_encodings = []
            known_names = []

        # Loop over the image paths
        for i, image_path in enumerate(image_paths):
            # Skip the image if it has already been processed
            if image_path in [name[0] for name in known_names]:
                print("[INFO] Skipping already processed image: {}".format(image_path))
                continue

            # Load the input image
            image = face_recognition.load_image_file(image_path)

            # Detect faces in the image
            face_locations = face_recognition.face_locations(image)

            if len(face_locations) != 1:
                os.remove(image_path)
                warning += f'[WARNING] detected {len(face_locations)} faces in {image_path}.'
                warning += ' This file is deleted.\n'
                continue

            # Encode the facial features
            encoding = face_recognition.face_encodings(image, face_locations)[0]

            # Extract the person name from the image path
            print(f"[INFO] processing image {i + 1}/{len(image_paths)}")
            category_label = os.path.basename(os.path.dirname(os.path.dirname(image_path)))
            name = os.path.basename(os.path.dirname(image_path))

            # Add the encoding and name to the lists
            known_encodings.append(encoding)
            known_names.append((name, category_label))

            suitable_image_found = True  # Set the flag to True

        # Check if a suitable image was found
        if not suitable_image_found:
            raise ValueError("No suitable image found")

        # Serialize the encodings and names
        data = {"encodings": known_encodings, "names": known_names}

        # Dump the data to the output file
        with open(output_encoding_file_path, "wb") as f:
            pickle.dump(data, f)

        if warning:
            print(warning)

        print("[INFO] The facial model has been saved, quit.\n")

