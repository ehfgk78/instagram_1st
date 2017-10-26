from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from post.forms import PostForm, CommentForm
from post.models import Post, PostComment


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
            'post': get_object_or_404(Post, pk=post_pk)
        }
    )

def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # CommentForm에 바인딩된 request.POST
        comment_form = CommentForm(request.POST)
        # 유효성 검증
        if comment_form.is_valid():
            # PostComment 모델 인스턴스 생성
            PostComment.objects.create(
                post=post,
                content=comment_form.cleaned_data['content']
            )
            # 생성 후 Post의 detail 화면으로 이동
            return redirect('post:post_detail', post_pk=post_pk)
    else:
        # GET요청이면 빈 Form(댓글 내용을 입력할 수 있는)을 생성
        comment_form = CommentForm()
    # 폼이 포함된 입력 페이지를 보여주는 부분
    return render(
        request,
        'post/comment_create.html',
        context= {
            'form': comment_form,
        }
    )






