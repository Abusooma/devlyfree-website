from .models import Service


def services_processor(request):
    return {'services': Service.objects.all()[:4]}
