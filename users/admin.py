from django.contrib import admin

from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_staff',)


admin.site.register(CustomUser, UserAdmin)
