from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    UserProfile,
    Company,
    CompanyProfile,
    Project,
    ProjectDocument,
    ProjectRFI,
    DrawingCategory,
    ProjectDrawing,
    ProjectPhoto,
    Invitation
)


class UserAdminConfig(UserAdmin):
    search_fields = ("email", "username")
    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    fieldsets = (
        (None, {"fields": ("email", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Personal", {"fields": ("first_name", "last_name", "title")}),
    )


# Register your models here.
admin.site.register(User, UserAdminConfig)
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Company)
admin.site.register(CompanyProfile)
admin.site.register(ProjectDocument)
admin.site.register(ProjectRFI)
admin.site.register(DrawingCategory)
admin.site.register(ProjectDrawing)
admin.site.register(ProjectPhoto)
admin.site.register(Invitation)