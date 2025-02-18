from django.http import JsonResponse
from django.core.exceptions import RequestDataTooBig
from .models import PageSEO, Service
import logging

logger = logging.getLogger(__name__)


class SEOMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, 'resolver_match') and request.resolver_match:
            url_name = request.resolver_match.url_name

            if url_name:
                try:
                    if url_name == 'service_detail' and view_kwargs:
                        slug = view_kwargs.get('slug')
                        seo_data = Service.objects.get(slug=slug)
                    else:
                        seo_data = PageSEO.objects.get(page=url_name)

                    request.seo_data = {
                        'meta_title': seo_data.meta_title,
                        'meta_description': seo_data.meta_description,
                        'meta_keywords': seo_data.meta_keywords
                    }
                   
                except (PageSEO.DoesNotExist, Service.DoesNotExist):
                    request.seo_data = None
        else:
            logger.debug("No resolver_match or URL name found")

        return None


class RequestSizeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except RequestDataTooBig:
            return JsonResponse({
                'error': 'Le fichier uploadé dépasse la taille maximale autorisée'
            }, status=413)
