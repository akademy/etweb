from django.shortcuts import render
from django.http import Http404
from django.db.models import Q

from ..models import Species, Detection


def entire(request):
	species_list = Species.objects.all()
	context = {
		"species_list": species_list,
	}
	return render(request, "species/list.html", context)


def single(request, species_id):
	try:
		species = Species.objects.get(pk=species_id)
	except Species.DoesNotExist:
		raise Http404("Species does not exist")

	detections = Detection.objects.filter(species=species)

	context = {
		"species": species,
		"detections": detections
	}
	return render(request, "species/single.html", context)


def search(request):

	# Check if the request is a post request.
	if request.method == 'POST':
		# Retrieve the search query entered by the user
		search_query = request.POST['search_query']
		# Filter your model by the search query
		species = Species.objects.filter(Q(common_name__icontains=search_query) | Q(scientific_name__icontains=search_query))
		return render(request, 'species/search.html', {'query': search_query, 'species': species})
	else:
		return render(request, 'species/search.html', {})
