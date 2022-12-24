from django.contrib import admin

from quote.models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'text', 'creation_date')
    readonly_fields = ('creation_date',)
