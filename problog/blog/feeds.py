import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'No Outlet - Official Blog'
    link = reverse_lazy('blog:post_list')
    description = 'Most recent publications at The Official No Outlet band Blog'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_pubdate(self, item):
        return item.publish
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    