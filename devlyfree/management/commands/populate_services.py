from django.core.management.base import BaseCommand
from django.conf import settings
from devlyfree.models import Service


class Command(BaseCommand):
    help = "Peuple la base de donnée avec les Services"

    def handle(self, *args, **options):
        services_data = [
            {
                'titre': 'Création de Sites Web',
                'petite_description': """Notre équipe d'experts combine créativité et expertise technique
                                        pour créer des solutions digitales sur mesure qui répondent parfaitement à vos objectifs commerciaux. 
                                        Nous vous accompagnons dans chaque étape de votre transformation digitale.""",
                'grande_description': """<h3>Solutions Web Professionnelles pour Développer Votre Présence en
                                        Ligne
                                    </h3>
                                    <p>Notre équipe d'experts combine créativité et expertise technique
                                        pour créer des solutions digitales sur mesure qui répondent parfaitement à vos objectifs commerciaux. 
                                        Nous vous accompagnons dans chaque étape de votre transformation digitale.
                                    </p>
                                    <p>Notre équipe d'experts combine créativité et expertise technique pour créer des solutions digitales sur mesure 
                                        qui répondent parfaitement à vos objectifs commerciaux. Nous vous accompagnons dans chaque étape de votre transformation digitale.</p>
                                    <ul>
                                        <li><i class="bi bi-check-circle"></i><span>Sites web responsifs optimisés pour tous les appareils</span></li>
                                        <li><i class="bi bi-check-circle"></i><span>Solutions e-commerce complètes avec gestion des stocks</span></li>
                                        <li><i class="bi bi-check-circle"></i><span>Stratégies SEO pour améliorer votre visibilité en ligne</span></li>
                                    </ul>
                                    <p>Nous mettons en œuvre les meilleures pratiques de développement web et utilisons les technologies les plus récentes 
                                        pour garantir des solutions performantes, sécurisées et évolutives.</p>
                                    <p>Notre approche collaborative nous permet de comprendre précisément vos besoins et de vous proposer des solutions adaptées 
                                        à votre secteur d'activité.</p>""",
                'icone': 'bi bi-briefcase',
                'icone_couleur': '#f57813',
                'cloudinary_image': 'v1737932801/site_web_zqehxl.jpg'
            },
            {
                'titre': 'Solutions E-commerce',
                'petite_description': """Développement de boutiques en ligne performantes intégrant gestion des stocks, paiements sécurisés et interfaces administrateur intuitives pour gérer votre activité efficacement.""",
                'grande_description': '''<h3>Solutions E-commerce</h3>
<p>Développement de boutiques en ligne performantes intégrant gestion des stocks, paiements sécurisés et interfaces administrateur intuitives pour gérer votre activité efficacement.</p>
<p>Développez votre activité en ligne avec une solution e-commerce performante et sécurisée.</p>
       <ul>
           <li><i class="bi bi-check-circle"></i><span>Gestion des stocks intégrée et automatisée</span></li>
           <li><i class="bi bi-check-circle"></i><span>Systèmes de paiement sécurisés</span></li>
           <li><i class="bi bi-check-circle"></i><span>Interface d'administration intuitive</span></li>
       </ul>
       <p>Notre expertise en e-commerce vous garantit une boutique en ligne performante et facile à gérer.</p>''',
                'icone': 'bi bi-card-checklist',
                'icone_couleur': '#15a04a',
                'cloudinary_image': 'v1737932794/solution_ecom_ona8vq.jpg'
            },
            {
                'titre': 'SEO & Marketing Digital',
                'petite_description': """Optimisation de votre visibilité en ligne grâce à des stratégies SEO efficaces et des campagnes marketing ciblées pour attirer et convertir plus de clients potentiels.""",
                'grande_description': '''<h3>SEO & Marketing Digital</h3>
<p>Optimisation de votre visibilité en ligne grâce à des stratégies SEO efficaces et des campagnes marketing ciblées pour attirer et convertir plus de clients potentiels.</p>
<p>Améliorez votre visibilité en ligne avec nos stratégies SEO et marketing digital sur mesure.</p>
       <ul>
           <li><i class="bi bi-check-circle"></i><span>Optimisation pour les moteurs de recherche</span></li>
           <li><i class="bi bi-check-circle"></i><span>Stratégies de contenu performantes</span></li>
           <li><i class="bi bi-check-circle"></i><span>Analyses et rapports détaillés</span></li>
       </ul>
       <p>Nos experts en marketing digital vous accompagnent pour maximiser votre présence en ligne.</p>''',
                'icone': 'bi bi-bar-chart',
                'icone_couleur': '#d90769',
                'cloudinary_image': 'v1737932793/seo_oem3st.jpg'

            },
            {
                'titre': 'Applications Web Sur Mesure',
                'petite_description': """Développement d'applications web personnalisées répondant à vos besoins spécifiques, avec des fonctionnalités avancées et une interface utilisateur intuitive.""",
                'grande_description': '''<h3>Applications Web Sur Mesure</h3>
<p>Développement d'applications web personnalisées répondant à vos besoins spécifiques, avec des fonctionnalités avancées et une interface utilisateur intuitive.</p>
<p>Des applications web sur mesure pour répondre à vos besoins spécifiques.</p>
       <ul>
           <li><i class="bi bi-check-circle"></i><span>Solutions personnalisées et évolutives</span></li>
           <li><i class="bi bi-check-circle"></i><span>Interfaces utilisateur intuitives</span></li>
           <li><i class="bi bi-check-circle"></i><span>Intégration avec vos systèmes existants</span></li>
       </ul>
       <p>Notre expertise technique vous garantit des applications performantes et adaptées à vos besoins.</p>''',
                'icone': 'bi bi-binoculars',
                'icone_couleur': '#15bfbc',
                'cloudinary_image': 'v1737932799/app_web_xyxyui.jpg'
            },
            {
                'titre': 'UI/UX Design',
                'petite_description': """Création d'interfaces utilisateur modernes et attractives, avec une attention particulière portée à l'expérience utilisateur pour maximiser l'engagement et la conversion.""",
                'grande_description': '''<h3>UI/UX Design</h3>
<p>Création d'interfaces utilisateur modernes et attractives, avec une attention particulière portée à l'expérience utilisateur pour maximiser l'engagement et la conversion.</p>
<p>Des interfaces utilisateur modernes et intuitives pour une expérience utilisateur optimale.</p>
       <ul>
           <li><i class="bi bi-check-circle"></i><span>Design moderne et attractif</span></li>
           <li><i class="bi bi-check-circle"></i><span>Expérience utilisateur optimisée</span></li>
           <li><i class="bi bi-check-circle"></i><span>Tests utilisateurs et optimisations</span></li>
       </ul>
       <p>Nos designers créent des interfaces qui engagent vos utilisateurs et augmentent vos conversions.</p>''',
                'icone': 'bi bi-brightness-high',
                'icone_couleur': '#f5cf13',
                'cloudinary_image': 'v1737932816/ui_ux_awvz6t.jpg'
            },
            {
                'titre': 'Maintenance & Support',
                'petite_description': """Service de maintenance continue et support technique réactif pour garantir le bon fonctionnement de vos solutions digitales et leur évolution dans le temps.""",
                'grande_description': '''<h3>Maintenance & Support</h3>
<p>Service de maintenance continue et support technique réactif pour garantir le bon fonctionnement de vos solutions digitales et leur évolution dans le temps.</p>
<p>Un accompagnement continu pour garantir la performance de vos solutions digitales.</p>
       <ul>
           <li><i class="bi bi-check-circle"></i><span>Support technique réactif</span></li>
           <li><i class="bi bi-check-circle"></i><span>Mises à jour régulières</span></li>
           <li><i class="bi bi-check-circle"></i><span>Monitoring et optimisations</span></li>
       </ul>
       <p>Notre équipe assure un suivi continu pour maintenir et faire évoluer vos solutions digitales.</p>''',
                'icone': 'bi bi-calendar4-week',
                'icone_couleur': '#1335f5',
                'cloudinary_image': 'v1737932793/m_and_su_zfec5z.jpg'
            }
        ]

        if Service.objects.exists():
            self.stdout.write(self.style.WARNING(
                'Des services existent déjà dans la base de données'))
            return
        

        try:
            for data in services_data:
                service = Service(
                    titre=data['titre'],
                    petite_description=data['petite_description'],
                    grande_description=data['grande_description'],
                    icone=data['icone'],
                    icone_couleur=data['icone_couleur']
                )

                service.image = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{data['cloudinary_image']}"
                service.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Service "{data["titre"]}" créé avec succès'))       

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Une erreur est survenue {e}"))
