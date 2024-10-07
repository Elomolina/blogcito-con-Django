from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.urls import reverse

from .forms import *
# Create your views here.

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "authentication/login.html", {
            "form":form
        })
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username_email = form.cleaned_data['username_email']
            password = form.cleaned_data['password']
            if '@' in username_email:
                try:
                    #check if user in table
                    user_model = User.objects.get(email = username_email)
                    #authenticate
                    user = authenticate(request, username = user_model.username, password = password)
                    if user is not None:
                        login(request, user)
                        return redirect(reverse("blog_site:index"))
                    else:
                        return render(request, "authentication/login.html", {
                            "form": form,
                            "message": "Los datos no coinciden"
                        })
                except User.DoesNotExist:
                    return render(request, "authentication/login.html", {
                        "form": form,
                        "message": 'El correo ingresado es incorrecto'
                    })
            else:
                #if not email then username
                try:
                    #check if user in table
                    user_model = User.objects.get(username = username_email)
                    #authenticate
                    user = authenticate(request, username = user_model.username, password = password)
                    if user is not None:
                        login(request, user)
                        return redirect(reverse("blog_site:index"))
                    else:
                        return render(request, "authentication/login.html", {
                            "form": form,
                            "message": 'Los datos no coinciden'
                        })
                except User.DoesNotExist:
                    return render(request, "authentication/login.html", {
                        "form": form,
                        "message": 'El usuario ingresado es incorrecto'
                    })
                    
    
class LogOutView(View):
    def post(self, request):
        logout(request)
        return(redirect("blog_site:index"))

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "authentication/register.html", {
            "form": form
        })
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email = form.cleaned_data['email'])
            except User.DoesNotExist:
                if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                    return render(request, "authentication/register.html", {
                        "form": form,
                        "message": 'Las contraseñas no coinciden'
                    })
                try: 
                    user = User.objects.create_user(first_name= form.cleaned_data['name'], last_name = form.cleaned_data['name'], username=form.cleaned_data['username'], email = form.cleaned_data['email'], password= form.cleaned_data['password'])
                    user.save()
                    login(request, user)
                    return redirect(reverse("blog_site:index"))
                except IntegrityError:
                    return render(request, "authentication/register.html", {
                        "form": form,
                        "message": 'Ya existe ese usuario'
                    })
            if user is not None:
                return render(request, "authentication/register.html", {
                    "form": form,
                    "message": 'El correo electronico ya esta vinculado con una cuenta existente'
                })
            
        else: 
            return render(request, "authentication/register.html", {
                "form": form
            })