# Generated by Django 3.2.4 on 2021-06-12 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foody', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_name',
            field=models.CharField(default='Recipe', max_length=255),
            preserve_default=False,
        ),
    ]
