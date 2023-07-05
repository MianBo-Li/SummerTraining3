# Generated by Django 4.2.2 on 2023-07-05 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="工作人员姓名")),
                ("gender", models.CharField(max_length=5, verbose_name="性别")),
                ("age", models.IntegerField(verbose_name="年龄")),
                ("phone", models.CharField(max_length=50, verbose_name="电话")),
                ("id_card", models.CharField(max_length=50, verbose_name="身份证")),
                ("checkin_date", models.DateTimeField(verbose_name="入职日期")),
                ("img_dir", models.CharField(max_length=200, verbose_name="图像目录")),
            ],
        ),
        migrations.CreateModel(
            name="OldPerson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="老人姓名")),
                ("room_number", models.CharField(max_length=50, verbose_name="房间号")),
                ("gender", models.CharField(max_length=5, verbose_name="性别")),
                ("age", models.IntegerField(verbose_name="年龄")),
                ("phone", models.CharField(max_length=50, verbose_name="电话")),
                ("id_card", models.CharField(max_length=50, verbose_name="身份证")),
                ("checkin_date", models.DateTimeField(verbose_name="入院日期")),
                ("img_dir", models.CharField(max_length=200, verbose_name="图像目录")),
                (
                    "guardian_name",
                    models.CharField(max_length=50, verbose_name="监护人姓名"),
                ),
                ("health_state", models.CharField(max_length=50, verbose_name="健康状况")),
            ],
        ),
        migrations.CreateModel(
            name="SysUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=50, verbose_name="姓名")),
                ("password", models.CharField(max_length=50, verbose_name="密码")),
                ("gender", models.CharField(max_length=5, verbose_name="性别")),
                ("phone", models.CharField(max_length=50, verbose_name="电话")),
                ("id_card", models.CharField(max_length=50, verbose_name="身份证")),
                ("email", models.CharField(max_length=50, verbose_name="邮箱")),
            ],
        ),
        migrations.CreateModel(
            name="Volunteer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="义工姓名")),
                ("gender", models.CharField(max_length=5, verbose_name="性别")),
                ("age", models.IntegerField(verbose_name="年龄")),
                ("phone", models.CharField(max_length=50, verbose_name="电话")),
                ("id_card", models.CharField(max_length=50, verbose_name="身份证")),
                ("checkin_date", models.DateTimeField(verbose_name="访问日期")),
                ("img_dir", models.CharField(max_length=200, verbose_name="图像目录")),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_type", models.IntegerField(verbose_name="事件类型")),
                ("event_date", models.DateTimeField(verbose_name="事件发送日期")),
                (
                    "oldPerson_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="oldPersonId",
                        to="web.oldperson",
                    ),
                ),
            ],
        ),
    ]
