# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .gemini_service import extract_recipe_from_video
from .models import RecipeHistory

def index(request):
    recipe = None
    error = None
    
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        try:
            recipe = extract_recipe_from_video(video_url)
            
            # Save to Database if Logged In
            if request.user.is_authenticated:
                RecipeHistory.objects.create(
                    user=request.user,
                    video_url=video_url,
                    recipe_name=recipe.get('recipe_name', 'Unknown Recipe'),
                    recipe_data=recipe
                )
            # Save to Session if Guest
            else:
                guest_history = request.session.get('guest_history', [])
                guest_history.insert(0, {'url': video_url, 'recipe': recipe})
                request.session['guest_history'] = guest_history[:5] # Keep last 5
                
        except Exception as e:
            error = "Could not process the video. Please ensure the link is valid."

    return render(request, 'core/index.html', {'recipe': recipe, 'error': error})

@login_required
def dashboard(request):
    history = RecipeHistory.objects.filter(user=request.user).order_by('-searched_at')
    return render(request, 'core/dashboard.html', {'history': history})

def custom_login(request):
    error = None
    if request.method == 'POST':
        # Extract data from standard HTML input fields
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # Verify the credentials
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password. Please try again."
            
    return render(request, 'registration/login.html', {'error': error})

def custom_signup(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p1 = request.POST.get('password')
        p2 = request.POST.get('confirm_password')

        # Validation checks
        if p1 != p2:
            error = "Passwords do not match."
        elif User.objects.filter(username=u).exists():
            error = "That username is already taken. Please choose another."
        else:
            # Create the user and log them in
            user = User.objects.create_user(username=u, password=p1)
            login(request, user)
            return redirect('dashboard')
            
    return render(request, 'registration/signup.html', {'error': error})