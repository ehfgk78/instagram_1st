from django.http import HttpResponse
from django.shortcuts import render

from post.forms import PostForm
from post.models import Post


def post_list(request):
    return render(
        request,
        'post/post_list.html',
        {'posts': Post.objects.all(), }
    )

def post_create(request):
    # photo = request.FILES.get('photo')
    if request.method == 'POST':
        # print(request.POST)
        ## < QueryDict: {'csrfmiddlewaretoken': ['3bP8vMXgDmwdOlxOv5qb7iwcBDzZyvv94tBUFWTSl2MsQNXHcEeRJ8Au5tWwBGMZ']} >
        # print(request.FILES)
        ## < MultiValueDict: {'photo': [ < InMemoryUploadedFile: 디아블로 - 티리엘.gif(image / gif) >]} >

        # photo = request.FILES['photo']
        # post = Post.objects.create(photo=photo)
        form = PostForm(request.POST, request.FILES)
        # form 생성과정에서 전달된 데이터들이 Form의 모든 field들에 유효한지 검사
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(
                photo=form.cleaned_data['photo'])
            return HttpResponse(f'<img src="{ post.photo.url }">')
        else:
            return HttpResponse('Form invalid!')
    else:
        return render(
            request,
            'post/post_create.html'
        )

def post_detail(request, post_pk):
    return render(
        request,
        'post/post_detail.html',
        {
            'post': Post.objects.get(pk=post_pk)
        }
    )



