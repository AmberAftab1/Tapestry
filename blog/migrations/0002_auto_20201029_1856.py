# Generated by Django 3.1.2 on 2020-10-29 18:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='author',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='poem',
            name='category',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='poem',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poem',
            name='description',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='poem',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poem',
            name='title',
            field=models.CharField(default=None, max_length=200),
        ),
    ]