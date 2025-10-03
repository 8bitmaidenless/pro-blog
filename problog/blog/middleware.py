from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from taggit.models import Tag

from blog.models import Post


def subdomain_blog_tags_middleware(get_response):
    def middleware(request):
        host_parts = request.get_host().split('.')
        if len(host_parts) > 2 and host_parts[0] != 'www':
            tag = get_object_or_404(Tag, slug=host_parts[0])
            tag_url = reverse(
                'blog:post_list_by_tag',
                args=[tag.slug]
            )
            url = '{}://{}{}'.format(
                request.scheme,
                '.'.join(host_parts[1:]),
                tag_url
            )
            return redirect(url)
        response = get_response(request)
        return response
    return middleware
