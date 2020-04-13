from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator


# Create your views here.
from django.http import HttpResponse
from .models import ArticlePost
import markdown
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@csrf_protect
def article_list(request):

    article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    
    articles = paginator.get_page(page)

    context = { 'articles': articles }
    return render(request, 'article/list.html', context)



@csrf_protect
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    if request.user!= article.author:
        article.total_views += 1
        article.save(update_fields=['total_views'])


    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.tables',
        'markdown.extensions.codehilite',
        ])

    context = { 'article': article }
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
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = { 'article_post_form': article_post_form }
        # 返回模板
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
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
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