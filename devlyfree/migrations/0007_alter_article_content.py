# Generated by Django 5.1.5 on 2025-01-31 00:52

import django_quill.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devlyfree', '0006_category_tag_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
    ]
