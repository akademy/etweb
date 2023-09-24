from django.shortcuts import render
from django.http import Http404
from django.db.models import Q

from ..models import Detector


def entire( request ):

	detector_list = Detector.objects.all().order_by("name")

	context = {
		"detector_list": detector_list,
	}
	return render(request, "detectors/list.html", context)


def single(request, item_id):
	try:
		detector = Detector.objects.get(pk=item_id)
	except Detector.DoesNotExist:
		raise Http404("Species does not exist")

	context = {
		"detector": detector
	}
	return render(request, "detectors/single.html", context)


def search(request):

	if request.method == 'POST':

		search_name = request.POST['search_name'].strip()
		search_position = request.POST['search_position'].strip()

		q_filter = Q()
		
		if search_name != "" :
			q_filter = q_filter & Q(name__icontains=search_name)
			
		if search_position != "" :
			q_filter = q_filter & Q(position__name__icontains=search_position)
			
		detectors_found = Detector.objects\
			.filter( q_filter )\
			.order_by("position", "name")

		return render(request, 'detectors/search.html', {
			'search_name': search_name,
			'search_position': search_position,
			'detectors_found': detectors_found,
			'posted': True
		})
	
	else:
		
		return render(request, 'detectors/search.html', {
			'posted': False
		})
