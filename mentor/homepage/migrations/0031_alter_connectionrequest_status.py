# Generated by Django 5.0.7 on 2024-12-27 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0030_connectionrequest_delete_mentorshiprequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], max_length=10),
        ),
    ]