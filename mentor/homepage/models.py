from django.db import models
from django.conf import settings

# Choices for the role field
ROLE_CHOICES = [
    ('mentor', 'Mentor'),
    ('mentee', 'Mentee'),
]

# Predefined choices for skills and interests
SKILL_CHOICES = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('html', 'HTML'),
    ('javascript', 'JavaScript'),
    ('c++', 'C++'),
    ('sql', 'SQL'),
    ('machine_learning', 'Machine Learning'),
    ('data_science', 'Data Science'),
    # Add more skills as needed
]

INTEREST_CHOICES = [
    ('ai', 'Artificial Intelligence'),
    ('ml', 'Machine Learning'),
    ('data_science', 'Data Science'),
    ('design', 'Design'),
    ('web_development', 'Web Development'),
    ('software_engineering', 'Software Engineering'),
    ('networking', 'Networking'),
    ('cloud_computing', 'Cloud Computing'),
    # Add more interests as needed
]

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False, null=False)
    email = models.EmailField(unique=True,blank=False, null=False)
    phone_number = models.CharField(unique=True,max_length=10, blank=False, null=False)
    location = models.CharField(max_length=200, blank=False, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    skills = models.TextField(blank=False, null=False)  # Store skills as comma-separated list
    interests = models.TextField(blank=False, null=False)  # Store interests as comma-separated list
    bio = models.TextField(blank=False, null=False)
    linkedin_profile = models.URLField(blank=False, null=False)
    working_as = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return f"{self.name}'s Profile"


from django.db import models
from django.contrib.auth.models import User

class ConnectionRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')])

    def __str__(self):
        return f'Connection request from {self.sender.username} to {self.receiver.username}'
