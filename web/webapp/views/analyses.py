from django.shortcuts import render
from django.http import Http404
from django.db.models import Q, Count

from ..models import Analysis, Detector


def entire( request ):

	analysis_list = Analysis.objects.all().order_by("name")

	context = {
		"analysis_list": analysis_list,
	}
	
	return render(request, "analyses/list.html", context)


def single(request, item_id):
	try:
		analysis = Analysis.objects.get(pk=item_id)
	except Analysis.DoesNotExist:
		raise Http404("Species does not exist")

	detector = Detector.objects.get(pk=analysis.detector.id)

	context = {
		"analysis": analysis,
		"detector": detector
	}
	return render(request, "analyses/single.html", context)


def search(request):

	if request.method == 'POST':

		search_name = request.POST['search_name'].strip()

		q_filter = Q()
		
		if search_name != "" :
			q_filter = q_filter & Q(name__icontains=search_name)
			
		analyses_found = Analysis.objects\
			.filter( q_filter )\
			.order_by("name")

		return render(request, 'analyses/search.html', {
			'search_name': search_name,
			'analyses_found': analyses_found,
			'posted': True
		})
	
	else:
		
		return render(request, 'analyses/search.html', {
			'posted': False
		})
