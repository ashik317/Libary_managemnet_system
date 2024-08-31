from datetime import date

from django.http import HttpResponse
from .models import Book, Item
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm, RegisterForm
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    return render(request, "User/home.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, "User/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken.")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                auth_login(request, user)
                return redirect('home')  # Redirect to home after successful registration
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
    else:
        return render(request, "User/register.html")

def user_logout(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def issue(request):
    if request.method == "POST":
        book_id = request.POST['book_id']
        book = Book.objects.get(pk=book_id)
        issue_item = Item.objects.create(user_id=request.user, book_id=book)
        book.quantity -= 1
        book.save()
        messages.success(request, "Book Issued Successfully")
        return redirect('home')
    my_item = Item.objects.filter(user_id=request.user, returned_date__isnull=True).values_list("book_id", flat=True)
    books = Book.objects.exclude(id__in=my_item).filter(quantity__gt=0)
    return render(request, 'User/issue_item.html', {"books": books})

@login_required(login_url='login')
def history(request):
    my_item = Item.objects.filter(user_id=request.user).order_by('-issued_date')
    paginator = Paginator(my_item, 10)
    page_number = request.GET.get('page', 1)
    show_date_final = paginator.get_page(page_number)
    return render(request, "User/history.html", {'books': show_date_final})

@login_required(login_url='login')
def return_item(request):
    if request.method == "POST":
        book_id = request.POST["book_id"]
        current_book = Book.objects.get(pk=book_id)
        book = Book.objects.get(id=book_id)
        book.update(quantity=book[0].quantity + 1)
        issue_item = Item.objects.filter(user_id=request.user, returned_date__isnull=True, book_id=current_book)
        issue_item.update(return_date=date.today())
        messages.success(request, "Book returned Successfully")

    my_items = Item.objects.filter(user_id=request.user, returned_date__isnull=True).values_list("book_id")
    books = Book.objects.exclude(~Q(id__in=my_items))
    params = {'books':books}
    return render(request, 'User/return_item.html', params)




