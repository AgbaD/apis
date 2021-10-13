from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/usr/dash')
        messages.info(request, 'User credentials not correct!')
    return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.info(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email has already been used')
        else:
            User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                     email=email, password=password2)
            return redirect('/usr/dash')

    return render(request, 'register.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.info(request, "Passwords do not match")
        else:
            user = request.user
            user.set_password([password2])
            user.save()
            return redirect('/usr/dash')
    return render(request, "change_password.html")
