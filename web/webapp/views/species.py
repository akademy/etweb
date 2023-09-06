from django.shortcuts import render

from ..models import Species


#def index(request):
#	return HttpResponse("Hello, world. You're at the home.")


def species(request):
	species_list = Species.objects.all()
	context = {
		"species_list": species_list,
	}
	return render(request, "species/list.html", context)


def species_single(request, species_id):
	species = Species.objects.get(pk=species_id)
	context = {
		"species": species,
	}
	return render(request, "species/single.html", context)