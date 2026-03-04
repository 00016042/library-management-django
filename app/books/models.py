from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    published_date = models.DateField()
    cover_image = models.ImageField(upload_to='books/', blank=True, null=True)
    available_copies = models.PositiveIntegerField(default=1)
    total_copies = models.PositiveIntegerField(default=1)
    # Many-to-one: many books have one author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    # Many-to-many: books can belong to many categories
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

    @property
    def is_available(self):
        return self.available_copies > 0


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    membership_date = models.DateField(auto_now_add=True)
    member_id = models.CharField(max_length=20, unique=True, blank=True)

    def __str__(self):
        return f'Member: {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.member_id:
            self.member_id = f'LIB{self.user.id:05d}'
        super().save(*args, **kwargs)


class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    # Many-to-one: many borrow records for one book
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    # Many-to-one: many borrow records for one member
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrow_records')
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-borrow_date']

    def __str__(self):
        return f'{self.member} borrowed {self.book.title}'
