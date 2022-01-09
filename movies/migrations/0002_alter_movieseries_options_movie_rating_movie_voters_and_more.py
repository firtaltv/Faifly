# Generated by Django 4.0.1 on 2022-01-08 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movieseries',
            options={'verbose_name_plural': 'Movie Series'},
        ),
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='voters',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(related_name='genres', to='movies.Genre'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'movie')},
            },
        ),
    ]