# Generated by Django 5.0.4 on 2024-04-16 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password_hash',
            new_name='password',
        ),
    ]
