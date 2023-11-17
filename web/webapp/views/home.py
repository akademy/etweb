from django.shortcuts import render


from ..models import Analysis, Detection, Detector, Position, Species


def index(request):

	position_number = Position.objects.count()
	detection_number = Detection.objects.count()
	species_number = Species.objects.count()
	
	context = {
		"position_number": position_number,
		"detection_number": detection_number,
		"species_number": species_number,
	}
	
	return render(request, "home.html", context )


def explore(request):

	analysis_number = Analysis.objects.count()
	detection_number = Detection.objects.count()
	detector_number = Detector.objects.count()
	position_number = Position.objects.count()
	species_number = Species.objects.count()

	context = {
		"analysis_number": analysis_number,
		"detection_number": detection_number,
		"detector_number": detector_number,
		"position_number": position_number,
		"species_number": species_number,
	}
	
	return render(request, "explore.html", context )

