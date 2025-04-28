from django.urls import path, include
from . import views 


urlpatterns = [
   path('', views.Home.as_view(), name='home'),
   path('about/', views.about, name='about'),
   path('books/', views.book_index, name='book-index'),
   path('cart/', views.cart_index, name='cart-index'),
   path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
   path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
   path('books/<int:book_id>/', views.book_detail, name='book-detail'),
   path('accounts/', include('django.contrib.auth.urls')),
   path('accounts/signup/', views.signup, name='signup'),
   path('books/create/', views.BookCreate.as_view(), name='book-create'),
   path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
   path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
   path('accounts/signup/', views.signup, name='signup'),
]