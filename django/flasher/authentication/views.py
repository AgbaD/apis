from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/user/page')
        messages.info(request, 'Username or password is incorrect')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email'].lower()

        if password1 != password2:
            messages.info(request, "Passwords must match")
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username has been takeen")
        else:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                            email=email, password=password1)
            user.save()
            return redirect('/user/page')
    return render(request, 'register.html')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != password2:
                messages.info(request, 'Passwords do not match')
                return render(request, 'change_password.html')

            user = request.user
            user.set_password([password2])
            user.save()
            return redirect('/user/page')
        return render(request, 'change_password.html')
    return redirect('/')


def delete_account(request):
    if request.user.is_authenticated:
        user = request.user

        user_id = user.id
        User.objects.filter(id=user_id).delete()
    return redirect('/')
