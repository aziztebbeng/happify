from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserAccount, Preference, AddedActivity
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the username or email already exists
        if UserAccount.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        elif UserAccount.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        # Hash the password and create the user account
        hashed_password = make_password(password)
        user = UserAccount(username=username, password=hashed_password, email=email)
        user.save()

        messages.success(request, 'Account created successfully!')
        return redirect('login')  # Redirect to login after successful sign-up

    return render(request, 'signup.html')

# Login View

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = UserAccount.objects.get(username=username)
            if check_password(password, user.password):
                # Manually set the user ID in session to simulate login
                request.session['user_id'] = user.id

                # Redirect based on user preferences
                if Preference.objects.filter(user=user).exists():
                    return redirect('homepage')
                else:
                    return redirect('preferences')
            else:
                messages.error(request, 'Invalid password.')
        except UserAccount.DoesNotExist:
            messages.error(request, 'Username does not exist.')
    
    return render(request, 'login.html')

def preferences(request):
    # Access the user via session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Ensure the user is logged in

    user = UserAccount.objects.get(id=user_id)

    if request.method == 'POST':
        selected_activities = request.POST.getlist('activities')

        # Clear previous preferences for the user
        Preference.objects.filter(user=user).delete()

        # Save new preferences
        for activity in selected_activities:
            Preference.objects.create(user=user, activity=activity)

        messages.success(request, 'Preferences saved successfully!')
        return redirect('homepage')

    return render(request, 'preference.html')

from datetime import datetime

def homepage(request):
    # Retrieve the user from the session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if no user session is found

    user = UserAccount.objects.get(id=user_id)

    if request.method == "POST":
        # Check if the necessary data is provided in the POST request
        activity = request.POST.get('activity')
        datetime_str = request.POST.get('datetime')
        
        # Check if data exists
        if activity and datetime_str:
            try:
                # Parse the datetime string into a datetime object
                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')  # Adjusted format

                # Create the new activity linked to the logged-in user
                added_activity = AddedActivity.objects.create(
                    user=user,  # Use the custom user instance
                    added_activity=activity,
                    datetime=datetime_obj  # Ensure datetime is in the correct format
                )
                return JsonResponse({'status': 'success', 'message': 'Activity added successfully'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

        return JsonResponse({'status': 'error', 'message': 'Missing data in the request'})

    return render(request, 'homepage.html')
