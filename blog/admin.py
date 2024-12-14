from django.contrib import admin

# Register your models here.
from .models import UserInfo, Blog, Category, Tag, Article, Article2Tag, ArticleUpDown, Comment

admin.site.site_header = 'XuMou的博客管理后台'
admin.site.site_title = 'XuMou的博客'
admin.site.index_title = 'XuMou Blogs'
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['nid', 'telephone', 'avatar', 'user_name']
    list_filter = ['telephone', 'username']

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Article2Tag)
admin.site.register(ArticleUpDown)
admin.site.register(Comment)

