from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('a-propos-de-nous/', views.about_view, name='about'),
    path('nos-services/', views.service_view, name='services'),
    path('nos-services/<str:slug>/',
         views.service_detail_view, name='service_detail'),
    path('porfolio/', views.porfolio_view, name='portfolio'),
    path('blog/', views.blog_view, name='blog'),
    # Mettre sidebar AVANT le pattern avec slug
    path('blog/sidebar/', views.blog_sidebar, name='blog_sidebar'),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('blog/<slug:slug>/comment/', views.add_comment_view, name='add_comment'),
    path('contact/', views.contact_view, name='contact'),
    path('quill/upload/', views.upload_image, name='quill_upload'),
]
