from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CreatePostForm
import datetime


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10


class PostDetailView(generic.DetailView):
    model = Post


def get_nick(user):
    conn_user = user
    conn_profile = User.objects.get(email=conn_user)
    nick = conn_profile.username
    return nick


@login_required
def post_write(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            conn_user = request.user
            conn_profile = get_object_or_404(User, email=conn_user)
            nick = conn_profile.username
            new_post = form.save(commit=False)
            new_post.writer = nick
            new_post.save()
            messages.info(request, '글을 성공적으로 올렸습니다!')
            return HttpResponseRedirect(reverse_lazy('board_index'))
    else:
        form = CreatePostForm()

    return render(request, 'blog/write_post.html', {'form': form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk = pk)
    context = {'post': post}
    # 저장 과정
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        conn_user = request.user
        nick = get_nick(conn_user)

        if nick != post.writer:
            messages.info(request, '권한이 없습니다!')
            return render(request, 'blog/post_detail.html', context=context)

        if form.is_valid():
            post = form.save(commit=False)
            post.post_date = datetime.datetime.now()
            post.save()
            messages.info(request, '성공적으로 수정되었습니다!')
            return render(request, 'blog/post_detail.html', context=context)
    # 전송 폼
    else:
        title = post.post_title
        content = post.post_contents
        form = CreatePostForm(initial={'post_title': title, 'post_contents': content,})

    return render(request, 'blog/write_post.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('board_index')


@login_required
def comment_write(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        context = {'post': post}
        content = request.POST.get('content')

        conn_user = request.user
        conn_profile = User.objects.get(email=conn_user)

        if not content:
            messages.info(request, 'You dont write anything....')
            return render(request, 'blog/post_detail.html', context=context)

        Comment.objects.create(post=post, comment_writer=conn_profile, comment_contents=content)
        return render(request, 'blog/post_detail.html', context=context)


@login_required
def comment_delete(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)

    context = {'post' : post,}
    content = request.POST.get('content')

    conn_user = request.user
    conn_profile = User.objects.get(email=conn_user)

    if conn_profile != comment.comment_writer:
        messages.info(request, '권한이 없습니다!')
        return render(request, 'blog/post_detail.html', context=context)

    comment.delete()
    return render(request, 'blog/post_detail.html', context=context)


#
# class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
#     model = Post
#     success_url = reverse_lazy('blog:board_index')
#
#     def get_queryset(self):
#         conn_user = self.request.user
#         nick = get_nick(conn_user)
#         return self.model.objects.filter(writer=nick)