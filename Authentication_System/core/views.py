from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


"""
Clears any existing messages stored in the Django messages framework for the given request.

This function retrieves the message storage for the current request, and marks all messages as "used", 
effectively clearing them. This is useful when you want to ensure that any previously displayed
 messages are not shown again on the next page load.
"""
def clear_messages(request):
    storage = messages.get_messages(request)
    storage.used = True




"""
Handles the sign-in functionality for the application.
    
This view function is responsible for authenticating a user and logging them in. It first checks if the
user is already authenticated, and if so, redirects them to the 'success' page. If the request method
is POST, it retrieves the username and password from the form data, and attempts to authenticate the
user using the Django authentication system. If the authentication is successful, the user is logged
in and a success message is displayed. If the authentication fails, a warning message is displayed
and the user is redirected back to the sign-in page.
"""
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('success')

    if request.method == "POST":
        
        username = request.POST["username"]
        password = request.POST["password"]
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            clear_messages(request)
            messages.success(request, "Successfully sign in!")
            return redirect("success")
        else:
            messages.warning(request, "Invalid credentials!")
            return redirect("sign_in")
    return render(request, "sign-in.html")





"""
Handles the sign-up functionality for the application.
    
This view function is responsible for creating a new user account. 
It first checks if the user is already authenticated, and if so, redirects 
them to the 'success' page. If the request method is POST, it retrieves the email, 
username, and password from the form data, and performs the following checks:
    
1. Checks if the username already exists in the system, and if so, displays a warning message.
2. Checks if the email already exists in the system, and if so, displays a warning message.
3. Checks if the password is at least 8 characters long, and if not, displays a warning message.
    
If all the checks pass, it creates a new user account using the Django user model, 
saves the user, clears any existing messages, displays a success message, and redirects 
the user to the sign-in page.
"""
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('success')

    if request.method == "POST":

        usermail = request.POST["usermail"]
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            clear_messages(request)
            messages.warning(request, "Choose different user name!")
            return redirect("sign_up")

        if User.objects.filter(email=usermail).exists():
            clear_messages(request)
            messages.warning(request, "Email already exist!")
            return redirect("sign_up")

        if not len(password) > 7:
            clear_messages(request)
            messages.warning(request, "Password is not secure!")
            return redirect("sign_up")

        user = User.objects.create_user(email=usermail, username=username, password=password)
        if user is not None: 
            user.save()
            clear_messages(request)
            messages.success(request, "Successfully sign up!")
            return redirect("sign_in")
        else:
            clear_messages(request)
            messages.warning(request, "Invalid credentials!")
            return redirect("sign_up")
    return render(request, "sign-up.html")




"""
Logs out the current user and redirects them to the sign-in page with a success message.
"""
def sign_out(request):
    clear_messages(request)
    messages.success(request, "Successfully Sign-out!")
    logout(request)
    return redirect("sign_in")




"""
Renders the "success.html" template, which is likely a page that displays 
a success message to the user.
"""
def success(request):
    return render(request, "success.html")
