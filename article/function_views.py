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



@csrf_protect
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    comment_form = CommentForm()

    # 过滤出所有的id比当前文章小的文章
    pre_article = ArticlePost.objects.filter(id__lt=article.id).order_by('-id')
    # 过滤出id大的文章
    next_article = ArticlePost.objects.filter(id__gt=article.id).order_by('id')

    # 取出相邻前一篇文章
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    # 取出相邻后一篇文章
    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None

    if request.user!= article.author:
        article.total_views += 1
        article.save(update_fields=['total_views'])


    # 将markdown语法渲染成html样式

    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        ]
    )
    article.body = md.convert(article.body)
    context = { 'article': article,
                'toc': md.toc,
                'comments': comments,
                'comment_form': comment_form,
                'pre_article': pre_article,
                'next_article': next_article}
    return render(request, 'article/detail.html', context)








def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['category'] != 'none':
                new_article.category = Category.objects.get(id=request.POST['category'])
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        categorys = Category.objects.all()
        context = { 'article_post_form': article_post_form, 'categorys': categorys }

        return render(request, 'article/create.html', context)