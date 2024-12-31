# forms.py
from django import forms
from .models import UserProfile, SKILL_CHOICES, INTEREST_CHOICES

class UserProfileForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(
        choices=SKILL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone_number', 'location', 'role', 'skills', 'interests', 'bio', 'linkedin_profile', 'working_as']

    def clean_skills(self):
        # Convert the list of selected skills into a comma-separated string
        return ', '.join(self.cleaned_data['skills'])

    def clean_interests(self):
        # Convert the list of selected interests into a comma-separated string
        return ', '.join(self.cleaned_data['interests'])

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance:
            # Pre-select values in skills and interests from the instance
            if self.instance.skills:
                self.initial['skills'] = self.instance.skills.split(', ')
            if self.instance.interests:
                self.initial['interests'] = self.instance.interests.split(', ')
