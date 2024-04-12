from django.shortcuts import render, get_object_or_404
from .models import Post, PostComment, HomeBanner, AboutMe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


# Create your views here.
def index(request):
    main = get_object_or_404(HomeBanner)
    about_me = get_object_or_404(AboutMe)
    context = {
        'main': main,
        'about_me': about_me
    }
    return render(request, 'blog/index/index.html', context)


def about_me_page(request):
    return render(request, 'blog/index/about.html')


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug, )
        post_list = post_list.filter(tags__in=[tag])
    for post in post_list:
        post.total_comments = post.comments.count()
    # Pagination with 3 post pre page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    all_tags = Tag.objects.filter(post__in=post_list).distinct()
    context = {
        'posts': posts,
        'tag': tag,
        'all_tags': all_tags

    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]
    comment_count = comments.count()
    # Check if 'INSERT_IMAGE_HERE' exists in the content
    if 'INSERT_IMAGE_HERE' in post.body:
        # Split the body into two parts based on the 'INSERT_IMAGE_HERE' marker
        body_parts = post.body.split('INSERT_IMAGE_HERE')
        content_before_image = body_parts[0]  # Content before the image
        content_after_image = body_parts[1]  # Content after the image
        has_image = True
    else:
        content_before_image = post.body
        content_after_image = None
        has_image = False
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
        'comment_count': comment_count,
        'content_before_image': content_before_image,
        'content_after_image': content_after_image,
        'has_image': has_image,
    }
    return render(request, 'blog/post/2.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'codepython3.12@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, 'blog/post/share.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'blog/post/comment.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query), ).filter(
                similarity__gt=0.1).order_by('-similarity')
    context = {
        'form': form,
        'query': query,
        'results': results
    }
    return render(request, 'blog/post/search.html', context)
