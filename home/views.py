from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def receipe(request):
    if request.method== "POST":
       receipe_name = request.POST.get('receipe_name')
       receipe_description = request.POST.get('receipe_description')
       receipe_image = request.FILES.get('receipe_image')
       
       Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
       return redirect('receipe')
    
    queryset = Receipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))

    context ={'receipes': queryset}

    return render(request, 'receipes.html', context)

@login_required(login_url="login")
def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('receipe')

@login_required(login_url="login")
def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)

    if request.method == "POST":
        receipe_name = request.POST.get('receipe_name')
        receipe_description = request.POST.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()
        return redirect('receipe')
    
    context = {'receipe': queryset}
    return render(request, 'update_receipes.html', context)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'invalid Username')
            return redirect('login')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request,'invalid credentials')
            return redirect('login')
        else:
            auth_login(request, user)
            
            return redirect('receipe')

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create(
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'register.html')
def logout(request):
    auth_logout(request)
    return redirect('login')
