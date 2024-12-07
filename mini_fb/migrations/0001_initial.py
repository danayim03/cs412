# Generated by Django 5.1.3 on 2024-12-04 20:47

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('city', models.TextField()),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('image_url', models.URLField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends1', to='mini_fb.profile')),
                ('profile2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends2', to='mini_fb.profile')),
            ],
        ),
        migrations.CreateModel(
            name='StatusMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_messages', to='mini_fb.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(blank=True, upload_to='')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mini_fb.statusmessage')),
            ],
        ),
    ]
