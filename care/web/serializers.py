import base64
import os

from rest_framework import serializers
from .models import SysUser


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = ['id', 'username', 'password', 'gender', 'phone']


def get_project_root(name):
    # 获取当前脚本文件的绝对路径
    script_path = os.path.abspath(__file__)
    # 返回当前脚本文件所在的目录
    script_dir = os.path.dirname(script_path)
    # 返回当前脚本文件所在的目录的父级目录，即项目的根目录
    root_dir = os.path.dirname(script_dir)
    path = os.path.join(root_dir, 'image')
    path = os.path.join(path, name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def download(path, image_name, image_data):
    image = image_name + '.png'
    path = os.path.join(path, image)
    if image_data:
        # image_data = image_data.encode("utf-8")
        _, image_data = image_data.split(',', 1)
        image_bytes = base64.b64decode(image_data)

        with open(path, 'wb') as file:
            file.write(image_bytes)

