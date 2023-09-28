from django.urls import path

from .views import analyses, detections, detectors, positions, species
from .views import home, about

urlpatterns = [
	path("", home.index, name="index"),
	path("explore/", home.explore, name="explore"),
	path("about/", about.about, name="about"),

	# Analyses
	path("analyses/", analyses.entire, name="analyses-entire"),
	path("analyses/search/", analyses.search, name="analyses-search"),
	path("analyses/<int:item_id>/", analyses.single, name="analyses-single"),
	
	# Detections
	path("detections/", detections.entire, name="detections-entire"),
	path("detections/search/", detections.search, name="detections-search"),
	path("detections/<int:item_id>/", detections.single, name="detections-single"),

	# Detectors
	path("detectors/", detectors.entire, name="detectors-entire"),
	path("detectors/search/", detectors.search, name="detectors-search"),
	path("detectors/<int:item_id>/", detectors.single, name="detectors-single"),

	# Positions
	path("positions/", positions.entire, name="positions-entire"),
	path("positions/search/", positions.search, name="positions-search"),
	path("positions/<int:item_id>/", positions.single, name="positions-single"),
	
	# Species
	path("species/", species.entire, name="species-entire"),
	path("species/search/", species.search, name="species-search"),
	path("species/<int:item_id>/", species.single, name="species-single"),

]
