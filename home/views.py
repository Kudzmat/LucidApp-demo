from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.
def sign_in(request):
    """
    Handle user sign-in and provide an option to create an account.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home:home')  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'home/sign_in.html', {'form': form})


def sign_up(request):
    """
    Handle user sign-up to create a new account.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful sign-up
            return redirect('home:home')  # Redirect to the home page
        else:
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, 'home/sign_up.html', {'form': form})

@login_required
def home(request):
    """
    Render the home page of the LucidDemo application.
    """
    user_name = request.user.username  # get username
    context = {
        'user_name': user_name,
    }
    return render(request, 'home/index.html', context=context)