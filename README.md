# SummerTraining1Back
**在这个分支中主要进行算法的开发**
## 需要用到的库
  * pyhton 3.6.7
  * opencv-python 3.4.4.19
  * opencv-contrib-python 3.4.4.19
  * tensorflow 1.12.0
  * keras 2.2.4
  * dlib
  * face_recognition
## 数据集
  * 人脸识别模块：分别拍摄正对摄像头，向左看，向右看，张嘴，眨眼的照片各5张
  * 情绪识别模块：fer2013 链接：https://www.kaggle.com/datasets/deadskull7/fer2013
  * 摔倒检测模块：http://fenix.univ.rzeszow.pl/~mkepski/ds/uf.html

## 各模块接口
* facial模块
  * load_embeddings() 用来读取模型的数据
  * get_face_location() 用来探测图片中人脸的位置
  * get_face_location_and_name() 用来得到人脸对应的名字，若不存在则显示unknown
  * save_embeddings() 用来保存训练的模型

* 