# Generated by Django 5.0.2 on 2024-02-21 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_views_alter_tag_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='views',
        ),
    ]
