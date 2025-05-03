from django.shortcuts import render,redirect
from .models import Book,BorrowCart,BorrowList , Comments
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse


def home(request):
    books = BorrowList.objects.all()
    return render(request, 'home.html',{'books': books})

def about(request):
    return render(request, 'about.html')


def book_index(request):
    books = Book.objects.all()
    borrowed_list = BorrowList.objects.all()
    return render(request, 'books/index.html', {'books': books , 'borrowed_list': borrowed_list})

@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'books/detail.html', {'book': book})

@login_required
def cart_index(request):
    books = BorrowCart.objects.filter(user=request.user, is_active=True)
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
    cart_items = BorrowCart.objects.filter(user=request.user, is_active=True)

    for item in cart_items:
        if not BorrowList.objects.filter(user=request.user, book=item.book).exists():
            BorrowList.objects.get_or_create(
                user=request.user,
                book=item.book,
                borrow_at=timezone.now().date(),
                due_date=timezone.now().date() + timedelta(days=14),
                is_borrowed=True
            )

            
            item.book.is_available = False
            item.book.save()

    
    cart_items.delete()

    return redirect('book-index')


@login_required
def Return(request,book_id):

    book = get_object_or_404(Book, id=book_id)
  
    BorrowList.objects.filter(book=book, user=request.user).delete()

    book.is_available = True
    book.save()

    return redirect('home')


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

@login_required
def comments_index(request):
    comments = Comments.objects.filter(user=request.user)
    return render(request, 'comments/index.html', {'comments': comments})

@login_required
def comment_detail(request, comment_id):
    comment = Comments.objects.get(id=comment_id, user=request.user)
    return render(request, 'comments/detail.html', {'comment': comment})


class CommentsCreate(LoginRequiredMixin,CreateView):
    model = Comments
    fields = '__all__'

    def form_valid(self, form):
        book_id = self.kwargs['book_id']
        form.instance.Book = get_object_or_404(Book, id=book_id)
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('book-detail', kwargs={
            'book_id': self.kwargs['book_id'],
            'comment_id': self.object.id
         })

class CommentsUpdate(LoginRequiredMixin,UpdateView):
    model = Comments
    fields = '__all__'

    def form_valid(self, form):
        book_id = self.kwargs['book_id']
        form.instance.Book = get_object_or_404(Book, id=book_id)
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('book-detail', kwargs={
            'book_id': self.kwargs['book_id'],
            'comment_id': self.object.id
         })
    

class CommentsDelete(LoginRequiredMixin,DeleteView):
    model = Comments

    def get_success_url(self):
        book_id = self.object.book.id
        return reverse('book-detail', kwargs={'book_id': book_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        context['book'] = comment.book
        context['comment'] = comment
        return context