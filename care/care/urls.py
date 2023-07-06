"""
URL configuration for care project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from django.urls import re_path as url
from rest_framework import routers
from web import views

router = routers.DefaultRouter()
# router.register(r'SysUser', views.SysUserViews, basename='SysUser')

urlpatterns = [
    path("admin/", admin.site.urls),
    url('', include(router.urls)),
    # path("SysUser/", views.find_page, name="find_page"),
    path("save_image/", views.download_image, name="download_image"),
    # path("SysUser/", views.controller_SysUser, name="controller_SysUser"),
    # path("SysUser/delete/<int:pk>", views.delete_SysUser, name="delete_SysUser"),
    path('login/', views.login, name='login'),
    path("OldPerson/", views.controller_OldPerson, name="controller_OldPerson"),
    path("OldPerson/delete/<int:pk>", views.delete_OldPerson, name="delete_OldPerson"),
    path("Employee/", views.controller_Employee, name="controller_Employee"),
    path("Employee/delete/<int:pk>", views.delete_Employee, name="delete_Employee"),
    path("Volunteer/", views.controller_Volunteer, name="controller_Volunteer"),
    path("Volunteer/delete/<int:pk>", views.delete_Volunteer, name="delete_Volunteer"),
    # path('list_oldPerson/', views.list_oldPerson),
    # path('add_oldPerson/', views.add_oldPerson),
    # path("SysUser/delete/<int:pk>", views.SysUserViews.as_view({'delete': 'delete_SysUser'}), name='delete_SysUser')
]
