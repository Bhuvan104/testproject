# Generated by Django 4.2.4 on 2023-09-10 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_character_product_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='character',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='character',
        ),
        migrations.DeleteModel(
            name='movie',
        ),
    ]