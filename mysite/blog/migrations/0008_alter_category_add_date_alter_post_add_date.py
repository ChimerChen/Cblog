# Generated by Django 4.1.7 on 2023-04-28 09:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='add_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='add_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='添加时间'),
        ),
    ]
