from django.contrib import admin
from .models import Post, User, Banner, BlogCategory,Tags


# admin页面普通展示
admin.site.register(User)
admin.site.register(Banner)
admin.site.register(BlogCategory)
admin.site.register(Tags)


# admin页面定制展示
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')