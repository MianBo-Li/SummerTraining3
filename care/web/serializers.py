from rest_framework import serializers
from .models import SysUser


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = ['id', 'username', 'password', 'gender', 'phone']
