# Generated by Django 5.0.7 on 2024-12-26 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0017_remove_userprofile_interests_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='name',
            field=models.CharField(choices=[('ai', 'Artificial Intelligence'), ('ml', 'Machine Learning'), ('data_science', 'Data Science'), ('design', 'Design'), ('web_development', 'Web Development'), ('software_engineering', 'Software Engineering'), ('networking', 'Networking'), ('cloud_computing', 'Cloud Computing')], max_length=100),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(choices=[('python', 'Python'), ('java', 'Java'), ('html', 'HTML'), ('javascript', 'JavaScript'), ('c++', 'C++'), ('sql', 'SQL'), ('machine_learning', 'Machine Learning'), ('data_science', 'Data Science'), ('ai', 'Artificial Intelligence'), ('cloud_computing', 'Cloud Computing'), ('web_development', 'Web Development'), ('software_engineering', 'Software Engineering'), ('design', 'Design')], max_length=100),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='skills',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='interests',
            field=models.ManyToManyField(to='homepage.interest'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='skills',
            field=models.ManyToManyField(to='homepage.skill'),
        ),
    ]