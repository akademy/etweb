from django.urls import path

from .views import species
from .views import home

urlpatterns = [
	path("", home.index, name="index"),
	path("species/", species.entire, name="species-entire"),
	path("species/search/", species.search, name="species-search"),
	path("species/<int:species_id>/", species.single, name="species-single"),
]
