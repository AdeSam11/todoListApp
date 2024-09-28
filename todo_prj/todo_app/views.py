from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get("task")
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    return render(request, 'todo_app/todo.html', {'todos':all_todos})

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if len(password) < 5:
            messages.error(request, 'Password must be more than 4 characters')
            return redirect('register')
        
        if password != password2:
            messages.error(request, "The passwords don't match")
            return redirect('register')
        
        get_all_users_by_uname = User.objects.filter(username=username)
        if get_all_users_by_uname:
            messages.error(request, 'Username already exists, try another one')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'Registration succesful, proceed to login')
        return redirect('login-page')
    return render(request, 'todo_app/register.html', {})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get("uname")
        password = request.POST.get("pass")

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login-page')
    return render(request, 'todo_app/login.html', {})

def deleteTask(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.delete()
    return redirect('home-page')

def updateTask(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    if get_todo.status == True:
        get_todo.status = False
    else:
        get_todo.status = True
    get_todo.save()
    return redirect('home-page')

def logoutView(request):
    logout(request)
    return redirect('login-page')