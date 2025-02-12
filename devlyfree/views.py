from .models import Article, Category, Tag
from django.db.models import Count
from cloudinary import uploader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Service, Article, Category, Tag


import logging

logger = logging.getLogger(__name__)


def home_view(request):
    services = Service.objects.all()
    context = {'services': services}

    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/index.html', context)

def about_view(request):
    context = {}
    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/about.html', context)


def service_view(request):
    services = Service.objects.all()
    context = {'services': services}
    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/services.html', context)


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug)
    all_services = Service.objects.all()
    context = {
        'service': service,
        'all_services': all_services,
        'selected_slug': slug
    }
    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/service_detail.html', context)


def porfolio_view(request):
    context = {}
    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/portfolio.html', context)


def blog_view(request):
    # Requête de base optimisée pour les articles avec leurs relations
    articles_list = (
        Article.objects
        .select_related('categorie', 'author')  # Pour les relations ForeignKey
        .prefetch_related('tags')  # Pour la relation ManyToMany
        .filter(status='published')
        .order_by('-published_at')
    )

    # Recherche
    query = request.GET.get('q')
    if query:
        articles_list = articles_list.filter(titre__icontains=query)

    # Filtrage par catégorie
    category = request.GET.get('category')
    if category:
        articles_list = articles_list.filter(categorie__slug=category)

    # Filtrage par tag
    tag = request.GET.get('tag')
    if tag:
        articles_list = articles_list.filter(tags__slug=tag)

    # Pagination
    paginator = Paginator(articles_list, 6)  # 6 articles par page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # Requêtes optimisées pour les widgets
    categories = (
        Category.objects
        .annotate(
            article_count=Count(
                'articles',
                filter=Article.objects.filter(status='published').values('id')
            )
        )
        .order_by('nom')
    )

    tags = Tag.objects.annotate(
        article_count=Count(
            'articles',
            filter=Article.objects.filter(status='published').values('id')
        )
    ).order_by('-article_count')[:20]  # Limiter aux 20 tags les plus utilisés

    recent_articles = (
        Article.objects
        .select_related('author')
        .filter(status='published')
        .order_by('-published_at')[:5]
    )

    # Contexte
    context = {
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'recent_articles': recent_articles,
    }

    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)

    return render(request, 'devlyfree/blog.html', context)


def blog_detail_view(request):
    return render(request, 'devlyfree/blog_detail.html')


def contact_view(request):
    context = {}
    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/contact.html', context)


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        if 'image' in request.FILES:
            image = request.FILES['image']
            try:
                result = uploader.upload(image)
                return JsonResponse({
                    'url': result['secure_url']
                })
            except Exception as e:
                print(f"Upload error: {str(e)}")
                return JsonResponse({
                    'error': str(e)
                }, status=500)
        else:
            print("No image file found in request")
            return JsonResponse({
                'error': 'No image file found in request'
            }, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
