from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Book, Author, Category, BorrowRecord, Member
from .forms import BookForm, AuthorForm, BorrowForm, BookSearchForm


def home(request):
    recent_books = Book.objects.select_related('author').prefetch_related('categories')[:6]
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_members = Member.objects.count()
    available_books = Book.objects.filter(available_copies__gt=0).count()
    context = {
        'recent_books': recent_books,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_members': total_members,
        'available_books': available_books,
    }
    return render(request, 'home.html', context)


def book_list(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.select_related('author').prefetch_related('categories')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(isbn__icontains=query)
            )
        if category:
            books = books.filter(categories=category)

    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'form': form,
        'categories': Category.objects.all(),
    })


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related('author').prefetch_related('categories'), pk=pk)
    borrow_records = book.borrow_records.select_related('member__user').filter(status='borrowed')
    return render(request, 'books/book_detail.html', {
        'book': book,
        'borrow_records': borrow_records,
    })


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book-detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Add'})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book-detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Edit', 'book': book})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book-list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


def author_list(request):
    authors = Author.objects.prefetch_related('books')
    return render(request, 'books/author_list.html', {'authors': authors})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.prefetch_related('categories')
    return render(request, 'books/author_detail.html', {'author': author, 'books': books})


@login_required
def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Author "{author.full_name}" added successfully!')
            return redirect('author-detail', pk=author.pk)
    else:
        form = AuthorForm()
    return render(request, 'books/author_form.html', {'form': form, 'action': 'Add'})


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        messages.error(request, 'You need a member profile to borrow books.')
        return redirect('book-detail', pk=pk)

    if not book.is_available:
        messages.error(request, 'This book is not available for borrowing.')
        return redirect('book-detail', pk=pk)

    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.book = book
            record.member = member
            record.save()
            book.available_copies -= 1
            book.save()
            messages.success(request, f'You successfully borrowed "{book.title}"!')
            return redirect('my-borrows')
    else:
        form = BorrowForm()
    return render(request, 'books/borrow_form.html', {'form': form, 'book': book})


@login_required
def return_book(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk, member__user=request.user)
    if request.method == 'POST':
        from datetime import date
        record.status = 'returned'
        record.return_date = date.today()
        record.save()
        record.book.available_copies += 1
        record.book.save()
        messages.success(request, f'You returned "{record.book.title}" successfully!')
        return redirect('my-borrows')
    return render(request, 'books/return_confirm.html', {'record': record})


@login_required
def my_borrows(request):
    try:
        member = request.user.member_profile
        records = member.borrow_records.select_related('book__author').order_by('-borrow_date')
    except Member.DoesNotExist:
        records = []
        member = None
    return render(request, 'books/my_borrows.html', {'records': records, 'member': member})
