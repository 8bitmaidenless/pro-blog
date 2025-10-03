from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request):
    posts = Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
        }
    )


# def post_detail(request, id):
#     post = get_object_or_404(
#         Post,
#         id=id,
#         status=Post.Status.PUBLISHED
#     )
#     return render(
#         request,
#         'blog/post/detail.html',
#         {
#             'post': post,
#         }
#     )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post
    )
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
        }
    )