from django.shortcuts import render

from ..models import Species


def index(request):
	return render(request, "home.html")
