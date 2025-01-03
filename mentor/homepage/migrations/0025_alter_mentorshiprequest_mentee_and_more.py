# Generated by Django 5.0.7 on 2024-12-27 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0024_alter_mentorshiprequest_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorshiprequest',
            name='mentee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentee_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mentorshiprequest',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
