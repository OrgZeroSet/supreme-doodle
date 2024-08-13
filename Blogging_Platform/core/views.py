from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Posts


"""
Renders the home page with a list of all articles.

Args:
    request (django.http.HttpRequest): The HTTP request object.

Returns:
    django.http.HttpResponse: The rendered response for the home page.
"""
def home(request):
    context = {
        "articles": Posts.objects.all(),
    }
    return render(request, "home.html", context)


"""
Retrieves and renders an article page based on the provided article slug or ID.

If a valid article slug is provided, the article with the matching slug is retrieved and rendered 
in the "article.html" template. If no article is found with the provided slug, or if an article ID 
is provided instead, the home page is rendered with the list of all articles.

Args:
    request (django.http.HttpRequest): The HTTP request object.
    article_slug (str, optional): The slug of the article to retrieve.
    article_id (int, optional): The ID of the article to retrieve.

Returns:
    django.http.HttpResponse: The rendered response for the article or home page.
"""
def article(request, article_slug=None, article_id=None):
    try:
        article = Posts.objects.get(id=article_id)

        if article_slug in article.slug:
            context = {
                "article_slug": article_slug,
                "article_id": article,
            }
            return render(request, "article.html", context)                   
    except ObjectDoesNotExist or AttributeError:        
        return render(request, "home.html", {"articles": Posts.objects.all()})
    return render(request, "home.html", {"articles": Posts.objects.all()})

