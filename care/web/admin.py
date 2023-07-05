from django.contrib import admin
from .models import SysUser


class SysUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'gender', 'phone']


admin.site.register(SysUser, SysUserAdmin)
