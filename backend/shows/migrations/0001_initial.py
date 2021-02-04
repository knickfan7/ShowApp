# Generated by Django 3.1.5 on 2021-01-31 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shows',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('image_path', models.TextField()),
                ('summary', models.TextField()),
                ('trailer', models.TextField()),
                ('country', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
                ('duration', models.CharField(max_length=20)),
                ('language', models.TextField()),
            ],
        ),
    ]
