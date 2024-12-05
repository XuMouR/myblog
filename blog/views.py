from django.db import transaction  # 事物操作
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.urls import reverse
# Create your views here.
from django.contrib import auth
from .Myforms import UserForm
from .models import UserInfo, Blog, Category, Tag, Article, Article2Tag, ArticleUpDown, Comment
from django.db.models import Q, F, Count, Max, Min, Avg, Count
from django.db.models.functions import TruncMonth
import json
# 发送邮件需要的模块
from django.core.mail import send_mail
from myblog import settings
import os
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from .utils.page import Pagination
from .Myforms import ChangePwdForm


# 登陆函数
def login(request):
    if request.method == "GET":

        return render(request, "login4.html")

    else:
        response = {"user": None, "msg": None}
        print(">>", request.POST)
        user = request.POST.get("username")
        # print(">>>>>>>>>>", type(user))
        pwd = request.POST.get("password")
        user_login = auth.authenticate(username=user, password=pwd)
        # print("登陆用户提交的数据〉〉", user, pwd, )
        # print("authenticate验证结果〉", user_login)
        if user_login:
            # 将 user对象注册进去
            auth.login(request, user_login)
            response["user"] = user_login.username

        else:
            response["msg"] = "用户名或则密码错误！"

    return JsonResponse(response)


# 注册函数
def register(request):
    # 前端利用ajax 提交表单注册信息
    if request.is_ajax():
        form = UserForm(request.POST)  # 提交的用户注册数据
        response = {"user": None, "msg": None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")  # 拿到用户上传的图片对象
            print("图片路径", avatar_obj)
            # print("提交的数据是〉〉", user, pwd, email, avatar_obj)
            if avatar_obj:                # 将新用户注册信息写入数据库
                # user_obj = UserInfo.objects.create(username=user, password=pwd, email=email, avatar=avatar_obj)
                user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar_obj)

            else:
                # 使用默认头像
                # user_obj = UserInfo.objects.create(username=user, password=pwd, email=email)
                user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email)
        else    :
            print("错误>>", form.errors)
            response["msg"] = form.errors

        return JsonResponse(response)

    form = UserForm()
    # get请求直接把UserForm对象传给页面
    return render(request, "register.html", {"form": form})


# @login_required()
def change_pwd(request):
    if request.method == "GET":

        return render(request, "change_pwd_no.html")
    else:

        return redirect("/blog/login/")
    '''
        if request.method == "GET":
        form = ChangePwdForm()
        print("get>>",form)
        return render(request, "change_pwd.html", {"form": form})
    else:
        form = ChangePwdForm(request.POST)
        print("密码修改form>>>",form)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get("oldpwd")
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get("newpassword1", "")
                        print("新的密码是〉",newpassword)

                user.set_password(newpassword)
                user.save()
                return render(request, "index.html", {"changepwd_success": True})

            else:
                return render(request, "change_pwd.html", {"form": form, 'oldpassword_is_wrong': True})

        else:

            return render(request, "change_pwd.html", {"form": form})
    '''


# 账户注销
@login_required()
def logout(request):
    auth.logout(request)

    return redirect("/blog/login/")


# 首页函数
def index(request):
    article_list = Article.objects.all()
    current_page = request.GET.get("page")
    pagination = Pagination(current_page, article_list.count(), request, per_page=10)

    # 当前页面的所有数据的显示范围
    current_page_obj = Article.objects.all()[pagination.start:pagination.end]
    # print("分页器〉〉",pagination.start,current_page_obj)

    #  批量生成假数据
    # from fake_data_file import add_fake_data
    # add_fake_data.add_fake_datas(request
    print(request.user)
    return render(request, "index.html", locals())

    '''
    # 将文章article从数据库提取出来  提供给前端展示
    article_list = Article.objects.all()
    # print(article_list)
    # 引入分页器
    # print(request.GET)
    # 总数
    all_count = Article.objects.all()
    current_page = request.GET.get("page")
    pagination = Pagination(current_page, all_count.count(), request, per_page=2)

    # 当前页面的所有数据的显示范围
    current_page_obj = Article.objects.all()[pagination.start:pagination.end]

    # 当前用户的所有标签
    tag_list = Tag.objects.filter(blog__userinfo=request.user).all()
    print("当前用户的所有标签", tag_list)
    # 当前用户的Category分类
    categoty_list = Category.objects.filter(blog__userinfo=request.user).all()
    print("当前用户的Category分类", categoty_list)
    '''


# 个人站点视图函数
# **kwargs 用于接受动态关键字参数
@login_required()
def home_site(request, username, **kwargs):  # username  为当前登陆人的名字

    # print("===〉", request) # <WSGIRequest: GET '/admin/tag/%E6%97%A5%E6%9C%AC%E5%B0%8F%E8%AF%B4/'> 中文编码错误

    '''
    个人站点视图函数
    :param request:
    :param username:
    :param kwargs:
    :return:
    '''

    print("kwargs----", kwargs)  # 区分是站点页面还是站点下的页面
    print("request.post>>", request.GET)
    user = UserInfo.objects.filter(username=username).first()
    print("查找的username>>", user)

    # 判断用户是否存在
    if not user:
        return render(request, "not_found.html")
    blog = user.blog  # 这个一直是None，是因为当前对象的数据库中没有对应的数据
    print("当前的user的blog>>", blog)

    # 查询当前的登录人的所有的blog及其title
    # 查询当前站点对象
    article_list = Article.objects.filter(user=user)
    print("article_list", article_list)

    if kwargs:  # kwargs这是一个字典对象
        condition = kwargs.get("condition")
        print("condition>>>>>", condition)  # tag
        param = kwargs.get("param")
        print("param>>>", param)  # # 2012-2

        if condition == "category":
            article_list = article_list.filter(category__title=param)

        elif condition == "tag":
            article_list = article_list.filter(tags__title=param)
            print("article_list--------", article_list)
        else:
            year, month = param.split("/")

            article_list = article_list.filter(create_time__year=year, create_time__month=month)
            print("时间段的article_lsit>>", article_list)

    # 当前用户或则当前站点 所对应的所有文章
    # 基于对象查询
    # user 和aricle 为一对多的关系
    # 反向查询 按表名小写
    # article_list = user.article_set.all()
    # 查询每一个分类名称后面对应的文章数
    # Category和Article为一对多的关系
    # 这里将title 改为nid  是不是更好？
    # ret = Category.objects.annotate(c=Count("article__title")).values("title", "c")
    # print("ret>>", ret)

    # 查询当前站点的每一个分类名称以及对应的文章数；
    cate_list = Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list(
        "title", "c")
    # 查询当前站点的每一个标签名称以及对应的文章数
    tag_list = Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")

    # 查询当前站点每一个年月的名称以及对应的文章数
    date_list = Article.objects.filter(user=user).extra(
        select={"y_m_date": "date_format(create_time,'%%Y/%%m')"}).values("y_m_date").annotate(
        c=Count("nid")).values_list("y_m_date", "c")
    # print("个人站点的date_list文章",date_list)
    return render(request, "home_site.html", locals())


@login_required()
def get_query_data(request, username, article_id):
    user = UserInfo.objects.filter(username=username).first()
    # 判断用户是否存在
    if not user:
        return render(request, "not_found.html")

    # 查询当前站点对象
    blog = user.blog
    # 查询当前站点的每一个分类名称及其对应的文章数
    # 通过Category查article
    cate_list = Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list(
        "title", "c")
    tag_list = Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")
    date_list = Article.objects.filter(user=user).extra(
        select={"y_m_date": "date_format(create_time,'%%Y-%%m')"}).values("y_m_date").annotate(
        c=Count("nid")).values_list("y_m_date", "c")
    article_obj = Article.objects.filter(pk=article_id).first()
    # print("article_obj", article_obj)
    comment_list = Comment.objects.filter(user=user, artcile_id=article_id).all()

    return {"blog": blog, "cate_list": cate_list, "date_list": date_list, "tag_list": tag_list,
            "article_obj": article_obj,
            "comment_list": comment_list
            }


@login_required()
def user_article_detail(request, username, article_id):
    '''

    已经登陆的用户的view
    article_detail: 显示当前登录人的指定文章
    :param request:
    :param username:
    :param article_id:
    :return:
    '''
    user = UserInfo.objects.filter(username=username).first()
    print("文章详情页面的user对象,article_id》〉〉", user, article_id)
    if not user:
        article_id = article_id
        print("未登录的id", article_id)
        return render(request, 'not_found.html')

    blog = user.blog
    # 查找当前登录用户的所有文章,刚注册的用户肯定是没有的
    # user_article_list=Article.objects.filter(user=user).all()
    article_obj = Article.objects.filter(pk=article_id).first()
    comment_list = Comment.objects.filter(user=user, article_id=article_id).all()
    return render(request, 'user_article_detail.html', locals())


# 未登陆的详情页面的view
def article_detail(request, article_id):
    article_obj = Article.objects.filter(pk=article_id).first()
    comment_list = Comment.objects.filter(article_id=article_id).all()

    return render(request, 'article_detail.html', locals())


# 点赞视图函数
@login_required()
def digg(request):
    print(request.POST)
    # print("当前登陆人〉〉〉", request.user)
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))
    # print("is_up>>>", is_up)
    # 点赞的是当前登录人  提取当前登录人pk？？
    user_id = request.user.pk
    # print("user_id", user_id)
    # 查找当前登录用户 在当前文章和点赞表里的记录是存在
    obj = ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
    # print("当前点击的obj>>>", obj)  # 第一次点击的时候为None
    # print("当前点击的obj2222>>>", not obj)
    response = {"state": True}  # 判断是否重复点击
    # if not obj:  # 如果不存在，则创建
    if obj is None:  # 如果不存在，则创建
        # 前端点击一次，这里的ArticleUpDown 模型就创建一条数据，添加一次点赞数据
        ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
        # 查找当前文章这个对象
        queryset = Article.objects.filter(pk=article_id)
        if is_up:  # 如果前端点击的是 赞（True）
            # 则给这个文章的点赞字段总数 加一
            queryset.update(up_count=F("up_count") + 1)
        else:  # 如果前端点击的是 踩（False）
            # 则给当前文章的“踩” 字段总数加一
            queryset.update(down_count=F("down_count") + 1)
    else:  # 如果当前登录人已经点击了赞 或则 踩
        response["state"] = False
        response["handled"] = obj.is_up  # 判断是哪一个标签被点击
    # print("response-----------", response)
    return JsonResponse(response)


# 评论视图函数
@login_required()
def comment(request):
    print(request.POST)
    article_id = request.POST.get("article_id")
    pid = request.POST.get("pid")
    content = request.POST.get("content")
    user_id = request.POST.get("user_id")
    # print("评论的user_id", user_id)
    # print("评论的username>>>", request.POST.get("user"))

    # 评论和文章是多对一的关系，关键字段在Content评论端
    # 这个时候article_id 指的Comment这个表内部的article_id
    '''
    设置该函数中的所有数据库操作在同一个事物中，
    第一个数据库操作1即使成功保存到数据库中，只要第2个数据操作失败，那么所有该段代码所有涉及的数据库操作都会更改回滚到原来。
    '''
    # 事物操作绑定
    with transaction.atomic():
        comment_obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content,
                                             parent_comment_id=pid)
        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)

    response = {}
    response["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d %X")
    response["username"] = request.POST.get("user")
    response["content"] = content

    # 找当前article_id文章的title标题
    article_title = Article.objects.filter(nid=article_id).first().title
    # print("article_id.title,...",article_title)

    # 发送邮件
    '''
     # send_mail的参数分别是  邮件标题，
     邮件内容，发件箱(settings.py中设置过的那个)，
     收件箱列表(可以发送给多个人),
     失败静默(若发送失败，报错提示我们)
    '''
    send_mail(
        "您的文章%s新增了一条评论" % article_title,
        content,
        settings.EMAIL_HOST_USER,
        ["118@qq.com"]
    )

    return JsonResponse(response)


@login_required()
def get_coment_tree(request):
    '''
    评论树视图函数
    :param request:
    :return:
    '''
    article_id = request.GET.get("article_id")
    ret = list(Comment.objects.filter(article_id=article_id).values("pk", "content", "parent_comment__article_id"))

    return JsonResponse(ret, safe=False)


@login_required()
def upload(request):
    '''
    编辑器上传文件接收视图函数
    :param request:
    :return:
    '''
    print(request.FILES)
    img_obj = request.FILES.get("upload_img")
    path = os.path.join(settings.MEDIA_ROOT, "avatar", img_obj.name)
    with open(path, "wb") as f:
        for line in img_obj:
            f.write(line)

    response = {
        "error": 0,
        "url": "media/avatar/%s" % (img_obj.name)
    }
    return HttpResponse(json.dumps(response))


# 博客管理后台
@login_required()
def cn_backend(request):
    print("cnbankend 的当前用户〉〉", request.user)
    # 后台管理界面
    # 因该只能对自己的所属的文章进行增删改查
    # 通过user查找 article ，使用正向查询
    try:
        if request.user:
            article_list = Article.objects.filter(user=request.user).all()
            # print("后台管理界面的文章列表", article_list)
            return render(request, 'backend/backend.html', locals())

    except Exception as e:

        # ajax进行删除

        return redirect('/login/')


@login_required()
def add_article(request):
    '''
    后台新增文章
    :param request:
    :return:
    '''
    if request.method == "POST":
        print("增加的文章的〉〉", request.POST)
        user = request.user
        # print("user>>>", user)
        title = request.POST.get("title")
        content = request.POST.get("content")
        desc = request.POST.get("desc")
        soup = BeautifulSoup(content, "html.parser")  # #通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
        # print("soup>>",type(soup))
        # print(soup.find_all())
        for tag in soup.find_all():
            if tag.name == "script":
                tag.decompose()
        # 构建摘要数据，获取标签字符串的钱150个字符
        # desc = soup.text[0:150]
        desc = desc

        Article.objects.create(title=title, desc=desc, content=str(soup), user=request.user)
        return redirect('/cn_backend/')

    return render(request, "backend/add_article.html")


@login_required()
def delete_article(request):
    res = {"state": True}
    try:
        pk = request.GET.get("pk")
        print("删除文章的pk值〉〉", pk)
        Article.objects.filter(pk=pk).delete()

    except Exception as e:

        res["state"] = False

    return JsonResponse(res)


@login_required()
def edit_article(request, id):
    print("当前登陆的编辑用户", request.user)
    # get请求获取文章信息
    if request.method == "GET":
        # 获取文章标题
        edit_artice_obj = Article.objects.filter(pk=id).first()
        print("edit_artice_obj>>", edit_artice_obj)
        edit_artice_title = edit_artice_obj.title
        edit_artice_content = edit_artice_obj.content
        edit_artice_desc = edit_artice_obj.desc
        print("编辑的文章描述〉〉", edit_artice_desc)
        edit_artice_category = edit_artice_obj.category
        edit_artice_tags = edit_artice_obj.tags

        # 当前用户所拥有的所有的分类category
        category_list = Category.objects.filter(article__user=request.user).all()
        print("当前用户所拥有的所有的分类》", category_list)
        # 当前文章的分类名,但是有些用户是的当前文章是没有分类的
        article_category_title_obj = Category.objects.filter(article__title=edit_artice_obj.title).first()
        print("当前文章的分类名称>>", article_category_title_obj)
        if article_category_title_obj is None:
            article_category_title = u"次文章暂无分类名称"

        else:
            article_category_title = article_category_title_obj.title

        # 当前用户所有的标签tags
        tag_list = Tag.objects.filter(article__user=request.user).all()
        print("当前用户所有的标签tags>>", tag_list)

        # 当前文章的标签名，但是有些文章是没有标签的
        article_tag_title_obj = Tag.objects.filter(article__title=edit_artice_obj.title).first()
        print("当前文章的标签tags>>", article_tag_title_obj)
        if article_tag_title_obj is None:
            article_tag_title = u"次文章暂无标签"

        else:
            article_tag_title = article_tag_title_obj.title

        # print("=====>",edit_artice_title,edit_artice_desc,edit_artice_category,edit_artice_tags)
        print("=====>", type(article_category_title))

        return render(request, "backend/edit_article.html", locals())

    else:
        edit_artice = Article.objects.filter(pk=id).first()
        edit_title = request.POST.get("title")
        edit_desc = request.POST.get("desc")
        edit_content = request.POST.get("content")
        # edit_category = request.POST.get("category")
        # edit_tags = request.POST.get("tags")

        # article = Article.objects.filter(pk=id).update(title=edit_title, desc=edit_desc, category=edit_category,
        #                                                tags=edit_tags)
        # 防xss脚本攻击，过滤script标签
        soup = BeautifulSoup(edit_content, 'html.parser')
        for tag in soup.find_all():
            if tag.name == 'script':
                tag.decompose()

        # 构建摘要数据,获取标签字符串的文本前150个字符
        desc = soup.text[0:150]
        Article.objects.filter(pk=id).update(title=edit_title, desc=desc, content=str(soup),
                                             user=request.user)
        return redirect("/cn_backend/")


def test(request):
    if request.method == "GET":
        # 查看所有的文章
        articl_list = Article.objects.all()
        print("article_list>>", len(articl_list))
        print("article_list>>", articl_list)

        # 查看文章标题开头
        article_title = Article.objects.filter(Q(title__contains="git") | Q(create_time__gt="2020-04-20")).order_by(
            "create_time")
        print("title>>", article_title)
        return HttpResponse("test ok")


def dashboard(request):
    blogs_count = Blog.objects.count()
    article_count = Article.objects.count()
    context = {"blogs_count": blogs_count, "article_count": article_count}
    return render(request, "backend/dashboard.html", context)
