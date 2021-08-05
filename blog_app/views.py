from django.shortcuts import render
import requests

def homepage(request):
    context = {}
    return render(request, 'homepage.html', context)