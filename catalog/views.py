from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre


# Create your views here.
def index(request: HttpRequest):
  num_books = Book.objects.all().count()
  num_books_contain_aku = Book.objects.filter(title__icontains='悪').count()
  num_genres_contain_1 = Genre.objects.filter(name__icontains='1').count()
  num_instances = BookInstance.objects.all().count()
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()
  num_authors = Author.objects.count()
  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits + 1

  context = {
    'num_books': num_books,
    'num_books_contain_aku': num_books_contain_aku,
    'num_genres_contain_1': num_genres_contain_1,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_visits': num_visits
  }

  return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
  model = Book
  paginate_by: int = 1

class BookDetailView(generic.DetailView):
  model = Book

class AuthorListView(generic.ListView):
  model = Author

class AuthorDetailView(generic.DetailView):
  model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 10

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
class AllBorrowedListView(PermissionRequiredMixin, generic.ListView):
  permission_required = ('catalog.can_mark_returned')
  model = BookInstance
  template_name = 'catalog/all_borrowed.html'