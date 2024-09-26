from django.contrib import admin

from blog.models import Category, Comment, Location, Post


class PostInLine(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "pub_date",
        "text",
        "author",
        "location",
        "category",
        "is_published",
        "created_at",
    )
    list_editable = ("is_published", "location", "category",)
    search_fields = ("text",)
    list_filter = (
        "id",
        "created_at",
    )
    list_display_links = ("title",)
    empty_value_display = "-пусто-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)
    list_display = (
        "title",
        "description",
        "is_published",
    )
    list_editable = ("is_published",)
    search_fields = ("title",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    search_fields = ("name",)


admin.site.register(Comment)
