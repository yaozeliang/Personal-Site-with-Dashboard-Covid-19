from rest_framework import serializers
from article.models import ArticlePost

class ArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArticlePost
        # fields=('author','title','category_id','tag_id','created','updated')
        fields="__all__"