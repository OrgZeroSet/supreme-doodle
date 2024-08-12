from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Todo



"""
Renders the main index page of the To-Do List application, displaying 
all the todo items.
    
This view function is responsible for fetching all the todo items from 
the database and passing them to the index.html template for rendering.
    
Args:
    request (django.http.HttpRequest): The HTTP request object.
    
Returns:
    django.http.HttpResponse: The rendered HTML response for the index page.
"""
def index(request):
    context = {
        "todo_list": Todo.objects.all()
    }
    return render(request, "index.html", context)



"""
Adds a new todo item to the database.

This view function is responsible for creating a new Todo object in the database 
based on the title provided in the request. If a valid title is provided, 
a new Todo object is created and saved to the database. A success message
is then displayed to the user and they are redirected to the index page. 
If no title is provided, an error message is displayed and the user is 
redirected to the index page.

Args:
    request (django.http.HttpRequest): The HTTP request object containing the 
    title of the new todo item.

Returns:
    django.http.HttpResponse: A redirect response to the index page.
"""
@require_http_methods(["POST"])
def add(request):
    title = request.POST.get("task_id")
    if title:
        todo = Todo(title=title)
        todo.save()
        messages.success(request, "Todo item added successfully!")
        return redirect("index")
    else:
        messages.error(request, "Value is required.")
        return redirect("index")





"""
Updates the completion status of a Todo item.
    
This view function is responsible for toggling the `complete` field of a Todo
object in the database. It retrieves the Todo object with the provided `task_id`,
flips the value of the `complete` field, saves the updated object, and redirects
the user back to the index page.
    
Args:
    request (django.http.HttpRequest): The HTTP request object.
    task_id (int): The ID of the todo item to be updated.
    
Returns:
    django.http.HttpResponse: A redirect response to the index page.
"""
def update(request, task_id):
    todo = Todo.objects.get(id=task_id)
    todo.complete = not todo.complete
    todo.save()
    return redirect("index")





"""
Deletes a Todo item from the database.
    
This view function is responsible for deleting a Todo object from the database. 
It retrieves the Todo object with the provided `task_id`, deletes it, and 
displays a success message to the user. If the `task_id` is invalid, 
an error message is displayed instead.
    
Args:
    request (django.http.HttpRequest): The HTTP request object.
    task_id (int): The ID of the todo item to be deleted.
    
Returns:
    django.http.HttpResponse: A redirect response to the index page.
"""
def delete(request, task_id):
    try:
        task = Todo.objects.get(id=task_id)
        task.delete()
        messages.success(request, "Task deleted!")
    except Todo.DoesNotExist:
        messages.error(request, "Task does not exist.")
    return redirect("index")