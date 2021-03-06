from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from member.decorators import login_required
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


@login_required
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
            # Post.objects.create(
            #     author=request.user,
            #     photo=form.cleaned_data['photo'])
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
        else:
            return HttpResponse('Form invalid!')
    else:
        # GET 요청인 경우
        return render(
            request,
            'post/post_create.html',
            {
                'form': PostForm(),
            }
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
    if not request.user.is_authenticated:
        return redirect('member:login')
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied('작성자가 아닙니다.')


@login_required
def post_like_toggle(request, post_pk):
    if request.method == 'POST':
        # 토글한 사람 (요청한 사용자 )
        user = request.user
        # 토글된 post (Post 객체)
        post = get_object_or_404(Post, pk=post_pk)
        # toggle:  이미 '좋아요' 누른 것이면 '좋아요' 삭제 >> 아니면 '좋아요' 추가
        already_pressed = user.like_posts.filter(pk=post.pk)
        if already_pressed.exists():
            user.like_posts.remove(post)
        else:
            user.like_posts.add(post)
        # 토글 후 이동할 화면 (<< urls << templates)
        # path 있으면 해당 위치로, 없으면 상세 페이지로
        next_path = request.GET.get('next', ' ').strip()
        if next_path:
            return redirect(next_path)
    return redirect('post:post_detail', post_pk=post_pk)


def comment_create(request, post_pk):
    # print('request: ', request)
    # print(request.GET)
    # print(request.POST)

    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # CommentForm에 바인딩된 request.POST
        comment_form = CommentForm(request.POST)
        # 유효성 검증
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            # GET parameter로 'next'값이 전달되면
            # 공백을 없애고 다음에 redirect될 주소로 지정
            next_path = request.GET.get('next', ' ').strip()
            if next_path:
                return redirect(next_path)
            # 생성 후 Post의 detail 화면으로 이동
            return redirect('post:post_detail', post_pk=post_pk)
    else:
        # GET 요청이면 빈 Form(댓글 내용을 입력할 수 있는)을 생성
        comment_form = CommentForm()
    # 폼이 포함된 입력 페이지를 보여주는 부분
    return render(
        request,
        'post/comment_create.html',
        context={
            'form': comment_form,
        }
    )


def comment_delete(request, comment_pk):
    # 삭제한 댓글의 post로 가기 위한 작업
    next_path = request.GET.get('next', ' ').strip()

    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_path: return redirect(next_path)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다.')
