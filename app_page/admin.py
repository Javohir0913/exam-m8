from django.contrib import admin


from .models import FAQ, Requirements, Contacts, Appeal


class AppealAdmin(admin.ModelAdmin):
    list_display = ("first_name", "email")
    search_fields = ("first_name", "email")
    list_filter = ("first_name", "email")


# Register your models here
admin.site.register(FAQ)
admin.site.register(Requirements)
admin.site.register(Contacts)
admin.site.register(Appeal, AppealAdmin)
