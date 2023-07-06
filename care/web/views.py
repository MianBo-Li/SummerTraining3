import base64
import os.path

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from django.http import JsonResponse
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.utils import json

from .serializers import get_project_root, download
from web import models

@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    sys_user = models.SysUser.objects.get(username=username, password=password)
    if sys_user is not None:
        return JsonResponse({'message': '登录成功', 'code': '0'}, status=200)
    else:
        return JsonResponse({'message': "用户名或者密码错误"}, status=500)
        # return JsonResponse({'success': '登录成功', 'user': sys_user.to_dict()}, status=200)


@csrf_exempt
def download_image(request):
    name = request.POST.get('name')
    path = get_project_root(name)

    print(path)
    arr = ['正脸', '向左看', '向右看', '眨眼', '张嘴', '笑']
    for i in range(0, 6):
        act = arr[i]
        for j in range(1, 6):
            image_name = f'{act}{j}'
            image_data = request.POST.get(image_name)
            download(path, image_name, image_data)

    return JsonResponse({'success': 'Image saved successfully'}, status=200)


@csrf_exempt
def controller_OldPerson(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('pageNum', 1))
        page_size = int(request.GET.get('pageSize', 10))
        search = request.GET.get('username', '')

        query = models.OldPerson.objects.all()
        if search:
            query = query.filter(name__contains=search)

        query = query.order_by('id')  # 假设按照 id 字段进行排序
        paginator = Paginator(query, page_size)
        try:
            user_page = paginator.page(page_num)
            users = user_page.object_list
            result = {
                'data': list(users.values()),
                'total': paginator.count,
                'page_num': user_page.number,
                'page_size': page_size
            }
            return JsonResponse(result)
        except EmptyPage:
            return JsonResponse({'error': 'Invalid page number'}, status=400)
    elif request.method == 'POST':
        data = json.loads(request.body)
        path = os.path.join('image', data['name'])
        data['img_dir'] = path
        old_person = models.OldPerson(**data)
        old_person.save()
        return JsonResponse({'success': '保存成功'}, status=200)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        old_person = models.OldPerson.objects.filter(id=data['id'])
        for key, value in data.items():
            setattr(old_person, key, value)
        old_person.save()
        return JsonResponse({'success': '更新成功'}, status=200)


@csrf_exempt
def delete_OldPerson(request, pk=None):
    # user_id = int(request.GET.get('id'))
    user_id = int(pk)
    models.OldPerson.objects.filter(id=user_id).delete()
    return JsonResponse({'success': '删除成功'}, status=200)


@csrf_exempt
def controller_Employee(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('pageNum', 1))
        page_size = int(request.GET.get('pageSize', 10))
        search = request.GET.get('username', '')

        query = models.Employee.objects.all()
        if search:
            query = query.filter(name__contains=search)

        query = query.order_by('id')  # 假设按照 id 字段进行排序
        paginator = Paginator(query, page_size)
        try:
            user_page = paginator.page(page_num)
            users = user_page.object_list
            result = {
                'data': list(users.values()),
                'total': paginator.count,
                'page_num': user_page.number,
                'page_size': page_size
            }
            return JsonResponse(result)
        except EmptyPage:
            return JsonResponse({'error': 'Invalid page number'}, status=400)
    elif request.method == 'POST':
        data = json.loads(request.body)
        path = os.path.join('image', data['name'])
        data['img_dir'] = path
        employee = models.Employee(**data)
        employee.save()
        return JsonResponse({'success': '保存成功'}, status=200)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        employee = models.Employee.objects.filter(id=data['id'])
        for key, value in data.items():
            setattr(employee, key, value)
        employee.save()
        return JsonResponse({'success': '更新成功'}, status=200)


@csrf_exempt
def delete_Employee(request, pk=None):
    # user_id = int(request.GET.get('id'))
    user_id = int(pk)
    models.Employee.objects.filter(id=user_id).delete()
    return JsonResponse({'success': '删除成功'}, status=200)


@csrf_exempt
def controller_Volunteer(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('pageNum', 1))
        page_size = int(request.GET.get('pageSize', 10))
        search = request.GET.get('username', '')

        query = models.Volunteer.objects.all()
        if search:
            query = query.filter(username__contains=search)

        query = query.order_by('id')  # 假设按照 id 字段进行排序
        paginator = Paginator(query, page_size)
        try:
            user_page = paginator.page(page_num)
            users = user_page.object_list
            result = {
                'data': list(users.values()),
                'total': paginator.count,
                'page_num': user_page.number,
                'page_size': page_size
            }
            return JsonResponse(result)
        except EmptyPage:
            return JsonResponse({'error': 'Invalid page number'}, status=400)
    elif request.method == 'POST':
        data = json.loads(request.body)
        path = os.path.join('image', data['name'])
        data['img_dir'] = path
        volunteer = models.Volunteer(**data)
        volunteer.save()
        return JsonResponse({'success': '保存成功'}, status=200)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        volunteer = models.Volunteer.objects.filter(id=data['id'])
        for key, value in data.items():
            setattr(volunteer, key, value)
        volunteer.save()
        return JsonResponse({'success': '更新成功'}, status=200)


@csrf_exempt
def delete_Volunteer(request, pk=None):
    # user_id = int(request.GET.get('id'))
    user_id = int(pk)
    models.Volunteer.objects.filter(id=user_id).delete()
    return JsonResponse({'success': '删除成功'}, status=200)


# @csrf_exempt
# def controller_SysUser(request):
#     if request.method == 'GET':
#         page_num = int(request.GET.get('pageNum', 1))
#         page_size = int(request.GET.get('pageSize', 10))
#         search = request.GET.get('username', '')
#
#         query = models.SysUser.objects.all()
#         if search:
#             query = query.filter(username__contains=search)
#
#         query = query.order_by('id')  # 假设按照 id 字段进行排序
#         paginator = Paginator(query, page_size)
#         try:
#             user_page = paginator.page(page_num)
#             users = user_page.object_list
#             result = {
#                 'data': list(users.values()),
#                 'total': paginator.count,
#                 'page_num': user_page.number,
#                 'page_size': page_size
#             }
#             return JsonResponse(result)
#         except EmptyPage:
#             return JsonResponse({'error': 'Invalid page number'}, status=400)
#     elif request.method == 'POST':
#         data = json.loads(request.body)
#         if 'password' not in data:
#             data['password'] = '123'
#         sys_user = models.SysUser(**data)
#         sys_user.save()
#         return JsonResponse({'success': '保存成功'}, status=200)
#     elif request.method == 'PUT':
#         data = json.loads(request.body)
#         sys_user = models.SysUser.objects.filter(id=data['id'])
#         for key, value in data.items():
#             setattr(sys_user, key, value)
#         sys_user.save()
#         return JsonResponse({'success': '更新成功'}, status=200)
#
#
# @csrf_exempt
# def delete_SysUser(request, pk=None):
#     # user_id = int(request.GET.get('id'))
#     user_id = int(pk)
#     models.SysUser.objects.filter(id=user_id).delete()
#     return JsonResponse({'success': '删除成功'}, status=200)

# class SysUserViews:
#
#     @action(detail=True, methods=['DELETE'])
#     def delete_SysUser(self, request, pk=None):
#         # user_id = int(request.GET.get('id'))
#         user_id = int(pk)
#         models.SysUser.objects.filter(id=user_id).delete()
#         return JsonResponse({'success': '删除成功'}, status=200)

# class SysUserViews(viewsets.ModelViewSet):
#     serializer_class = SysUserSerializer
#     # queryset = models.SysUser.objects.all()
#
#     def get_queryset(self):
#         return models.SysUser.objects.all()

# def list_oldPerson(request):
#     queryset = models.OldPerson.objects.all()
#     return render(request, '', {'queryset': queryset})
#
#
# def add_oldPerson(request):
#     # request.POST.get()
#     return HttpResponse("添加成功")

# 增加
# models.SysUser.objects.create(username="js", password="123", gender="男", phone="15312341234", id_card="098780",
#                               email="123@qq.com")

# 查询
# queryset = models.SysUser.objects.all()
# queryset = models.SysUser.objects.filter(id=1)
# for obj in queryset:
#     print(obj.id, obj.username)

# 删除
# models.SysUser.objects.filter(id=2).delete()

# 更新
# models.SysUser.objects.filter(id=1).update(phone="")

# return render(request, 'admin.html', {'queryset': queryset})
