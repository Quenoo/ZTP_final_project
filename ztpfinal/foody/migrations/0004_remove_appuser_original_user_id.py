# Generated by Django 3.2.4 on 2021-06-15 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foody', '0003_appuser_original_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='original_user_id',
        ),
    ]