from users.models import Users
from django.contrib import admin


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name",
                    "is_superuser", "is_staff", "date_joined"]
    #list_display = ['image', 'email', 'gender', 'birthday', 'is_superuser', 'is_staff']
    #ordering = ['birthday']
    #list_filter = ['birthday']
    #search_fields = ['email']
    #search_help_text = 'Поиск по полю email'


#admin.site.register(Users, UsersAdmin)

