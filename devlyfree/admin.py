from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from django import forms
from .models import Service
from django.utils.html import format_html


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
   compressed_fields = ['grande_description']

   list_display = ['titre', 'icon_preview', 'petite_description']
   list_display_links = ['titre', 'icon_preview']
   search_fields = ['titre']
   readonly_fields = ['icon_live_preview']

   fieldsets = (
       ('Informations principales', {
           'fields': (
               'titre',
               'slug',
               ('icone', 'icon_live_preview', 'icone_couleur'),
               'image',
           ),
           'classes': ('wide',)
       }),
       ('Contenu', {
           'fields': ('petite_description', 'grande_description'),
           'classes': ('wide',)
       }),
   )

   def icon_preview(self, obj):
       return format_html(
           '<div style="font-size:10px;"><i class="{}" style="color:{}"></i> {}</div>',
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

   class Media:
       css = {
           'all': [
               'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
           ]
       }
