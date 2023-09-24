from django.shortcuts import render
from django.http import Http404
from django.db.models import Q

from ..models import Species, Detection


def entire( request ):

	# Todo: Make this more efficient
	species_list = Species.objects.all().order_by("common_name")
	detection_list = Detection.objects.all()

	detections_by_species_id = count_detections_by_species_id(detection_list)

	for s in species_list:
		s.detection_count = detections_by_species_id[s.id]

	context = {
		"species_list": species_list,
	}
	return render(request, "species/list.html", context)


def single(request, item_id):
	try:
		species = Species.objects.get(pk=item_id)
	except Species.DoesNotExist:
		raise Http404("Species does not exist")

	detections = Detection.objects.filter(species=species)

	context = {
		"species": species,
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
		
		detections_by_species_id = count_detections_by_species_id(detections)
		for s in species_found:
			s.detection_count = detections_by_species_id[s.id]

		context = {
			'query': search_query,
			'species_found': species_found
		}

	return render(request, 'species/search.html', context)



def count_detections_by_species_id( detection_list ) :

	species_ids = {}

	for d in detection_list :
		try:
			species_ids[d.species.id] += 1
		except KeyError:
			species_ids[d.species.id] = 1

	return species_ids
