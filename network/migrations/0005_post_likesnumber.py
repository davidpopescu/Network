# Generated by Django 4.0.6 on 2022-10-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likesNumber',
            field=models.IntegerField(default=0),
        ),
    ]