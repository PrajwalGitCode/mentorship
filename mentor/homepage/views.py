from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, ConnectionRequest, INTEREST_CHOICES, SKILL_CHOICES
from .forms import UserProfileForm
from django.contrib.auth.models import User


# Home View
def Home(request):
    return render(request, "home.html")


# Login View
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, "login.html", {'form': form})
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {'form': form})


# Signup View
def signup_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {'form': form})


# Logout View
def logout_user(request):
    logout(request)
    return redirect('home')


# Profile View
@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    # Check the connection status in both directions
    connection_status = None
    # Check if the current user has sent a request and it has been accepted
    if ConnectionRequest.objects.filter(sender=request.user, receiver=user_profile.user, status='accepted').exists():
        connection_status = 'connected'
    # Check if the current user has received a request and it has been accepted
    elif ConnectionRequest.objects.filter(sender=user_profile.user, receiver=request.user, status='accepted').exists():
        connection_status = 'connected'
    # Check if the current user has sent a request but it is still pending
    elif ConnectionRequest.objects.filter(sender=request.user, receiver=user_profile.user, status='pending').exists():
        connection_status = 'sent'
    # Check if the current user has received a request but it is still pending
    elif ConnectionRequest.objects.filter(sender=user_profile.user, receiver=request.user, status='pending').exists():
        connection_status = 'received'

    return render(request, 'user_profile.html', {
        'user_profile': user_profile,
        'connection_status': connection_status,
    })

# Create Profile View
@login_required
def create_profile(request):
    if UserProfile.objects.filter(user=request.user).exists():
        messages.error(request, "You can only have one profile. You cannot create another.")
        return redirect('home')

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Associate profile with the current logged-in user
            profile.save()
            messages.success(request, "Your profile has been created successfully.")
            return redirect('home')
    else:
        form = UserProfileForm()

    return render(request, 'create_profile.html', {'form': form})


# Update Profile View
@login_required
def update_profile(request):
    # Fetch the current user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Initialize the form with POST data and the existing instance
        form = UserProfileForm(request.POST, instance=user_profile)
        
        if form.is_valid():
            # Save the updated profile
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('home')
    else:
        # Initialize the form with the existing user profile instance
        form = UserProfileForm(instance=user_profile)

    return render(request, 'update_profile.html', {'form': form})



# Delete Profile View
@login_required
def delete_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_profile.delete()
        messages.success(request, "Your profile has been deleted successfully.")
        return redirect('home')

    return render(request, 'delete_profile.html', {'user_profile': user_profile})


# Browse Profiles View
from django.db.models import Q
@login_required
def browse_profile(request):
    # Get the filter values from the GET request
    role_filter = request.GET.get('role', '').strip()
    skills_filter = request.GET.get('skills', '').split(',') if request.GET.get('skills') else []
    interests_filter = request.GET.get('interests', '').split(',') if request.GET.get('interests') else []

    # Start with all profiles
    profiles = UserProfile.objects.all()
    filter_query = Q()


    if role_filter:
        filter_query &= Q(role=role_filter)  

    if skills_filter:
        for skill in skills_filter:
            filter_query &= Q(skills__icontains=skill.strip())  


    if interests_filter:
        for interest in interests_filter:
            filter_query &= Q(interests__icontains=interest.strip())  


    profiles = profiles.filter(filter_query).distinct()


    roles = UserProfile.objects.values_list('role', flat=True).distinct()
    skills = [choice[0] for choice in SKILL_CHOICES]
    interests = [choice[0] for choice in INTEREST_CHOICES]

    # Render the response
    return render(request, 'browse_profile.html', {
        'profiles': profiles,
        'roles': roles,
        'skills': skills,
        'interests': interests,
        'selected_role': role_filter,
        'selected_skills': skills_filter,
        'selected_interests': interests_filter,
    })




# Profile Detail View
@login_required
def profile_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    skills_list = user_profile.skills.split(', ') if user_profile.skills else []
    interests_list = user_profile.interests.split(', ') if user_profile.interests else []

    # Check connection status
    connection_status = None
    if ConnectionRequest.objects.filter(sender=request.user, receiver=user_profile.user, status='accepted').exists():
        connection_status = 'connected'
    elif ConnectionRequest.objects.filter(sender=request.user, receiver=user_profile.user, status='pending').exists():
        connection_status = 'sent'
    elif ConnectionRequest.objects.filter(sender=user_profile.user, receiver=request.user, status='pending').exists():
        connection_status = 'received'

    return render(request, 'user_profile.html', {
        'user_profile': user_profile,
        'skills_list': skills_list,
        'interests_list': interests_list,
        'connection_status': connection_status,
    })



# Send Connection Request View
@login_required
def send_connection_request(request, user_id):
    receiver = get_object_or_404(UserProfile, user_id=user_id)
    if receiver != request.user:
        # Check if there is no pending connection request between them
        if not ConnectionRequest.objects.filter(sender=request.user, receiver=receiver.user, status='pending').exists() and \
           not ConnectionRequest.objects.filter(sender=receiver.user, receiver=request.user, status='pending').exists():
            ConnectionRequest.objects.create(sender=request.user, receiver=receiver.user, status='pending')

    return redirect('profile_detail', user_id=user_id)

# Manage Connection Requests View

@login_required
def manage_requests(request):
    # Sent and received connection requests (both pending)
    sent_requests = ConnectionRequest.objects.filter(sender=request.user, status='pending')
    received_requests = ConnectionRequest.objects.filter(receiver=request.user, status='pending')

    # Handle the action of accepting or declining a request
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')
        connection_request = get_object_or_404(ConnectionRequest, id=request_id)

        if connection_request.receiver == request.user:
            if action == 'accept':
                connection_request.status = 'accepted'
                # Also create the reverse request (sender accepts the connection)
                ConnectionRequest.objects.create(sender=request.user, receiver=connection_request.sender, status='accepted')
                messages.success(request, "Connection request accepted.")
            elif action == 'decline':
                connection_request.status = 'declined'
                messages.info(request, "Connection request declined.")
            connection_request.save()

    # Display the requests (sent, received, accepted)
    accepted_requests = ConnectionRequest.objects.filter(status='accepted').filter(
        sender=request.user
    ) | ConnectionRequest.objects.filter(status='accepted').filter(receiver=request.user)

    return render(request, 'manage_requests.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'accepted_requests': accepted_requests,
    })