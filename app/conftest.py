import pytest
from django.contrib.auth.models import User
from books.models import Author, Category, Book, Member
from datetime import date


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username='staffuser',
        password='staffpass123',
        is_staff=True
    )


@pytest.fixture
def member(db, user):
    return Member.objects.create(user=user, phone='1234567890')


@pytest.fixture
def category(db):
    return Category.objects.create(name='Fiction', slug='fiction', description='Fiction books')


@pytest.fixture
def author(db):
    return Author.objects.create(
        first_name='George',
        last_name='Orwell',
        bio='English novelist and essayist.'
    )


@pytest.fixture
def book(db, author, category):
    b = Book.objects.create(
        title='1984',
        isbn='9780451524935',
        description='Dystopian novel',
        published_date=date(1949, 6, 8),
        author=author,
        available_copies=3,
        total_copies=3
    )
    b.categories.add(category)
    return b
