
from django.urls import path
from .views import FilmsList
urlpatterns = [
    path('movies/',FilmsList.as_view()),
]
