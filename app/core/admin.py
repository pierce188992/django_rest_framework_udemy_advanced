# from django.contrib import admin  # noqa

# # Register your models here.

"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

"""
允許在定義時翻譯字符串，但延遲評估結果直到字符串被使用。
使用其他語言的環境中被使用時（並且該語言的翻譯可用），
"Name" 會被自動翻譯成該語言的對應文本。
class MyModel(models.Model):
    name = models.CharField(_("Name"), max_length=255)
"""
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    # 當添加新用戶時，在添加頁面上顯示的字段組和字段。
    # 這與 fieldsets 類似，但專用於添加頁面。
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
