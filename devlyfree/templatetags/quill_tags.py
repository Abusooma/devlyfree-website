from django import template
from bs4 import BeautifulSoup
from django_quill.fields import FieldQuill

register = template.Library()


@register.filter(name='format_quill_content')
def format_quill_content(content):
    if not content:
        return ''

    if isinstance(content, FieldQuill):
        content = content.html

    if not content:
        return ''

    soup = BeautifulSoup(content, 'html.parser')

    # Formatter les images
    for img in soup.find_all('img'):
        # Classes de base
        img_classes = ['article-image']

        # Déterminer la taille basée sur la largeur naturelle de l'image
        # ou vous pouvez ajouter un attribut data-size dans l'éditeur Quill
        width = img.get('width', '')
        if width:
            width = int(width)
            if width <= 300:
                img_classes.append('img-small')
            elif width <= 500:
                img_classes.append('img-medium')
            else:
                img_classes.append('img-large')
        else:
            # Taille par défaut si pas de width
            img_classes.append('img-medium')

        # Mettre à jour les classes
        img['class'] = ' '.join(img_classes)

        # Ajouter des attributs data pour plus de flexibilité
        img['data-size'] = img_classes[-1].replace('img-', '')

        # Créer le wrapper
        if img.parent.name == 'p':
            wrapper = soup.new_tag('div')
            wrapper['class'] = f'image-wrapper {img_classes[-1]}-wrapper'
            img.parent.replace_with(wrapper)
            wrapper.append(img)

            # Ajouter une légende si nécessaire
            if img.get('alt'):
                caption = soup.new_tag('figcaption')
                caption.string = img.get('alt')
                wrapper.append(caption)

    return str(soup)
