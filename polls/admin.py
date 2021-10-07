"""File for administrator panel."""
# Register your models here.

from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Display choice in admin panel."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Class for make field set of polls with display and search."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'was_published_recently', 'end_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
