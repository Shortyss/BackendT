from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from viewer.models import *


class MovieAdmin(ModelAdmin):

    @staticmethod
    def released_year(obj):
        return obj.year

    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)

    ordering = ['title_cz', 'title_sk', 'title_orig']
    list_display = ['id', 'title_orig', 'title_cz', 'year']
    list_display_links = ['id', 'title_orig', 'title_cz']
    list_per_page = 10
    list_filter = ['genres', 'countries']
    search_fields = ['title_orig', 'title_cz', 'title_sk', 'description']
    actions = ['cleanup_description']


class PersonAdmin(ModelAdmin):
    fieldsets = [
        (
            'Main Information',
            {
                'fields': ['first_name', 'last_name', 'created']
            }
        ),
        (
            'External Information',
            {
                'fields': ['birth_date'],
                'description': (
                    'These fields are going to be filled with data parsed '
                    'from external databases.'
                )
            }
        ),
        (
            'User Information',
            {
                'fields': ['biography'],
                'description': 'These fields are intended to be filled in by our users.'
            }
        )
    ]
    readonly_fields = ['created']


admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Person, PersonAdmin)