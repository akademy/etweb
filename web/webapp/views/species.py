from django.shortcuts import render
from django.http import Http404

from ..models import Species


def species(request):
	species_list = Species.objects.all()
	context = {
		"species_list": species_list,
	}
	return render(request, "species/list.html", context)


def species_single(request, species_id):
	try:
		species = Species.objects.get(pk=species_id)
	except Species.DoesNotExist:
		raise Http404("Species does not exist")

	context = {
		"species": species,
	}
	return render(request, "species/single.html", context)

