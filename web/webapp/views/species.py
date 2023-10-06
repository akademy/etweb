from django.shortcuts import render
from django.http import Http404
from django.db.models import Q, Count

from ..models import Species, Detection


def entire( request ):

	species_list = Species.objects.all().order_by("common_name")
	species_by_detection(Detection.objects.all(), species_list)

	context = {
		"species_list": species_list,
	}
	return render(request, "species/list.html", context)


def single(request, item_id):
	try:
		species = Species.objects.get(pk=item_id)
	except Species.DoesNotExist:
		raise Http404("Species does not exist")

	detections = Detection.objects.filter(species=species).order_by("date")
	
	context = {
		"species": species,
		"photos": species.wikimedia_photo_urls.split("###"),
		"detections": detections
	}
	return render(request, "species/single.html", context)


def search(request):

	context = {}
	if request.method == 'POST':

		search_query = request.POST['query'].strip()
		
		species_found = Species.objects\
			.filter(Q(common_name__icontains=search_query) | Q(scientific_name__icontains=search_query))\
			.order_by("common_name")

		detections = Detection.objects.filter(species__in=[s.id for s in species_found])

		species_by_detection(detections, species_found)

		context = {
			'query': search_query,
			'species_found': species_found
		}

	return render(request, 'species/search.html', context)


def species_by_detection(detections, species_list):
	
	detections_per_species = detections.values("species").annotate(count=Count("species"))
	
	species_by_detections = { dps["species"] : dps["count"] for dps in detections_per_species }
	for s in species_list:
		try:
			s.detection_count = species_by_detections[s.id]
		except KeyError:
			s.detection_count = 0


