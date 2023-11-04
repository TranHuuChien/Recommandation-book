# Generated by Django 2.2 on 2023-09-14 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=255)),
                ('author_slug', models.CharField(max_length=100, unique=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
