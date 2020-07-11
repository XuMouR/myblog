from django.contrib import admin

# Register your models here.
from .models import  UserInfo,Blog,Category,Tag,Article,Article2Tag,ArticleUpDown,Comment


admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Article2Tag)
admin.site.register(ArticleUpDown)
admin.site.register(Comment)
