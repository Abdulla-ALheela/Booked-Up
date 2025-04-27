from django.shortcuts import render,redirect
from .models import Book
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def book_index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})

@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'books/detail.html', {'book': book})

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = '/Books/'

class Home(LoginRequiredMixin,LoginView):
    template_name = 'home.html'

@login_required
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
  