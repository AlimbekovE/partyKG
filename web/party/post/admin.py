from django.contrib import admin
from django.utils.safestring import mark_safe

from party.post.models import Post, PostImages


class ImageInline(admin.TabularInline):
    model = PostImages

    fields = ('file', 'type', 'output')
    readonly_fields = ('output',)

    def output(self, obj):
        output = ''
        if file := getattr(obj, 'file', None):
            if obj.type == 'image':
                output = f'<a href="{file.url}?w=270&h=150" target="_blank">' \
                         f'<img src="{file.url}?w=270&h=150"' \
                         f'height=150 width=270/></a>'

            elif obj.type == 'video':
                output = f'<video width="270" height="150" controls>' \
                         f'<source src="{file.url}">' \
                         f'</video>'
        return mark_safe(output)


class PostAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)
    raw_id_fields = ('owner',)
    list_display = ('owner', 'title')


admin.site.register(Post, PostAdmin)
