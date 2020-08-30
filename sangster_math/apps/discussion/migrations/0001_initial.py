# Generated by Django 3.0.6 on 2020-08-29 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('members', models.ManyToManyField(related_name='chat_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=400)),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_set', to='discussion.Chat')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]