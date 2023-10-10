from django.shortcuts import render
from django.http import Http404
from django.db.models import Q, Count, Avg

from ..models import Species, Detection


def entire( request ):

	species_list = Species.objects.all().order_by("common_name")
	add_additional_info(Detection.objects.all(), species_list)

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

	# TODO: figure out why I can't just pass in the ordered list here...
	# add_additional_info(detections, [species])
	add_additional_info(Detection.objects.filter(species=species), [species])
	
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

		add_additional_info(detections, species_found)

		context = {
			'query': search_query,
			'species_found': species_found
		}

	return render(request, 'species/search.html', context)


def add_additional_info(detections, species_list):
	
	detections_count = detections.values("species").annotate(count=Count("species") )
	detections_average_confidence = detections.values("species").annotate(average_confidence=Avg("confidence") )

	print(detections_count)
	print(detections_average_confidence)

	detections_count_by_species = { dps["species"] : dps["count"] for dps in detections_count }
	detections_average_confidence_by_species = { dac["species"] : dac["average_confidence"] for dac in detections_average_confidence }
	
	for s in species_list:
		
		try:
			s.detection_count = detections_count_by_species[s.id]
		except KeyError:
			s.detection_count = 0
			
		try:
			s.average_confidence = detections_average_confidence_by_species[s.id]
		except KeyError:
			s.average_confidence = 0


