# Generated by Django 3.2.16 on 2024-06-17 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('created_at',), 'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('created_at',), 'verbose_name': 'местоположение', 'verbose_name_plural': 'Местоположения'},
        ),
    ]
