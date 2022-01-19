from django.contrib import admin
from user.models import SignUpOrder, CustomUser,PasswordChangeOrder

admin.site.register(SignUpOrder)
admin.site.register(CustomUser)
admin.site.register(PasswordChangeOrder)

# Register your models here.
