from django.contrib import admin
from user.models import CreateUser, CustomUser,PasswordChangeOrder

admin.site.register(CreateUser)
admin.site.register(CustomUser)
admin.site.register(PasswordChangeOrder)

# Register your models here.
