

from django.contrib import admin
from django.urls import path,include
# from article import urls

# 新引入的模块
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('article.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('password-reset/', include('password_reset.urls')),
    path('comment/', include('comment.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('notice/', include('notice.urls')),
    path('accounts/', include('allauth.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
