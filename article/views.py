from django.shortcuts import render,get_object_or_404,redirect
from  django.urls import  reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView,DetailView,DeleteView
from django.views.generic.edit import CreateView,UpdateView
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


from django.core.exceptions import PermissionDenied # new
from django.contrib.auth.mixins import LoginRequiredMixin 


class ArticleListView(ListView):
    model=ArticlePost
    context_object_name = 'articles'
    template_name = 'article/list.html'

    categories = Category.objects.all()
    all_tags= ArticlePost.tags.all()

    def get_queryset(self):
        search =self.request.GET.get("search")   
        order = self.request.GET.get("order")            
        category = self.request.GET.get("category") 
        tag = self.request.GET.get("tag")
        article_list = ArticlePost.objects.all()

        if search:
            article_list = article_list.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
        else:
            search = ''

        if category is not None and category.isdigit():
            article_list = article_list.filter(category=category)

        
        if tag and tag != 'None':
            article_list = article_list.filter(tags__name__in=[tag])

        if order=='total_views':
            article_list = article_list.order_by('-total_views')

        paginator = Paginator(article_list, 4)
        page = self.request.GET.get('page')
        articles = paginator.get_page(page)
        return articles


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        context['all_tags'] = self.all_tags
        return context



class ArticleDetailView(DetailView):
    model=ArticlePost
    context_object_name = 'article'
    template_name = 'article/detail.html'

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        ])

    comment_form = CommentForm()

    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        # if request.user!= article.author:
        #     article.total_views += 1
        #     article.save(update_fields=['total_views'])
        obj.total_views += 1
        obj.save(update_fields=['total_views'])
        obj.body= self.md.convert(obj.body)
        return obj

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        pre_article = self.model.objects.filter(id__lt=self.kwargs['pk']).order_by('-id')
        next_article = self.model.objects.filter(id__gt=self.kwargs['pk']).order_by('id')
        if pre_article.count() > 0:
            pre_article = pre_article[0]
        else:
            pre_article = None

        if next_article.count() > 0:
            next_article = next_article[0]
        else:
            next_article = None

        comments = Comment.objects.filter(article=self.kwargs['pk'])
        

        context['toc'] = self.md.toc
        context['comments'] = comments
        context['comment_form'] = self.comment_form
        context['pre_article'] = pre_article
        context['next_article'] = next_article
        return context





class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = ArticlePost
    # fields = ['title','avatar','category','tags','body']
    login_url = 'login'
    form_class=ArticlePostForm
    template_name = 'article/create_crispy.html'

 
    def get_initial(self, *args, **kwargs):
        initial = super(ArticleCreateView, self).get_initial(**kwargs)
        initial['title']='Your Title'
        return initial


    def form_valid(self, form):
        new_article = form.save(commit=False)
        new_article.author = self.request.user
        new_article.save()
        form.save_m2m()
        return super().form_valid(form)
        


# @login_required(login_url='/userprofile/login/')
class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    model = ArticlePost
    login_url = 'login'
    # fields = ['title','avatar','category','tags','body']
    form_class=ArticlePostForm
    template_name = 'article/update_crispy.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponse("Sorry, you don't have right to update")
            # raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
        

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = ArticlePost
    login_url = 'login'
    template_name = 'article/detail.html'
    success_url = reverse_lazy("article:article_list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponse("Sorry, you don't have right to update")
            # raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)










# class ArticleCreateView(CreateView): # new
#     model = ArticlePost
#     template_name = 'article/create_crispy.html'
#     fields = ['title','body']

#     def form_valid(self, form): # new
#         form.instance.author = self.request.user
#         return super().form_valid(form)


