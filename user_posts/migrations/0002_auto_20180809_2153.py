# Generated by Django 2.0.5 on 2018-08-09 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_posts',
            name='body',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='user_posts',
            name='url',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]