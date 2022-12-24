from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from reports.models import BookReport


@admin.register(BookReport)
class BookChapterAdmin(SummernoteModelAdmin):
    fields = ('sender', 'book', 'reason', 'content', 'creation_datetime')
    readonly_fields = (
        'sender', 'book', 'reason', 'creation_datetime'
        )
    summernote_fields = ('content',)
