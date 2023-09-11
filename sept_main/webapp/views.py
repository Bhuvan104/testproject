from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, SignUpForm
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from webapp.custom_auth_backends import CustomAuthBackend 
from .models import Categories, CustomUser ,Books
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Books
from .serializers import BookSerializer
from django.http import JsonResponse

from .models import Books


def returnbook(request):
    if request.method == 'POST':
        return_book_id = request.POST.get('return_book_id')
        print("need to find tiger",return_book_id)
        if return_book_id:
            # Get the book to be returned
            book = Books.objects.filter(bookid=return_book_id).first()
            if book:
                # Clear the association with the user by setting customuser to None
                book.customuser = None
                book.save()
    return redirect('profile')


def take_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('books-dropdown')  # Assuming 'books-dropdown' is the name of your select field]
        if book_id:
            book = Books.objects.filter(bookid=book_id, customuser__isnull=True).first()
            if book:
                # Assign the book to the currently logged-in user
                book.customuser = request.user
                book.save()
    return redirect('profile') 



def get_books_by_category(request):
    category_id = request.GET.get('category_id')
    
    books = Books.objects.filter(category_id=category_id ,customuser=None).values('bookid', 'book_name')
    return JsonResponse({'books': list(books)})



class BookListAPIView(APIView):
    def get(self, request):
        category_id = request.GET.get("category")
        if category_id is not None:
            books = Books.objects.filter(category_id=category_id)
            serializer = BookSerializer(books, many=True)
            return Response({"books": serializer.data})
        return Response({"books": []})
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')  # Redirect to the user's profile page after registration
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm  # Import your custom authentication form
from .custom_auth_backends import CustomAuthBackend  # Import your custom authentication backend

def custom_login(request):
    error_message = ""  # Initialize error message

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Initialize the custom authentication backend
            auth_backend = CustomAuthBackend()

            # Attempt authentication
            authenticated_user = auth_backend.authenticate(request, username=email, password=password)

            if authenticated_user:
                # Use the default ModelBackend for login
                login(request, authenticated_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('profile')  # Replace 'profile' with your profile view name
            else:
                # Handle authentication failure (e.g., display an error message)
                error_message = "Invalid email or password. Please try again."
        else:
            # Handle form validation errors
            error_message = "Form validation failed. Please check your inputs."
    else:
        form = CustomAuthenticationForm()

    context = {'form': form, 'error_message': error_message}
    return render(request, 'login.html', context)


def profile(request):
    all_categories = Categories.objects.all()
    user_taken_books=Books.objects.filter(customuser=request.user)
    return render(request, 'profile.html', {'all_categories': all_categories,"user_taken_books":user_taken_books})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('custom_login')