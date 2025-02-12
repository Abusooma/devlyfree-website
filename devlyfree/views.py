from cloudinary import uploader
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
    articles = (
        Article.objects.select_related('categorie', 'author')
        .prefetch_related('tags')
        .filter(status='published')
        .order_by('-published_at')
    )

    context = {'articles': articles}

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
