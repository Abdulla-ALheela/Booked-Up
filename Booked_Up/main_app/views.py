from django.shortcuts import render,redirect
from .models import Book,BorrowCart,BorrowList
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def book_index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})

@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'books/detail.html', {'book': book})

@login_required
def cart_index(request):
    books = BorrowCart.objects.filter(user=request.user, is_active=True)
    print(books)
    return render(request, 'cart/index.html', {'books': books})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    BorrowCart.objects.get_or_create(book=book, user=request.user, is_active=True)

    return redirect('book-index')

@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    BorrowCart.objects.filter(book=book, user=request.user, is_active=True).delete()

    return redirect('cart-index')

@login_required
def checkout(request):

    cart = request.session.get('cart', [])

    
    return redirect('book-index')

class BookCreate(LoginRequiredMixin,CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(LoginRequiredMixin,UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(LoginRequiredMixin,DeleteView):
    model = Book
    success_url = '/Books/'

class Home(LoginView):
    template_name = 'home.html'


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
    
   