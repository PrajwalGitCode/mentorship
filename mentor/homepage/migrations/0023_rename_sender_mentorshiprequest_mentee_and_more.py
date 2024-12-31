# Generated by Django 5.0.7 on 2024-12-27 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0022_alter_mentorshiprequest_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentorshiprequest',
            old_name='sender',
            new_name='mentee',
        ),
        migrations.RenameField(
            model_name='mentorshiprequest',
            old_name='receiver',
            new_name='mentor',
        ),
        migrations.RemoveField(
            model_name='mentorshiprequest',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='mentorshiprequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=20),
        ),
    ]
