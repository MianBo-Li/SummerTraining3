from django.contrib import admin
from .models import SysUser


class SysUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'gender', 'phone', 'id_card', 'email']


admin.site.register(SysUser, SysUserAdmin)
