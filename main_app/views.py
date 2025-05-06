from django.shortcuts import render,redirect
from .models import Book,BorrowCart,BorrowList , Comment
from django.contrib.auth.forms import AuthenticationForm
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
from .forms import CommentForm
from django.contrib import messages


# Home view: displays login form for unauthenticated users; shows borrowed books for logged-in users
def home(request):
    if request.user.is_authenticated:
        borrowed_books = BorrowList.objects.filter(user=request.user)
        return render(request, 'home.html', {'borrowed_books': borrowed_books})
    else:
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect('home')
        return render(request, 'home.html', {'form': form})


# About view: displays information about the application
def about(request):
    return render(request, 'about.html')

# Book index: displays all books, indicating which are available and which are not for borrowing
def book_index(request):
    books = Book.objects.all()
    borrowed_list = BorrowList.objects.all()
    return render(request, 'books/index.html', {'books': books , 'borrowed_list': borrowed_list})

# Book detail view: displays detailed information about a book, along with a comment form and existing comments for the book
@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    comments = Comment.objects.filter(book=book) 
    borrow = BorrowList.objects.filter(book=book).first()
    comment_form = CommentForm()
    return render(request, 'books/detail.html', {'book': book, 'comments': comments, 'borrow': borrow, 'comment_form': comment_form})


# Cart index: displays all books currently in the user's cart
@login_required
def cart_index(request):
    books = BorrowCart.objects.filter(user=request.user, is_active=True)
    return render(request, 'cart/index.html', {'books': books})


# Add to cart view: adds a book to the cart when the "Borrow" button is clicked on the book detail page
@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    BorrowCart.objects.get_or_create(book=book, user=request.user, is_active=True)
    
    return redirect('book-index')

# Remove from cart view: removes a book from the cart when the "Remove" button is clicked on the cart page
@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    BorrowCart.objects.filter(book=book, user=request.user, is_active=True).delete()

    return redirect('cart-index')

# Checkout view: handles the checkout process by verifying all books in the cart are still available. 
# If available, it creates entries in the BorrowList, deletes the books from the cart, and redirects to the home page. 
# Also handles messaging if any books in the cart are no longer available.
@login_required
def checkout(request):
    cart_items = BorrowCart.objects.filter(user=request.user, is_active=True)
    unavailable_books = []

    for item in cart_items:
      
        if item.book.is_available:
    
            BorrowList.objects.create(
                user=request.user,
                book=item.book,
                borrow_at=timezone.now().date(),
                due_date=timezone.now().date() + timedelta(days=14),
                is_borrowed=True
            )

   
            item.book.is_available = False
            item.book.save()

      
            item.delete()
        else:
  
            unavailable_books.append(item.book.title)
            item.delete()

 
    if unavailable_books:
        msg = "The following book(s) were not available and removed from your cart: " + ", ".join(unavailable_books)
        messages.warning(request, msg)

    return redirect('home')


# Return view: handles returning a book when the "Return" button is clicked on the home page
@login_required
def Return(request,book_id):

    book = get_object_or_404(Book, id=book_id)
  
    BorrowList.objects.filter(book=book, user=request.user).delete()

    book.is_available = True
    book.save()

    return redirect('home')


# Route for displaying and handling the sign-up form
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

# Comments index: displays all comments as cards
@login_required
def comment_index(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'comments/index.html', {'comments': comments})

# Comment detail view: displays detailed information about a specific comment
@login_required
def comment_detail(request, comment_id):
    comment = Comment.objects.get(id=comment_id, user=request.user)
    return render(request, 'comments/detail.html', {'comment': comment})


# View that handles the creation of new comments from the comment form
class CommentCreate(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['comment']
    template_name = 'books/detail.html'

    def form_valid(self, form):
        book_id = self.kwargs['book_id']
        form.instance.book = get_object_or_404(Book, id=book_id)
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('book-detail', kwargs={
            'book_id': self.kwargs['book_id'],
         })
    
# View that handles displaying and updating a specific comment
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'books/detail_edit.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['book_id']
        context['book'] = get_object_or_404(Book, id=book_id)
        context['borrow'] = BorrowList.objects.filter(book_id=book_id).first()
        context['comment'] = self.get_object()  
        context['comments'] = Comment.objects.filter(book_id=book_id)
        context['comment_form'] = CommentForm(instance=self.get_object())   
        return context

   
    def form_valid(self, form):
        book_id = self.kwargs['book_id']
        form.instance.book = get_object_or_404(Book, id=book_id)
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('book-detail', kwargs={'book_id': self.kwargs['book_id']})
    
    
# View that handles deleting a specific comment
class CommentDelete(LoginRequiredMixin,DeleteView):
    model = Comment

    def get_success_url(self):
        book_id = self.object.book.id
        return reverse('book-detail', kwargs={'book_id': book_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        context['book'] = comment.book
        context['comment'] = comment
        return context
