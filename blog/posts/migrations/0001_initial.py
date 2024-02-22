# Generated by Django 5.0.2 on 2024-02-20 14:06

import django.db.models.deletion
import django.utils.timezone
import hitcount.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('title', models.CharField(max_length=300)),
                ('text', models.TextField()),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('VD', 'Verified'), ('NV', 'NotVerified')], default='NV', max_length=2)),
                ('recommendation', models.CharField(choices=[('RCMD', 'Recommended'), ('NCMD', 'NotRecommended')], default='NCMD', max_length=4)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publish_time'],
            },
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]
