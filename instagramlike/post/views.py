from django.http import HttpResponse
from django.shortcuts import render

from post.models import Post


def post_list(request):
    return render(
        request,
        'post/post_list.html',
        {'posts': Post.objects.all(), }
    )

def post_create(request):
    photo = request.FILES.get('photo')
    if request.method == 'POST' and photo:
        # print(request.POST)
        ## < QueryDict: {'csrfmiddlewaretoken': ['3bP8vMXgDmwdOlxOv5qb7iwcBDzZyvv94tBUFWTSl2MsQNXHcEeRJ8Au5tWwBGMZ']} >
        # print(request.FILES)
        ## < MultiValueDict: {'photo': [ < InMemoryUploadedFile: 디아블로 - 티리엘.gif(image / gif) >]} >
        photo = request.FILES['photo']
        post = Post.objects.create(photo=photo)
        return HttpResponse(f'<img src="{ post.photo.url }">')
    else:
        return render(
            request,
            'post/post_create.html'
        )



