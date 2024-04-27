from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("monblog:accueil")
            else:
                messages.error(request, "Identifiant ou mot de passe incorrect")
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {'form': form})

def logout_user(request):
    logout(request)
    return redirect("monblog:accueil")

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("account:login")
    else:
        form = UserCreationForm()
    return render(request, "account/register.html", {'form': form})
