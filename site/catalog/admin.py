from django.contrib import admin

from catalog.models import Book, Tag


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основное', {'fields': ('name', 'preview', 'content')}),
        ('Состояние', {'fields': ('is_published', 'is_blocked')}),
        (
            'Информация', {
                'fields': (
                    'description', 'slug', 'age_rating',
                    'author', 'tags', 'creation_data'
                    )
                }
        ),
    )
    list_display = (
        'name', 'author', 'age_rating', 'is_published', 'is_blocked'
        )
    list_editable = ('is_published', 'is_blocked')
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('creation_data',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)
