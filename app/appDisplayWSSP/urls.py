from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_page_es, name="get_page_es"),
    path("<str:pagename>", views.get_page_es, name="get_page_es"),
    path("en/<str:pagename>", views.get_page_en, name="get_page_en"),
    
    # API Routes
    path("retrieve/countries", views.retrieve_countries, name="retrieve_countries"),
]