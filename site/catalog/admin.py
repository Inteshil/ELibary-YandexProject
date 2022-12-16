from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from catalog.models import Book, BookChapter, Tag


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основное', {'fields': ('name', 'preview')}),
        ('Состояние', {'fields': ('is_published', 'is_blocked')}),
        (
            'Информация', {
                'fields': (
                    'description', 'age_rating', 'author', 'tags',
                    'creation_data'
                    )
                }
        ),
    )
    list_display = (
        'name', 'author', 'age_rating', 'is_published', 'is_blocked'
        )
    list_editable = ('is_published', 'is_blocked')
    filter_horizontal = ('tags',)
    readonly_fields = ('creation_data',)

    class BookChapterInline(admin.TabularInline):
        model = BookChapter
        extra = 0
        show_change_link = True
        fields = ('name', 'number', 'is_published')
    inlines = (BookChapterInline, )


@admin.register(BookChapter)
class BookChapterAdmin(SummernoteModelAdmin):
    fields = ('name', 'number', 'is_published', 'content', 'book')
    list_display = ('name', 'book', 'number', 'is_published')
    list_editable = ('is_published',)
    ordering = ('number',)
    summernote_fields = ('content',)


@admin.register(BookChapter)
class BookChapterAdmin(SummernoteModelAdmin):
    fields = ('name', 'number', 'is_published', 'content', 'book')
    list_display = ('name', 'book', 'number', 'is_published')
    list_editable = ('is_published',)
    ordering = ('number',)
    summernote_fields = ('content',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)
