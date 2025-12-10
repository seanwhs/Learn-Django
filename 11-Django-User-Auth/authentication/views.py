# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import SignupForm, SigninForm
from .tokens import account_activation_token

User = get_user_model()

def home(request):
    return render(request, 'authentication/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = f"{request.scheme}://{request.get_host()}/activate/{uid}/{token}/"

            subject = "Activate Your Account"
            message = f"Hi {user.first_name},\n\nActivate your account:\n{activation_link}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.success(request, "Account created! Check console for activation link.")
            return redirect('signin')
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated! You can now log in.")
        return redirect('signin')
    else:
        messages.error(request, "Activation link is invalid.")
        return redirect('signup')

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "Account not activated! Check console for activation link.")
                return render(request, 'authentication/signin.html', {'form': form})
            login(request, user)
            messages.success(request, f"Logged in as {user.first_name}")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = SigninForm()
    return render(request, 'authentication/signin.html', {'form': form})

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')
