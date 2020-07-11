
# from ..models import Article, ArticleUpDown, Article2Tag, Comment, Category, UserInfo, Blog, Tag
import copy


class Pagination(object):
    def __init__(self, current_page, all_count, request, per_page=10, max_pager_num=11):
        """
        :param current_page:当前页
        :param all_count: 所有数据总数
        :param request:
        :param per_page: 每一页显示的数据条数
        :param max_pager_num: 这个页面最多显示的页码数量
        num_pages:总数据所分页的总页面数
        """
        # 减少小于的时候，让其展示页面1的数据
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1 or current_page is None:
            current_page = 1

        self.current_page = current_page
        self.all_count = all_count
        self.per_page = per_page  # 每一页显示的数据条数
        print("分页器当前的页面〉〉",current_page)

        # 计算总页数
        # print("计算",all_count,per_page)
        num_pages, tmp = divmod(all_count, per_page)  # 多的一条数据也展示一页
        print("多少页》〉",num_pages,tmp)
        if tmp:
            num_pages += 1
        self.num_pages = num_pages

        self.max_pager_num = max_pager_num  # 最大显示的页数
        self.page_count_half = int((self.max_pager_num - 1) / 2)  # 最多显示页数的一半
        self.params = copy.deepcopy(request.GET)
        # print("urlencode", self.params.urlencode())

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page


    @property
    def end(self):
        return self.current_page * self.per_page


    def page_html(self):
        # 如果总页数小于11

        if self.num_pages <= self.max_pager_num:
            pager_start = 1
            pager_end = self.num_pages + 1
        else:
            if self.current_page <= self.page_count_half:
                pager_start = 1
                pager_end = self.max_pager_num + 1
            # 当前页大于5
            elif (self.current_page + self.page_count_half) > self.num_pages:
                pager_start = self.num_pages - self.max_pager_num + 1
                pager_end = self.num_pages + 1
            else:
                pager_start = self.current_page - self.page_count_half
                pager_end = self.current_page + self.page_count_half + 1

        page_html_list = []

        # 首页 上一页标签
        self.params["page"] = 1
        first_page = '<nav aria-label="Page navigation"><ul class="pagination"><li><a href="?%s">首页</a></li>' % (
            self.params.urlencode(),)

        page_html_list.append(first_page)
        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            self.params["page"] = self.current_page - 1
            prev_page = '<li><a href="?%s">上一页</a></li>' % (self.params.urlencode(),)
        page_html_list.append(prev_page)

        # 每一页显示页码
        for i in range(pager_start, pager_end):
            self.params["page"] = i
            if i == self.current_page:
                temp = '<li class="active"><a href="?%s">%s</a></li>' % (self.params.urlencode(), i,)
                # print("1>>",temp)
            else:
                temp = '<li><a href="?%s">%s</a></li>' % (self.params.urlencode(), i)
                # print("2>>", temp)

            page_html_list.append(temp)

        # 尾页 下一页
        self.params["page"] = self.current_page + 1
        if self.current_page >= self.num_pages:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?%s">下一页</a></li>' % (self.params.urlencode(),)
        page_html_list.append(next_page)

        self.params["page"] = self.num_pages
        last_page = '<li><a href="?%s">尾页</a></li></ul></nav>' % (self.params.urlencode())
        page_html_list.append(last_page)
        # print("=======", ''.join(page_html_list))
        return ''.join(page_html_list)
