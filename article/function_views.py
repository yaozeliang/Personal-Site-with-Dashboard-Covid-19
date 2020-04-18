from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
from .models import ArticlePost,Category
import markdown
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from comment.models import Comment
from comment.forms import CommentForm



def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    categories = Category.objects.all()
    all_tags= ArticlePost.tags.all()
    # 用户搜索逻辑

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if category is not None and category.isdigit():
        article_list = article_list.filter(category=category)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order=='total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'category': category,
        'tag': tag,
        'categories':categories,
        'all_tags':all_tags,

    }

    return render(request, 'article/list.html', context)