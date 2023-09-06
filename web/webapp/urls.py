from django.urls import path

from .views import species
from .views import home

urlpatterns = [
	path("", home.index, name="index"),
	path("species/", species.species, name="species"),
	path("species/<int:species_id>/", species.species_single, name="species"),
]
