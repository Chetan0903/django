# Generated by Django 3.1.7 on 2022-04-09 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_auto_20220409_1009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='department',
            new_name='domain',
        ),
    ]
