# Generated by Django 3.1.7 on 2022-05-01 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0022_ratingnotifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingnotifier',
            name='book_to_rate',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='library.issuebook'),
        ),
    ]
