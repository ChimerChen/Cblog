# Generated by Django 4.1.7 on 2023-04-18 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_categor_tag_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Categor',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
