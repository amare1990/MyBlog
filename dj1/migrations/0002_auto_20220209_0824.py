# Generated by Django 2.2.7 on 2022-02-09 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='owner',
        ),
    ]
