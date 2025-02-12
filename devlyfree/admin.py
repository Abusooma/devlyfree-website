from .models import Service, Category, Tag, Article, PageSEO
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html


@admin.register(PageSEO)
class PageSEOAdmin(ModelAdmin):
    list_display = ['page_display', 'meta_title', 'seo_status']
    list_display_links = ['page_display']
    search_fields = ['meta_title', 'meta_description']

    fieldsets = (
        ('Page', {
            'fields': ('page',),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('wide',)
        }),
    )

    def page_display(self, obj):
        return obj.get_page_display()
    page_display.short_description = "Page"

    def seo_status(self, obj):
        status = []
        if not obj.meta_title:
            status.append('❌ Meta Title')
        if not obj.meta_description:
            status.append('❌ Meta Description')
        if not obj.meta_keywords:
            status.append('❌ Keywords')

        if not status:
            return format_html('<span style="color: green;">✓ SEO Complet</span>')
        return format_html('<span style="color: red;">{}</span>', ', '.join(status))
    seo_status.short_description = 'Statut SEO'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('page',)
        return ()


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    compressed_fields = ['grande_description']

    list_display = ['titre', 'icon_preview',
                    'image_preview_list']
    list_display_links = ['titre', 'icon_preview']
    search_fields = ['titre']
    readonly_fields = ['icon_live_preview', 'image_preview']

    fieldsets = (
        ('Informations principales', {
            'fields': (
                'titre',
                'slug',
                ('icone', 'icon_live_preview', 'icone_couleur'),
                ('image', 'image_preview'),
            ),
            'classes': ('wide',)
        }),
        ('Contenu', {
            'fields': ('petite_description', 'grande_description'),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords'
            ),
            'classes': ('wide',),
            'description': "Optimisation pour les moteurs de recherche"
        }),
    )

    def icon_preview(self, obj):
        return format_html(
            '<div style="font-size:17px;"><i class="{}" style="color:{}"></i> {}</div>',
            obj.icone, obj.icone_couleur, obj.titre
        )
    icon_preview.short_description = "Service"

    def icon_live_preview(self, obj):
        if obj:
            return format_html(
                '<div style="font-size:20px;margin:10px 0;"><i class="{}" style="color:{}"></i></div>',
                obj.icone, obj.icone_couleur
            )
        return ""
    icon_live_preview.short_description = "Aperçu de l'icône"

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                """
                <div style="margin: 10px 0;">
                    <img src="{}" alt="{}" style="max-width: 400px; height: auto; 
                        border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <p style="color: #666; margin-top: 5px; font-size: 0.9em;">
                        Texte alternatif: <span style="font-style: italic;">{}</span>
                    </p>
                </div>
                """,
                obj.image.url,
                obj.titre,
                obj.titre
            )
        
    image_preview.short_description = "Aperçu de l'image"

    def image_preview_list(self, obj):
        if obj and obj.image:
            return format_html(
                """
                <div style="text-align: center;">
                    <img src="{}" alt="{}" style="max-width: 80px; height: auto; 
                        border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                </div>
                """,
                obj.image.url,
                obj.titre
            )
        
    image_preview_list.short_description = "Image"

    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
            ]
        }

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    compressed_fields = ['nom']
    list_display = ['nom', 'post_count', 'seo_status']
    list_display_links = ['nom']
    search_fields = ['nom']
    readonly_fields = ['post_count']

    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug'),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('wide',)
        }),
    )

    def post_count(self, obj):
        return obj.article_set.count()
    post_count.short_description = "Nombre d'articles"

    def seo_status(self, obj):
        status = []
        if not obj.meta_title:
            status.append('❌ Meta Title')
        if not obj.meta_description:
            status.append('❌ Meta Description')

        if not status:
            return format_html('<span style="color: green;">✓ SEO Complet</span>')
        return format_html('<span style="color: red;">{}</span>', ', '.join(status))
    seo_status.short_description = 'Statut SEO'

    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
            ]
        }


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    compressed_fields = ['nom']
    list_display = ['nom', 'post_count', 'seo_status']
    list_display_links = ['nom']
    search_fields = ['nom']

    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug', 'description'),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('wide',)
        }),
    )

    def post_count(self, obj):
        return obj.article_set.count()
    post_count.short_description = "Nombre d'articles"

    def seo_status(self, obj):
        status = []
        if not obj.meta_title:
            status.append('❌ Meta Title')
        if not obj.meta_description:
            status.append('❌ Meta Description')

        if not status:
            return format_html('<span style="color: green;">✓ SEO Complet</span>')
        return format_html('<span style="color: red;">{}</span>', ', '.join(status))
    seo_status.short_description = 'Statut SEO'
    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
            ]
        }


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    compressed_fields = ['titre']
    list_display = ['titre', 'author', 'categorie', 'status', 'published_at', 'seo_status']
    list_filter = ['status', 'categorie', 'author', 'created_at']
    search_fields = ['titre', 'content', 'meta_title', 'meta_description']
    filter_horizontal = ['tags']
    readonly_fields = ['featured_image_preview']

    fieldsets = (
        ('Informations principales', {
            'fields': (
                'titre',
                'slug',
                'author',
                'status',
                'published_at'
            ),
            'classes': ('wide',)
        }),
        ('Contenu', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Médias', {
            'fields': ('featured_image', 'featured_image_preview', 'featured_image_alt'),
            'classes': ('wide',)
        }),
        ('Catégorisation', {
            'fields': ('categorie', 'tags'),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'canonical_url'
            ),
            'classes': ('collapse', 'wide',)
        }),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                """
                <div style="margin: 10px 0;">
                    <img src="{}" alt="{}" style="max-width: 400px; height: auto; 
                        border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <p style="color: #666; margin-top: 5px; font-size: 0.9em;">
                        Texte alternatif: <span style="font-style: italic;">{}</span>
                    </p>
                </div>
                """,
                obj.featured_image.url,
                obj.featured_image_alt or "Image de l'article",
                obj.featured_image_alt or "Non défini"
            )
        return format_html(
            '<div style="color: #999; font-style: italic; margin: 10px 0;">Aucune image</div>'
        )
    featured_image_preview.short_description = "Aperçu de l'image"

    def featured_image_preview_list(self, obj):
        if obj.featured_image:
            return format_html(
                """
                <div style="text-align: center;">
                    <img src="{}" alt="{}" style="max-width: 100px; height: auto; 
                        border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                </div>
                """,
                obj.featured_image.url,
                obj.featured_image_alt or "Image de l'article"
            )
        return format_html(
            '<span style="color: #999; font-style: italic;">Aucune image</span>'
        )
    featured_image_preview_list.short_description = "Image"

    def seo_status(self, obj):
        status = []
        if not obj.meta_title:
            status.append('❌ Meta Title')
        if not obj.meta_description:
            status.append('❌ Meta Description')
        if not obj.meta_keywords:
            status.append('❌ Keywords')

        if not status:
            return format_html('<span style="color: green;">✓ SEO Complet</span>')
        return format_html('<span style="color: red;">{}</span>', ', '.join(status))
    seo_status.short_description = 'Statut SEO'

    class Media:
        js = (
            'https://cdn.quilljs.com/1.3.6/quill.min.js',
        )
        css = {
            'all': (
                'https://cdn.quilljs.com/1.3.6/quill.snow.css',
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
            )
        }
