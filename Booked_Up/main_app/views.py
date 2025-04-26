from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cat_index(request):
    return render(request, 'books/index.html', {'books': books})