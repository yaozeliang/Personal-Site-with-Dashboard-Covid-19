from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_protect
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


def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    search = request.GET.get('search')
    order = request.GET.get('order')
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
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'category': category,
        'tag': tag,
    }

    return render(request, 'article/list.html', context)



@csrf_protect
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)

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
    context = { 'article': article,'toc': md.toc,'comments': comments }
    return render(request, 'article/detail.html', context)

@csrf_protect
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
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

@csrf_protect
@login_required(login_url='/userprofile/login/')
def article_update(request, id):

    article = ArticlePost.objects.get(id=id)

    if request.user!= article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)

        if article_post_form.is_valid():
            if request.POST['category']!='none':
                article.category = Category.objects.get(id=request.POST['category'])
            else:
                article.category = None
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()

            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        categorys = Category.objects.all()
        context = { 
            'article': article, 
            'categorys': categorys,
        }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


@csrf_protect
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)

        if request.user!= article.author:
            return HttpResponse("对不起，你无权修改这篇文章。")
        else:
            article.delete()
            return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")



# class ArticleCreateView(CreateView): # new
#     model = ArticlePost
#     template_name = 'article/create_crispy.html'
#     fields = ['title','body']

#     def form_valid(self, form): # new
#         form.instance.author = self.request.user
#         return super().form_valid(form)