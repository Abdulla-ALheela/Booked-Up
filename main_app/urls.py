from django.urls import path, include
from . import views 


urlpatterns = [
   path('', views.home, name='home'),
   path('about/', views.about, name='about'),
   path('books/', views.book_index, name='book-index'),
   path('cart/', views.cart_index, name='cart-index'),
   path('checkout/', views.checkout, name='checkout'),
   path('return/<int:book_id>/', views.Return, name='return'),
   path('cart/<int:book_id>/add/', views.add_to_cart, name='add-to-cart'),
   path('cart/<int:book_id>/remove/', views.remove_from_cart, name='remove-from-cart'),
   path('books/<int:book_id>/', views.book_detail, name='book-detail'),
   path('accounts/', include('django.contrib.auth.urls')),
   path('accounts/signup/', views.signup, name='signup'),
   path('comments/', views.comment_index, name='comment-index'),
   path('comments/<int:comment_id>/', views.comment_detail, name='comment-detail'),
   path('books/<int:book_id>/comments/create/', views.CommentCreate.as_view(), name='comment-create'),
   path('books/<int:book_id>/comments/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment-update'),
   path('books/<int:book_id>/comments/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment-delete'),
]