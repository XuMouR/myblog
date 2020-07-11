from django import template
from blog import models
from django.db.models import Count

register = template.Library()


@register.inclusion_tag(filename='classification.html')  # 这个装饰器式先加载这个html界面然后再去下面拿到数据进行渲染这个界面
def get_classification_style(username):
    print("request----------")
    user = models.UserInfo.objects.filter(username=username).first()
    print("user>>>>",user)
    blog = user.blog
    print("当前blog》〉",blog)
    # 查询当前用户的每一个分类名称及其对应的文章，在点击相应的分类后即可跳转查看
    cate_list = models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list(
        "title", "c")
    tag_list = models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")
    date_list = models.Article.objects.filter(user=user).extra(
        select={"y_m_date": "date_format(create_time,'%%Y-%%m')"}).values("y_m_date").annotate(
        c=Count("nid")).values_list("y_m_date", "c")
    print("tag_list",tag_list)
    print("date_list+++++++++++++",date_list)
    return {"blog": blog, "cate_list": cate_list, "date_list": date_list, "tag_list": tag_list,"user":user}
