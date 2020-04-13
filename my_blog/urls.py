

from django.contrib import admin
from django.urls import path,include
# from article import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('password-reset/', include('password_reset.urls')),
    
]


