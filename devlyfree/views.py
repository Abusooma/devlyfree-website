from django.core.exceptions import RequestDataTooBig
from .models import Article, Category, Tag, Comment, Service
from .forms import CommentForm
from django.db.models import Count, Q
from cloudinary import uploader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
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
        .select_related('categorie', 'author')
        .prefetch_related('tags')
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

    # Contexte (sans les données du sidebar)
    context = {
        'articles': articles,
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

    # Formulaire initial
    comment_form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'comments_count': comments_count,
        'comment_form': comment_form
    }

    context.update(request.seo_data)

    return render(request, 'devlyfree/blog_detail.html', context)


def add_comment_view(request, slug):
    """Vue pour gérer l'ajout de commentaires via HTMX"""
    article = get_object_or_404(
        Article.objects.filter(status='published'), slug=slug)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user if request.user.is_authenticated else None

            # Gestion du commentaire parent (pour les réponses)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment

            comment.save()

            # Après avoir sauvegardé le commentaire
            comments = article.comments.filter(
                approved=True).order_by('-created_at')
            comments_count = comments.count()

            # Pour HTMX: renvoyer juste le fragment mis à jour
            context = {
                'article': article,
                'comments': comments,
                'comments_count': comments_count,
                'comment_form': CommentForm(),  # Nouveau formulaire vide
                'comment_success': True
            }

            return render(request, 'devlyfree/partials/comments_section.html', context)

    # En cas d'erreur, renvoyer le formulaire avec les erreurs
    comments = article.comments.filter(approved=True).order_by('-created_at')
    comments_count = comments.count()

    context = {
        'article': article,
        'comments': comments,
        'comments_count': comments_count,
        'comment_form': comment_form
    }

    return render(request, 'devlyfree/partials/comments_section.html', context)


def contact_view(request):
    context = {}
    if hasattr(request, 'seo_data') and request.seo_data is not None:
        context.update(request.seo_data)
    return render(request, 'devlyfree/contact.html', context)


def blog_sidebar(request):
    # Requêtes optimisées pour les widgets
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

    tags = Tag.objects.annotate(
        article_count=Count(
            'articles',
            filter=Q(articles__status='published')
        )
    ).order_by('-article_count')[:20]  # Limiter aux 20 tags les plus utilisés

    recent_articles = (
        Article.objects
        .select_related('author')
        .filter(status='published')
        .order_by('-published_at')[:5]
    )

    context = {
        'categories': categories,
        'tags': tags,
        'recent_articles': recent_articles,
        'request': request,  # Pour transmettre les paramètres de requête
    }

    return render(request, 'devlyfree/partials/blog_sidebar.html', context)


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

    return JsonResponse(
        {
            'error': 'Méthode non autorisée'
        },
        status=405
    )
