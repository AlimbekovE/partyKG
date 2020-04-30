from django.contrib import admin
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import Token

from party.account.models import User, Avatar, Position
from django.contrib.auth.models import Group

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field


class AvatarInline(admin.TabularInline):
    model = Avatar
    fields = ('user', 'image', 'picture')
    readonly_fields = ('picture',)

    def picture(self, obj):
        if obj.image:
            output = f'<a href="{obj.image.url}?w=270&h=150" target="_blank">' \
                     f'<img src="{obj.image.url}?w=270&h=150"' \
                     f'height=150 width=270/></a>'
        else:
            output = ""
        return mark_safe(output)


class UserResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Имя')
    surname = Field(attribute='surname', column_name='Фамилия')
    patronymic = Field(attribute='patronymic', column_name='Отчество')
    phone = Field(attribute='phone', column_name='Телефон')
    email = Field(attribute='email', column_name='E-mail')
    position = Field(attribute='position', column_name='Должность')
    gender = Field(attribute='gender', column_name='Пол')
    marital_status = Field(attribute='marital_status', column_name='Семейное положение')
    plot = Field(attribute='plot', column_name='Участок')
    representation = Field(attribute='representation', column_name='Представление')
    date_of_birth = Field(attribute='date_of_birth', column_name='Дата рождения')
    city = Field(attribute='city', column_name='Город')
    region = Field(attribute='region', column_name='Область')
    district = Field(attribute='district', column_name='Район')

    class Meta:
        model = User
        ordering = ['name']
        exclude = ('id', 'password', 'last_login', 'activation_code',
                   'is_staff', 'is_active')


class UserAdmin(ImportExportModelAdmin):
    inlines = (AvatarInline,)
    exclude = ('password', 'last_login')
    list_display = ('name', 'surname', 'patronymic', 'phone', 'position')
    resource_class = UserResource


class PositionAdmin(admin.ModelAdmin):
    fields = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.unregister(Group)
admin.site.unregister(Token)
