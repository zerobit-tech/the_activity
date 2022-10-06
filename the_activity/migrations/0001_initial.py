# Generated by Django 4.0.7 on 2022-09-23 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='action time')),
                ('target_id', models.TextField(blank=True, null=True, verbose_name='object id')),
                ('change_message', models.TextField(blank=True, verbose_name='change message')),
                ('ip_address', models.CharField(blank=True, max_length=20, null=True, verbose_name='IP Address')),
                ('user_agent', models.CharField(blank=True, max_length=200, null=True, verbose_name='User agent')),
                ('path', models.CharField(blank=True, max_length=256, null=True, verbose_name='Path')),
                ('read', models.BooleanField(default=False)),
                ('target_ct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_object', to='contenttypes.contenttype', verbose_name='content type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'ordering': ['-action_time'],
            },
        ),
    ]
