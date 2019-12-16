from django.contrib import admin
from django.utils.safestring import mark_safe

from party.post.models import Post, PostImages


class ImageInline(admin.TabularInline):
    model = PostImages

    ields = ('user', 'image', 'picture')
    readonly_fields = ('image',)

    def image(self, obj):
        if obj.picture:
            output = f'<a href="{obj.picture.url}?w=270&h=150" target="_blank">' \
                     f'<img src="{obj.picture.url}?w=270&h=150"' \
                     f'height=150 width=270/></a>'
        else:
            output = ""
        return mark_safe(output)


class PostAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)
    raw_id_fields = ('owner',)
    list_display = ('owner', 'title')


admin.site.register(Post, PostAdmin)
