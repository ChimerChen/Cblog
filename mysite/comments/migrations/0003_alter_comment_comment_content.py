# Generated by Django 4.1.7 on 2023-04-26 07:38

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_comment_parent_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
