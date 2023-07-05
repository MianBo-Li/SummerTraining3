from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from django.http import JsonResponse
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.utils import json

from .serializers import SysUserSerializer
from web import models


@csrf_exempt
def controller_SysUser(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('pageNum', 1))
        page_size = int(request.GET.get('pageSize', 10))
        search = request.GET.get('username', '')

        query = models.SysUser.objects.all()
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
        if 'password' not in data:
            data['password'] = '123'
        sys_user = models.SysUser(**data)
        sys_user.save()
        return JsonResponse({'success': '保存成功'}, status=200)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        sys_user = models.SysUser.objects.filter(id=data['id'])
        for key, value in data.items():
            setattr(sys_user, key, value)
        sys_user.save()
        return JsonResponse({'success': '更新成功'}, status=200)


@csrf_exempt
def delete_SysUser(request, pk=None):
    # user_id = int(request.GET.get('id'))
    user_id = int(pk)
    models.SysUser.objects.filter(id=user_id).delete()
    return JsonResponse({'success': '删除成功'}, status=200)
# def find_page(request):
#     page_num = int(request.GET.get('pageNum', 1))
#     page_size = int(request.GET.get('pageSize', 10))
#     search = request.GET.get('username', '')
#
#     query = models.SysUser.objects.all()
#     if search:
#         query = query.filter(username__contains=search)
#
#     query = query.order_by('id')  # 假设按照 id 字段进行排序
#     paginator = Paginator(query, page_size)
#     try:
#         user_page = paginator.page(page_num)
#         users = user_page.object_list
#         result = {
#             'data': list(users.values()),
#             'total': paginator.count,
#             'page_num': user_page.number,
#             'page_size': page_size
#         }
#         return JsonResponse(result)
#     except EmptyPage:
#         return JsonResponse({'error': 'Invalid page number'}, status=400)


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
#     queryset = models.SysUser.objects.all()
#
#     @action(detail=True, methods=['DELETE'])
#     def delete_SysUser(self, request, pk=None):
#         # user_id = int(request.GET.get('id'))
#         user_id = int(pk)
#         models.SysUser.objects.filter(id=user_id).delete()
#         return JsonResponse({'success': '删除成功'}, status=200)

# def get_queryset(self):
#     return models.SysUser.objects.all()

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
