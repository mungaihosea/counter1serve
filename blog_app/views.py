from django.shortcuts import render
import requests
from django.core.files.storage import FileSystemStorage

def homepage(request):
    context = {}
    qs = requests.get("http://localhost:8000/api/list")
    data = qs.json()
    context['data'] = data
    for x in data['results']:
        print(x)
        print ("************")
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
# head = {
#             "Authorization": f"Token {}"
#      }

def create_post(request):
    context = {}
    if request.method == "POST":
        data = {}
        data["title"] = request.POST.get("title")
        data["content"] = request.POST.get("content")

        myfile = request.FILES['image']
        
        fs = FileSystemStorage()
        print(dir(myfile))
        # files = {myfile.read()}
        files = {}
        files['img'] = myfile.read()
        
        # if request.FILES:
        #     files = {"img": open(request.FILES.get("image"), 'rb')}
        headers = {"Authorization": f"Token {request.session['token']}"}
        response = requests.post("http://localhost:8000/api/create_post", json=data, headers=headers, files = files)
        try: 
            success = response.json()['success']
            context['success'] = "The post has been added successfully"
        except:
            context['error'] = "an error occured check your input and try again"
        
    return render(request, 'create_post.html', context)