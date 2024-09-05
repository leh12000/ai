from django.shortcuts import render

from biblio.models import Book
from category.models import Category


def home(request):

    return render(request,"sewa/home.html",)


def mylearning(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    print(categories)
    print("ok")
    return render(request, "sewa/mylearning.html", {"books": books, "categories": categories})