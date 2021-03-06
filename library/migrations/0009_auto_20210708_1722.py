# Generated by Django 3.2.5 on 2021-07-08 11:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20201217_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='isbn',
        ),
        migrations.RemoveField(
            model_name='book',
            name='status',
        ),
        migrations.AlterField(
            model_name='book',
            name='department',
            field=models.CharField(choices=[('Computer', 'Computer'), ('Mechanical', 'Mechanical'), ('ENTC', 'ENTC'), ('Civil', 'Civil'), ('IT', 'IT'), ('other', 'other')], max_length=30),
        ),
        migrations.CreateModel(
            name='RequestBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.student')),
            ],
        ),
        migrations.CreateModel(
            name='BookCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.PositiveIntegerField(unique=True)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Not Available', 'Not Available')], default='Available', max_length=20, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
    ]
