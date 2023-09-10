from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, SignUpForm
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from webapp.custom_auth_backends import CustomAuthBackend 
from .models import CustomUser 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')  # Redirect to the user's profile page after registration
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm  # Import your custom authentication form
from .custom_auth_backends import CustomAuthBackend  # Import your custom authentication backend

def custom_login(request):
    error_message = ""  # Initialize error message

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Initialize the custom authentication backend
            auth_backend = CustomAuthBackend()

            # Attempt authentication
            authenticated_user = auth_backend.authenticate(request, username=email, password=password)

            if authenticated_user:
                # Use the default ModelBackend for login
                login(request, authenticated_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('profile')  # Replace 'profile' with your profile view name
            else:
                # Handle authentication failure (e.g., display an error message)
                error_message = "Invalid email or password. Please try again."
        else:
            # Handle form validation errors
            error_message = "Form validation failed. Please check your inputs."
    else:
        form = CustomAuthenticationForm()

    context = {'form': form, 'error_message': error_message}
    return render(request, 'login.html', context)



def profile(request):
    user = request.user
    print("welcome to tiger",user)
    return render(request, 'profile.html', {'user': user})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('custom_login')