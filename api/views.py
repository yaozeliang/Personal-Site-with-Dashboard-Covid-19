from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse

from article.models import ArticlePost
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticlePostSerializer


@api_view(['GET'])
def apiOverview(request):

	api_urls = {
		'List':'/article-list/',
		'Detail View':'/article-detail/<str:pk>/',
		'Create':'/article-create/',
		'Update':'/article-update/<str:pk>/',
		'Delete':'/article-delete/<str:pk>/',
	}

	return Response(api_urls)


@api_view(['GET'])
def articleList(request):
    # data = serializers.serialize("json", SomeModel.objects.all())
	articles = ArticlePost.objects.all()
	serializer = ArticlePostSerializer(articles, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def articleDetail(request,pk):
	article = ArticlePost.objects.get(id=pk)
	serializer = ArticlePostSerializer(article, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def articleCreate(request):
	serializer = ArticlePostSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['POST'])
def articleUpdate(request,pk):
	article = ArticlePost.objects.get(id=pk)
	serializer = ArticlePostSerializer(instance=article,data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)


@api_view(['DELETE'])
def articleDelete(request,pk):
	article = ArticlePost.objects.get(id=pk)
	article.delete()
	return Response("Item has been removed successfully")