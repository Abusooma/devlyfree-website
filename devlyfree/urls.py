from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('a-propos-de-nous/', views.about_view, name='about'),
    path('nos-services/', views.service_view, name='services'),
    path('nos-services/<str:slug>/', views.service_detail_view, name='service_detail'),
    path('porfolio/', views.porfolio_view, name='portfolio'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/blog-details', views.blog_detail_view, name='blog_detail'),
    path('contact/', views.contact_view, name='contact'),
]