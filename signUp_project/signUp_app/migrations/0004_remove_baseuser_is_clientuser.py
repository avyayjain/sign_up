# Generated by Django 3.2.7 on 2022-01-13 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signUp_app', '0003_auto_20220112_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='is_clientuser',
        ),
    ]
