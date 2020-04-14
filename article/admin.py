from django.contrib import admin

# Register your models here.
from .models import ArticlePost,Category

admin.site.register(ArticlePost)
admin.site.register(Category)

