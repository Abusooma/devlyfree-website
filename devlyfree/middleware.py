from .models import PageSEO
import logging

logger = logging.getLogger(__name__)


class SEOMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # À ce stade, resolver_match devrait être disponible
        if hasattr(request, 'resolver_match') and request.resolver_match:
            url_name = request.resolver_match.url_name

            if url_name:
                try:
                    seo_data = PageSEO.objects.get(page=url_name)

                    request.seo_data = {
                        'meta_title': seo_data.meta_title,
                        'meta_description': seo_data.meta_description,
                        'meta_keywords': seo_data.meta_keywords
                    }
                   
                except PageSEO.DoesNotExist:
                    request.seo_data = None
        else:
            logger.debug("No resolver_match or URL name found")

        return None  # Important : retourne None pour continuer le traitement
