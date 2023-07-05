from django.db import models


class SysUser(models.Model):
    username = models.CharField(verbose_name="姓名", max_length=50)
    password = models.CharField(verbose_name="密码", max_length=50)
    gender = models.CharField(verbose_name="性别", max_length=5)
    phone = models.CharField(verbose_name="电话", max_length=50)
    id_card = models.CharField(verbose_name="身份证", max_length=50)
    email = models.CharField(verbose_name="邮箱", max_length=50)


class OldPerson(models.Model):
    name = models.CharField(verbose_name="老人姓名", max_length=50)
    room_number = models.CharField(verbose_name='房间号', max_length=50)
    gender = models.CharField(verbose_name="性别", max_length=5)
    age = models.IntegerField(verbose_name="年龄")
    phone = models.CharField(verbose_name="电话", max_length=50)
    id_card = models.CharField(verbose_name="身份证", max_length=50)
    checkin_date = models.DateTimeField(verbose_name="入院日期")
    img_dir = models.CharField(verbose_name='图像目录', max_length=200)
    guardian_name = models.CharField(verbose_name="监护人姓名", max_length=50)
    health_state = models.CharField(verbose_name="健康状况", max_length=50)


class Employee(models.Model):
    name = models.CharField(verbose_name="工作人员姓名", max_length=50)
    gender = models.CharField(verbose_name="性别", max_length=5)
    age = models.IntegerField(verbose_name="年龄")
    phone = models.CharField(verbose_name="电话", max_length=50)
    id_card = models.CharField(verbose_name="身份证", max_length=50)
    checkin_date = models.DateTimeField(verbose_name="入职日期")
    img_dir = models.CharField(verbose_name='图像目录', max_length=200)


class Volunteer(models.Model):
    name = models.CharField(verbose_name="义工姓名", max_length=50)
    gender = models.CharField(verbose_name="性别", max_length=5)
    age = models.IntegerField(verbose_name="年龄")
    phone = models.CharField(verbose_name="电话", max_length=50)
    id_card = models.CharField(verbose_name="身份证", max_length=50)
    checkin_date = models.DateTimeField(verbose_name="访问日期")
    img_dir = models.CharField(verbose_name='图像目录', max_length=200)


class Event(models.Model):
    event_type = models.IntegerField(verbose_name="事件类型")
    event_date = models.DateTimeField(verbose_name="事件发送日期")
    oldPerson_id = models.ForeignKey(OldPerson, on_delete=models.CASCADE, related_name='oldPersonId')

