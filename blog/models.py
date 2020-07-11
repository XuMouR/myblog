from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

'''
    共八张表，到时会生成十张表
    
'''


class UserInfo(AbstractUser):
    '''
    用户信息
    '''

    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to="avatars/", default="/avatars/default.jpg")
    # auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
    # auto_now_add为添加时的时间，更新对象时不会有变动。
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    blog = models.OneToOneField("Blog", null=True, on_delete=models.CASCADE, verbose_name="站点对象")

    def __str__(self):  # 当实例对象调用的时候，返回这个改值
        return self.username


class Blog(models.Model):
    '''
    博客信息
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="个人博客标题", max_length=64)
    site_name = models.CharField(verbose_name="站点名称", max_length=64)
    theme = models.CharField(verbose_name="博客主题", max_length=32)

    def __str__(self):
        return self.title


class Category(models.Model):
    '''
    博主个人文章分类
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="分类标题", max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客", to="Blog", to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)  # primary_key  设置这个键为主键
    title = models.CharField(verbose_name="标题名称", max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客", to="Blog", to_field="nid", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="文章标题")
    desc = models.CharField(max_length=255, verbose_name="文章描述")
    content = models.TextField(verbose_name="文章内容")
    # auto_now_add为添加时的时间，更新对象时不会有变动。
    create_time = models.DateTimeField(verbose_name="文章创建时间", auto_now_add=True)
    comment_count = models.IntegerField(verbose_name="评论数量", default=0)
    up_count = models.IntegerField(verbose_name="点赞数量", default=0)
    down_count = models.IntegerField(verbose_name="下载数量", default=0)

    user = models.ForeignKey(verbose_name="作者", to="UserInfo", to_field="nid", on_delete=models.CASCADE)
    # 文章分类
    category = models.ForeignKey(to="Category", to_field="nid", null=True, on_delete=models.CASCADE)
    # through 用于多对多关系时候，定义中间表，到时会多创建一张表Article2Tag
    # through_fields  用于定义中间表的时候，作为关联两个表的 关联字段
    tags = models.ManyToManyField(to="Tag", through="Article2Tag", through_fields=("article", "tag"))

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name="文章", to="Article", to_field="nid", on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name="标签", to="Tag", to_field="nid", on_delete=models.CASCADE)

    class Meta:
        '''
        unique_together这个选项用于：当你需要通过两个字段保持唯一性时使用。这会在 Django admin
        层和数据库层同时做出限制(也就是相关的 UNIQUE 语句会被包括在 CREATE TABLE 语句中)。
        比如：一个Person的FirstName和LastName两者的组合必须是唯一的，那么需要这样设置：
        unique_together = (("first_name", "last_name"),)
        '''
        unique_together = [
            ('article', "tag")

        ]

    def __str__(self):
        v = self.article.title + "---" + self.tag.title
        return v


class ArticleUpDown(models.Model):
    '''
    点赞表
    '''
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey("UserInfo", null=True, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ("article", "user"),
        ]


class Comment(models.Model):
    '''
    评论表
    '''
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name="评论文章", to='Article', to_field="nid", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="评论者", to="UserInfo", to_field="nid", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容", max_length=255)
    create_time = models.DateTimeField(verbose_name="评论创建时间", auto_now_add=True)
    parent_comment = models.ForeignKey("self", verbose_name="父级评论", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
