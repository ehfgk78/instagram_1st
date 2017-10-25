from django.shortcuts import render

from post.models import Post


def post_list(request):
    return render(
        request,
        'post/post_list.html',
        {'posts': Post.objects.all(), }
    )
