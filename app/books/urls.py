from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book-list'),
    path('books/add/', views.book_create, name='book-create'),
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
    path('books/<int:pk>/edit/', views.book_update, name='book-update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book-delete'),
    path('books/<int:pk>/borrow/', views.borrow_book, name='borrow-book'),
    path('borrow/<int:pk>/return/', views.return_book, name='return-book'),
    path('my-borrows/', views.my_borrows, name='my-borrows'),
    path('authors/', views.author_list, name='author-list'),
    path('authors/add/', views.author_create, name='author-create'),
    path('authors/<int:pk>/', views.author_detail, name='author-detail'),
]
