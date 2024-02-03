from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from contas.forms import UserCreationForm
from contas.models import MyUser

class MyUserAdmin(UserAdmin):
    # add_form = UserCreationForm
    model = MyUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','force_change_password', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)


admin.site.register(MyUser, MyUserAdmin)