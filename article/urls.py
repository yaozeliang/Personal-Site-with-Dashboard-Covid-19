from django.urls import path
from .views import article_list,article_detail,article_create,article_delete




app_name = 'article'

urlpatterns = [
    path('article-list',article_list,name="article_list"),
    path('article-detail/<int:id>/', article_detail, name='article_detail'),
    path('article-create/', article_create, name='article_create'),
    path('article-delete/<int:id>/', article_delete, name='article_delete'),
]

