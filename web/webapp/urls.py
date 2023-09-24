from django.urls import path

from .views import detections, detectors, species
from .views import home

urlpatterns = [
	path("", home.index, name="index"),

	# Detections
	path("detections/", detections.entire, name="detections-entire"),
	path("detections/search/", detections.search, name="detections-search"),
	path("detections/<int:item_id>/", detections.single, name="detections-single"),

	# Detectors
	path("detectors/", detectors.entire, name="detectors-entire"),
	path("detectors/search/", detectors.search, name="detectors-search"),
	path("detectors/<int:item_id>/", detectors.single, name="detectors-single"),

	# Species
	path("species/", species.entire, name="species-entire"),
	path("species/search/", species.search, name="species-search"),
	path("species/<int:item_id>/", species.single, name="species-single"),

]
