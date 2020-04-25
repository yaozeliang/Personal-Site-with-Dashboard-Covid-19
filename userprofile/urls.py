from django.urls import path
from .views import user_login,user_logout,user_delete,profile_edit,RegisterView,user_register



app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    # path('register/', RegisterView.as_view(), name='register'),

    path('delete/<int:id>/', user_delete, name='delete'),
    path('edit/<int:id>/', profile_edit, name='edit'),
]
