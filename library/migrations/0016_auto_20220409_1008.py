# Generated by Django 3.1.7 on 2022-04-09 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_student_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='department',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
