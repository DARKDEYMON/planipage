# Generated by Django 4.1.1 on 2022-09-19 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0004_remove_publicacion_tipos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='tipo',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='tipo',
            field=models.ManyToManyField(to='noticias.tipo'),
        ),
    ]
