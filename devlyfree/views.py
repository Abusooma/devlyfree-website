from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Service



def home_view(request):
    services = Service.objects.all()
    return render(request, 'devlyfree/index.html', {'services': services})

def about_view(request):
    return render(request, 'devlyfree/about.html')


def service_view(request, slug=None):
    services = Service.objects.all()
    selected_slug = slug
    print(selected_slug)
    if slug:
        service = get_object_or_404(Service, slug=slug)
        all_services = Service.objects.all()
        context = {
            'service': service,
            'all_services': all_services,
            'selected_slug': selected_slug
        }
        return render(request, 'devlyfree/service_detail.html', context=context)
    return render(request, 'devlyfree/services.html', {'services': services})


def porfolio_view(request):
    return render(request, 'devlyfree/portfolio.html')

def blog_view(request):
    return render(request, 'devlyfree/blog.html')

def contact_view(request):
    return render(request, 'devlyfree/contact.html')
