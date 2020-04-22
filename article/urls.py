from django.urls import path
# from .views import article_list,article_detail,article_create,article_update,article_safe_delete
from .views import ArticleListView,ArticleDetailView,ArticleCreateView,ArticleUpdateView,ArticleDeleteView,ArchiveView


app_name = 'article'

urlpatterns = [
    path('',ArticleListView.as_view(),name="article_list"),
    path('article-detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article-update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('article-delete/<int:pk>/',ArticleDeleteView.as_view(),name='article_safe_delete'),
    path('article-create/', ArticleCreateView.as_view(), name='article_create'),
    path('article-archives/<int:year>/<int:month>/', ArchiveView.as_view(), name='archive'),
]



