# Generated by Django 3.0.6 on 2024-12-05 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20240711_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.CharField(max_length=64, verbose_name='作者'),
        ),
    ]