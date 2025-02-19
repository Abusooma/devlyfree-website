from django.core.exceptions import RequestDataTooBig
from .models import Article, Category, Tag
from django.contrib import messages
from .forms import CommentForm
from django.db.models import Count, Q
from cloudinary import uploader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Service, Article, Category, Tag
import logging


logger = logging.getLogger(__name__)


def home_view(request):
    services = Service.objects.all()
    recent_articles = (
        Article.objects
        .select_related('author')
        .filter(status='published')
        .order_by('-published_at')[:5]
    )

    context = {'services': services, 'recent_articles': recent_articles}

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
        'recent_articles': recent_articles
    }

    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)

    return render(request, 'devlyfree/blog.html', context)


def blog_detail_view(request, slug):
    # Récupérer l'article avec ses relations
    article = get_object_or_404(
        Article.objects
        .select_related('categorie', 'author')
        .prefetch_related('tags', 'comments__author')
        .filter(status='published'),
        slug=slug
    )

    # Récupérer les commentaires de l'article
    comments = article.comments.filter(approved=True).order_by('-created_at')
    comments_count = comments.count()

    # Articles récents pour le widget sidebar
    recent_articles = (
        Article.objects
        .select_related('author')
        .filter(status='published')
        .exclude(id=article.id)  # Exclure l'article courant
        .order_by('-published_at')[:5]
    )

    # Catégories pour le widget
    categories = (
        Category.objects
        .annotate(
            article_count=Count(
                'articles',
                filter=Q(articles__status='published')
            )
        )
        .order_by('nom')
    )

    # Tags pour le widget
    tags = Tag.objects.annotate(
        article_count=Count(
            'articles',
            filter=Q(articles__status='published')
        )
    ).order_by('-article_count')[:20]


    # Gestion du formulaire de commentaire
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user if request.user.is_authenticated else None
            comment.save()
            messages.success(
                request, 'Votre commentaire a été soumis avec succès et est en attente de modération.')
            return redirect('blog_detail', slug=slug)
    else:
        comment_form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'comments_count': comments_count,
        'comment_form': comment_form,
        'recent_articles': recent_articles,
        'categories': categories,
        'tags': tags,
    }

    # Mise a jour du contexte pour l'ajout du dictionnaire des meta données
    context.update(request.seo_data)

    return render(request, 'devlyfree/blog_detail.html', context)


def contact_view(request):
    context = {}
    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/contact.html', context)


@csrf_exempt
def upload_image(request):
    try:
        if request.method == "POST":
            if 'image' not in request.FILES:
                return JsonResponse({
                    'error': 'Aucun fichier image trouvé dans la requête'
                }, status=400)

            image = request.FILES['image']

            # Vérification de la taille
            if image.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
                return JsonResponse({
                    'error': f'L\'image est trop volumineuse. Taille maximum: {settings.DATA_UPLOAD_MAX_MEMORY_SIZE/1024/1024}MB'
                }, status=413)

            try:
                result = uploader.upload(image)
                return JsonResponse({
                    'url': result['secure_url']
                })
            except Exception as e:
                return JsonResponse({
                    'error': f'Erreur lors de l\'upload: {str(e)}'
                }, status=500)

    except RequestDataTooBig:
        return JsonResponse({
            'error': f'L\'image est trop volumineuse. Taille maximum: {settings.DATA_UPLOAD_MAX_MEMORY_SIZE/1024/1024}MB'
        }, status=413)
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur inattendue: {str(e)}'
        }, status=500)

    return JsonResponse({
        'error': 'Méthode non autorisée'
    }, status=405)
