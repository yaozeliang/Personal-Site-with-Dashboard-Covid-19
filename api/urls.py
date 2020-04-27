from django.urls import path,include
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.apiOverview, name="api_overview"),
	path('article-list/', views.articleList, name="api_article_list"),
	path('article-create/', views.articleCreate, name="api_article_create"),
	path('article-detail/<str:pk>/', views.articleDetail, name="api_article_detail"),
	path('article-update/<str:pk>/', views.articleUpdate, name="api_article_update"),
	path('article-delete/<str:pk>/', views.articleDelete, name="api_article_delete"),	
]