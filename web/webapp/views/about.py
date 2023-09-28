from django.shortcuts import render

from ..models import Species


def about(request):
	return render(request, "about.html")

