# Generated by Django 3.2.5 on 2021-07-18 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_alter_requestbook_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
    ]
