from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from cloudinary.models import CloudinaryField


class Service(models.Model):
    ICON_CHOICES = [
        ('bi bi-briefcase', 'Icône pour Création Web'),
        ('bi bi-card-checklist', 'Icône pour E-commerce'),
        ('bi bi-bar-chart', 'Icône pour SEO & Marketing'),
        ('bi bi-binoculars', 'Icône pour Applications Web'),
        ('bi bi-brightness-high', 'Icône pour UI/UX Design'),
        ('bi bi-calendar4-week', 'Icône pour Maintenance')
    ]

    ICON_COLOR_CHOICES = [
        ('#f57813', 'Orange - Création Web'),
        ('#15a04a', 'Vert - E-commerce'),
        ('#d90769', 'Rose - SEO & Marketing'),
        ('#15bfbc', 'Turquoise - Applications Web'),
        ('#f5cf13', 'Jaune - UI/UX Design'),
        ('#1335f5', 'Bleu - Maintenance')
    ]

    titre = models.CharField(max_length=250)
    petite_description = models.TextField()
    grande_description = models.TextField()
    slug = AutoSlugField(
        populate_from='titre', 
        editable=True, 
        always_update=True,
        unique=True,
        blank=True,
        null=True
    )
    image = CloudinaryField(blank=True, null=True)
    icone = models.CharField(max_length=25, choices=ICON_CHOICES)
    icone_couleur = models.CharField(max_length=7, choices=ICON_COLOR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.titre)

    
# Les models pour le blog

class Category(models.Model):
    nom = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from='nom',
        editable=True,
        always_update=True,
        blank=True,
        null=True
    )
    meta_title = models.CharField(
        max_length=60, blank=True, 
        help_text="Title tag pour le SEO - Idéalement entre 50 et 60 caractères"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True, 
        help_text="Meta description pour le SEO - Idéalement entre 150 et 160 caractères"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.nom)

class Tag(models.Model):
    nom = models.CharField(max_length=50)
    slug = AutoSlugField(
        populate_from='nom',
        editable=True,
        blank=True,
        null=True,
        always_update=True
    )
    description = models.TextField(blank=True)
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Title tag pour le SEO - Idéalement entre 50 et 60 caractères"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Meta description pour le SEO - Idéalement entre 150 et 160 caractères"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nom)
    

class Article(models.Model):
    STATUS = [
        ('draft','brouillon'),
        ('published', 'publié')
    ]

    titre = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    featured_image = CloudinaryField()
    featured_image_alt = models.CharField(
        max_length=100,
        help_text="Texte alternatif pour l'image principale (SEO)"
    )
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    # LES CHAMPS POUR LE SEO
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Title tag pour le SEO - Idéalement entre 50 et 60 caractères"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Meta description pour le SEO - Idéalement entre 150 et 160 caractères"
    )

    meta_keywords = models.CharField(
        max_length=200,
        blank=True,
        help_text="Mots-clés séparés par des virgules"
    )
    canonical_url = models.URLField(
        blank=True,
        help_text="URL canonique si différente de l'URL par défaut"
    )

    # Champs pour Open Graph ....


    def __str__(self):
        return str(self.titre)
    
