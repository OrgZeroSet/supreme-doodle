from django.urls import path
from . import views

urlpatterns = [
    path("", views.sign_in, name="sign_in"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("sign-out/", views.sign_out, name="sign_out"),
    path("success/", views.success, name="success"),
]