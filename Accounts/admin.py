from django.contrib import admin
from .models import CustomUser
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "id_number",
        "phone_number",
        "user_type",
        
    )
    list_filter = (
        "user_type",
        "is_active",
        "is_staff",
        
    )


admin.site.register(CustomUser,CustomUserAdmin)
