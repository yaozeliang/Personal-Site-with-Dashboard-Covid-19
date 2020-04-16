from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm
from . models import Comment

from notifications.signals import notify
from django.contrib.auth.models import User

# 文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()

            # 新增代码，给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )

            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")


@login_required(login_url='/userprofile/login/')
def delete_comment(request, article_id, comment_id):
    article = get_object_or_404(ArticlePost, id=article_id)
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user!= comment.user:
        return HttpResponse("对不起，你无权删除这篇评论。")
    else:
        comment.delete()
        return redirect(article)

