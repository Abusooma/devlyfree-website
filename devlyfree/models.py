from django.db import models
from autoslug import AutoSlugField
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

    



