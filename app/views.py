from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )

    def post_detail(request, post):
    # get post object
        post = get_object_or_404(Post, slug=post)
        # list of active parent comments
        comments = post.comments.filter(active=True, parent__isnull=True)
        if request.method == 'POST':
            # comment has been added
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                parent_obj = None
                # get parent comment id from hidden input
                try:
                    # id integer e.g. 15
                    parent_id = int(request.POST.get('parent_id'))
                except:
                    parent_id = None
                # if parent_id has been submitted get parent_obj id
                if parent_id:
                    parent_obj = Comment.objects.get(id=parent_id)
                    # if parent object exist
                    if parent_obj:
                        # create replay comment object
                        replay_comment = comment_form.save(commit=False)
                        # assign parent_obj to replay comment
                        replay_comment.parent = parent_obj
                # normal comment
                # create comment object but do not save to database
                new_comment = comment_form.save(commit=False)
                # assign ship to the comment
                new_comment.post = post
                # save
                new_comment.save()
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            comment_form = CommentForm()
        return render(request,
                    'core/detail.html',
                    {'post': post,
                    'comments': comments,
                    'comment_form': comment_form})

class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))