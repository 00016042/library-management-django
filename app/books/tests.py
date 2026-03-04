import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Author, Book, Category, Member, BorrowRecord
from datetime import date, timedelta


@pytest.mark.django_db
class TestModels:
    def test_author_str(self, author):
        assert str(author) == 'George Orwell'

    def test_author_full_name(self, author):
        assert author.full_name == 'George Orwell'

    def test_book_str(self, book):
        assert str(book) == '1984'

    def test_book_is_available(self, book):
        assert book.is_available is True

    def test_book_unavailable_when_no_copies(self, book):
        book.available_copies = 0
        book.save()
        assert book.is_available is False

    def test_category_str(self, category):
        assert str(category) == 'Fiction'

    def test_member_str(self, member):
        assert 'testuser' in str(member)

    def test_member_id_generated(self, member):
        assert member.member_id.startswith('LIB')

    def test_book_author_relationship(self, book, author):
        assert book.author == author
        assert book in author.books.all()

    def test_book_category_relationship(self, book, category):
        assert category in book.categories.all()
        assert book in category.books.all()


@pytest.mark.django_db
class TestViews:
    def test_home_page(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_book_list_page(self, client):
        response = client.get(reverse('book-list'))
        assert response.status_code == 200

    def test_author_list_page(self, client):
        response = client.get(reverse('author-list'))
        assert response.status_code == 200

    def test_book_detail_page(self, client, book):
        response = client.get(reverse('book-detail', kwargs={'pk': book.pk}))
        assert response.status_code == 200
        assert b'1984' in response.content

    def test_author_detail_page(self, client, author):
        response = client.get(reverse('author-detail', kwargs={'pk': author.pk}))
        assert response.status_code == 200

    def test_book_create_requires_login(self, client):
        response = client.get(reverse('book-create'))
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_my_borrows_requires_login(self, client):
        response = client.get(reverse('my-borrows'))
        assert response.status_code == 302

    def test_login_page(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_register_page(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200

    def test_profile_requires_login(self, client):
        response = client.get(reverse('profile'))
        assert response.status_code == 302

    def test_book_list_search(self, client, book):
        response = client.get(reverse('book-list') + '?query=1984')
        assert response.status_code == 200
        assert b'1984' in response.content

    def test_login_success(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 302

    def test_register_creates_user(self, client, db):
        response = client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        assert User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
class TestBorrowSystem:
    def test_borrow_record_creation(self, book, member):
        record = BorrowRecord.objects.create(
            book=book,
            member=member,
            due_date=date.today() + timedelta(days=14)
        )
        assert record.status == 'borrowed'
        assert str(record.book.title) == '1984'

    def test_book_availability_decreases_on_borrow(self, client, user, book, member):
        initial = book.available_copies
        client.force_login(user)
        client.post(reverse('borrow-book', kwargs={'pk': book.pk}), {
            'due_date': date.today() + timedelta(days=14),
        })
        book.refresh_from_db()
        assert book.available_copies == initial - 1
