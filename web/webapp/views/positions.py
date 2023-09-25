from django.shortcuts import render
from django.http import Http404
from django.db.models import Q

from ..models import Position


def entire( request ):

	position_list = Position.objects.all().order_by("name")

	for p in position_list :
		add_latitude_and_longitude_to_position( p )

	context = {
		"position_list": position_list,
	}
	return render(request, "positions/list.html", context)


def single(request, item_id):
	try:
		position = Position.objects.get(pk=item_id)
	except Position.DoesNotExist:
		raise Http404("Species does not exist")

	add_latitude_and_longitude_to_position( position )
	
	context = {
		"position": position,
	}
	
	return render(request, "positions/single.html", context)


def search(request):

	if request.method == 'POST':

		search_name = request.POST['search_name'].strip()

		q_filter = Q()
		
		if search_name != "" :
			q_filter = q_filter & Q(name__icontains=search_name)
			
		positions_found = Position.objects\
			.filter( q_filter )\
			.order_by("name")

		for p in positions_found :
			add_latitude_and_longitude_to_position( p )

		return render(request, 'positions/search.html', {
			'search_name': search_name,
			'positions_found': positions_found,
			'posted': True
		})
	
	else:
		
		return render(request, 'positions/search.html', {
			'posted': False
		})


def add_latitude_and_longitude_to_position( position: Position ) :
	lat, long = get_latitude_and_longitude( position.lat_long )
	position.latitude = lat
	position.longitude = long
	
def get_latitude_and_longitude( lat_long: str) :
	# e.g. 51.656660,-1.194251

	try:
		lat, long = lat_long.split(",")
	except ValueError:
		return lat_long
	
	return lat, long