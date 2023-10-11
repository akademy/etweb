from django.shortcuts import render
from django.http import Http404
from django.db.models import Q

from ..models import Detection

MAX_RETURN = 500


def entire( request ):

	detection_list = Detection.objects.all().order_by("date")[:MAX_RETURN]
	count = Detection.objects.count()

	context = {
		"detection_list": detection_list,
		"count": count
	}
	return render(request, "detections/list.html", context)


def single(request, item_id):
	try:
		detection = Detection.objects.get(pk=item_id)
	except Detection.DoesNotExist:
		raise Http404("Species does not exist")

	context = {
		"detection": detection
	}
	return render(request, "detections/single.html", context)


def search(request):

	if request.method == 'POST':

		search_name = request.POST['search_name'].strip()
		search_start = request.POST['search_start']
		search_end = request.POST['search_end']
		
		q_filter = Q(date__gte=search_start + " 00:00:00") & Q(date__lte=search_end + " 23:59:59")
		if search_name != "" :
			q_filter = q_filter & (
					Q(species__common_name__icontains=search_name) | Q(species__scientific_name__icontains=search_name))
			
		detections_found = Detection.objects\
			.filter( q_filter )\
			.order_by("date")
		
		count = detections_found.count()
		detections_found = detections_found[:MAX_RETURN]

		return render(request, 'detections/search.html', {
			'search_name': search_name,
			'search_start': search_start,
			'search_end': search_end,
			'detections_found': detections_found,
			'count': count,
			'posted': True
		})
	
	else:
		
		return render(request, 'detections/search.html', {
			'search_start': "2022-01-01",
			'search_end': "2024-01-01",
			'posted': False
		})
		
		



def count_detections_by_species_id( detection_list ) :

	species_ids = {}

	for d in detection_list :
		try:
			species_ids[d.species.id] += 1
		except KeyError:
			species_ids[d.species.id] = 1

	return species_ids
