from django.contrib.syndication.views import Feed
from tinymce.models import HTMLField
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]

    def item_description(self, item):
        # Assuming item.body is an HTMLField instance
        return truncatewords_html(item.body, 30)

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.publish
