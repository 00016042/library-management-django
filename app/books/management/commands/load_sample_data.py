"""
Management command to load sample data for demonstration.
Run: python manage.py load_sample_data
Student ID: 00016042
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Author, Category, Book, Member
from datetime import date


class Command(BaseCommand):
    help = 'Load sample data: authors, categories, books, and test users'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')

        # Create categories
        categories_data = [
            ('Fiction', 'fiction', 'Fictional literature and novels'),
            ('Science', 'science', 'Scientific books and research'),
            ('History', 'history', 'Historical accounts and biographies'),
            ('Technology', 'technology', 'Technology, computing, and engineering'),
            ('Philosophy', 'philosophy', 'Philosophical works and essays'),
        ]
        categories = {}
        for name, slug, desc in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
            categories[slug] = cat
        self.stdout.write(f'  Created {len(categories)} categories')

        # Create authors
        authors_data = [
            ('George', 'Orwell', 'English novelist and essayist, known for Nineteen Eighty-Four and Animal Farm.', date(1903, 6, 25)),
            ('Aldous', 'Huxley', 'English writer known for Brave New World and Point Counter Point.', date(1894, 7, 26)),
            ('Fyodor', 'Dostoevsky', 'Russian novelist, journalist, and philosopher.', date(1821, 11, 11)),
            ('Isaac', 'Asimov', 'American author and professor of biochemistry at Boston University.', date(1920, 1, 2)),
            ('Yuval Noah', 'Harari', 'Israeli historian, philosopher, and author of Sapiens.', date(1976, 2, 24)),
        ]
        authors = []
        for first, last, bio, birth in authors_data:
            author, _ = Author.objects.get_or_create(
                first_name=first, last_name=last,
                defaults={'bio': bio, 'birth_date': birth}
            )
            authors.append(author)
        self.stdout.write(f'  Created {len(authors)} authors')

        # Create books
        books_data = [
            ('1984', '9780451524935', authors[0], [categories['fiction'], categories['philosophy']],
             date(1949, 6, 8), 'A dystopian novel about totalitarian surveillance.', 5),
            ('Animal Farm', '9780451526342', authors[0], [categories['fiction']],
             date(1945, 8, 17), 'An allegorical novella reflecting events of Soviet history.', 3),
            ('Brave New World', '9780060850524', authors[1], [categories['fiction'], categories['science']],
             date(1932, 1, 1), 'A dystopian novel set in a futuristic World State.', 4),
            ('Crime and Punishment', '9780140449136', authors[2], [categories['fiction'], categories['philosophy']],
             date(1866, 1, 1), 'A novel about the psychological turmoil of a murderer.', 2),
            ('Foundation', '9780553293357', authors[3], [categories['fiction'], categories['science']],
             date(1951, 5, 1), 'A science fiction novel about the fall of a Galactic Empire.', 6),
            ('Sapiens', '9780062316097', authors[4], [categories['history'], categories['science']],
             date(2011, 1, 1), 'A brief history of humankind.', 4),
            ('Homo Deus', '9780062464316', authors[4], [categories['history'], categories['philosophy']],
             date(2015, 1, 1), 'A brief history of tomorrow.', 3),
        ]
        for title, isbn, author, cats, pub_date, desc, copies in books_data:
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title, 'author': author,
                    'published_date': pub_date, 'description': desc,
                    'available_copies': copies, 'total_copies': copies,
                }
            )
            if created:
                book.categories.set(cats)
        self.stdout.write(f'  Created {len(books_data)} books')

        # Create test users
        test_user, created = User.objects.get_or_create(
            username='testmember',
            defaults={
                'email': 'testmember@library.uz',
                'first_name': 'Test',
                'last_name': 'Member',
            }
        )
        if created:
            test_user.set_password('member123')
            test_user.save()
            Member.objects.create(user=test_user, phone='+998901234567', address='Tashkent, Uzbekistan')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@library.uz', 'admin123')
            Member.objects.create(user=admin, phone='+998901234568')
            self.stdout.write('  Created admin user (admin/admin123)')

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write('  Test user: testmember / member123')
        self.stdout.write('  Admin user: admin / admin123')
