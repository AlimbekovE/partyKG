from django.contrib import admin
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import Token

from party.account.models import User, Avatar
from django.contrib.auth.models import Group


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


class UserAdmin(admin.ModelAdmin):
    inlines = (AvatarInline,)
    exclude = ('password', 'last_login')
    list_display = ('name', 'surname', 'patronymic', 'phone', 'position')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.unregister(Token)
