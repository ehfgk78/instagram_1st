from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from post.forms import PostForm, CommentForm
from post.models import Post, PostComment


def post_list(request):
    return render(
        request,
        'post/post_list.html',
        {
            'posts': Post.objects.all(),
            'comment_form': CommentForm(),
        }
    )


def post_create(request):
    # login하지 않는  사용자는 login View로
    if not request.user.is_authenticated:
        return redirect('member:login')

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
            post = Post.objects.create(
                author=request.user,
                photo=form.cleaned_data['photo'])
            return redirect('post:post_list')
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
            'post': get_object_or_404(Post, pk=post_pk),
            'comment_form': CommentForm()
        }
    )

def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
    else:
        raise PermissionDenied

def comment_create(request, post_pk):
    print('request: ', request)
    print(request.GET)
    print(request.POST)

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
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            # 생성 후 Post의 detail 화면으로 이동
            return redirect('post:post_detail', post_pk=post_pk)
    else:
        # GET요청이면 빈 Form(댓글 내용을 입력할 수 있는)을 생성
        comment_form = CommentForm()
    # 폼이 포함된 입력 페이지를 보여주는 부분
    return render(
        request,
        'post/comment_create.html',
        context={
            'form': comment_form,
        }
    )
