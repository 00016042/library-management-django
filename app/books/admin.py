from django.contrib import admin
from .models import Author, Book, Category, Member, BorrowRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date']
    search_fields = ['first_name', 'last_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available_copies', 'published_date']
    list_filter = ['categories', 'author']
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    filter_horizontal = ['categories']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'member_id', 'membership_date', 'phone']
    search_fields = ['user__username', 'member_id']


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrow_date', 'due_date', 'status']
    list_filter = ['status']
    search_fields = ['book__title', 'member__user__username']
