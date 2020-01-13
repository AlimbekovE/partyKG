from django.contrib import admin
from django.utils.safestring import mark_safe
from party.event.models import Event


class EventAdmin(admin.ModelAdmin):
    fields = (
        'owner', 'title', 'description',
        'number_of_people', 'location',
        'datetime', 'qr_code_scanner',
        'visits'
    )
    list_display = ('title', 'location', 'datetime', 'number_of_people')
    readonly_fields = ('qr_code_scanner', 'visits')
    raw_id_fields = ('owner',)

    def qr_code_scanner(self, obj):
        html = f"<a href='{obj.get_qr_code_url()}'>qr code</a>"
        return mark_safe(html)

    def visits(self, obj):
        html = f"<a href='{obj.get_user_visit_url()}'>visits</a>"
        return mark_safe(html)


admin.site.register(Event, EventAdmin)
