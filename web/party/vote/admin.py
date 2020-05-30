from django.contrib import admin
from party.vote.models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner',)
    list_filter = ('created',)


admin.site.register(Question, QuestionAdmin)
