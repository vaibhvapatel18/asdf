from django.contrib import admin
from apiapp.models import User,Restaurant,MenuItem,UserLikeRetaurant,Userlikemenuitem,Usersavemenuitem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "email" , "name", "tc", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["id", "email"]
    filter_horizontal = []



admin.site.register(User, UserModelAdmin)
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(UserLikeRetaurant)
admin.site.register(Userlikemenuitem)
admin.site.register(Usersavemenuitem)




