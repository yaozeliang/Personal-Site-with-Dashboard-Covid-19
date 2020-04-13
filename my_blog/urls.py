

from django.contrib import admin
from django.urls import path,include
# from article import urls

# 新引入的模块
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('password-reset/', include('password_reset.urls')),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
