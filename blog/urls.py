from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('blog/list/', views.post_list, name='post_list'),
    re_path(r'^tag/(?P<tag_slug>[\w-]+)/$',views.post_list, name='post_list_by_tag'),
    re_path(r'^detail/(?P<post_slug>[\w-]+)/$', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
