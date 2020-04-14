from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [

    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
    path('delete-comment/<int:article_id>/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]