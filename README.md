# SummerTraining1Back
**在这个分支中主要进行算法的开发**

* facial模块
  * load_embeddings() 用来读取模型的数据
  * get_face_location() 用来探测图片中人脸的位置
  * def get_face_location_and_name() 用来得到人脸对应的名字，若不存在则显示unknown
  * save_embeddings() 用来保存训练的模型