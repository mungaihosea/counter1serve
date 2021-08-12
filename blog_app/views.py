from django.shortcuts import render
import requests
from django.core.files.storage import FileSystemStorage

def homepage(request):
    context = {}
    if request.GET.get('page'):
        qs = requests.get(f"{request.GET.get('page')}")
    else:
        qs = requests.get("http://localhost:8000/api/list")
    data = qs.json()
    context['data'] = data
    data['range'] = range(1, data['count'] + 1)
    print(data)
    return render(request, 'homepage.html', context)

def detail_view(request, id):
    context = {}
    response = requests.get(f"http://localhost:8000/api/detail/{id}")
    data = response.json()
    print(data)
    context['post'] = data
    return render(request, 'detail_view.html', context)

def login(request):
    context = {}
    if request.method == "POST":
        data = {
            "username" : request.POST.get('username'),
            "password" : request.POST.get("password")    
        }
        response = requests.post(url = "http://localhost:8000/api/login", json=data)
        try:
            token = response.json()['token']
            print("token", token)
            context['success'] = 'you have been logged in successfully.'
            request.session['token'] = token
        except:
            context['error'] = 'invalid login credentials'
    
    return render(request, 'login.html', context)

def register(request):
    context = {}
    if request.method == "POST":
        data = {
            "username" : request.POST.get('username'),
            "password" : request.POST.get("password"),
            "email" : request.POST.get("email"),  
            "password2" : request.POST.get("password2"),
        }
        response = requests.post(url = "http://localhost:8000/api/add_user", json=data)
        try:
            token = response.json()['token']
            print(response.json())
            context['success'] = 'User created and logged in successfully.'
            request.session['token'] = token
        except:
            context['error'] = 'An error occured check your details and try again'
    return render(request, 'register.html', context)

def create_post(request):
    context = {}
    if request.method == "POST":
        data = {}
        data["title"] = request.POST.get("title")
        data["content"] = request.POST.get("content")

        headers = {"Authorization": f"Token {request.session['token']}"}
        response = requests.post("http://localhost:8000/api/create_post", json=data, headers=headers)
        try: 
            success = response.json()['success']
            context['success'] = "The post has been added successfully"
        except:
            context['error'] = "an error occured check your input and try again"
        
    return render(request, 'create_post.html', context)

#testing comment