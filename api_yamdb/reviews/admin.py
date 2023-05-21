from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка модели Reviews в админке."""

    list_display = (
        'id',
        'author',
        'text',
        'score',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = (
        'author',
        'text',
    )


class GenreInline(admin.TabularInline):
    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    inlines = (GenreInline,)


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
