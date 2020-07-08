from django.urls import path
from . import views


app_name = 'dashboard'  # here for namespacing of urls.

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
