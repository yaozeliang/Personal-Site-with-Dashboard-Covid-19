from django.urls import path
# from .views import article_list,article_detail,article_create,article_update,article_safe_delete
from .views import ArticleListView,article_create,article_update,article_safe_delete, ArticleDetailView,ArticleCreateView


app_name = 'article'

urlpatterns = [
    path('',ArticleListView.as_view(),name="article_list"),
    # path('article-detail/<int:id>/', article_detail, name='article_detail'),
    path('article-detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    # path('article-create/', article_create, name='article_create'),
    path('article-update/<int:id>/', article_update, name='article_update'),
    path('article-safe-delete/<int:id>/',article_safe_delete,name='article_safe_delete'),
    path('article-create/', ArticleCreateView.as_view(), name='article_create'),
]



