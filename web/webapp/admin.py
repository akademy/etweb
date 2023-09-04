from django.contrib import admin

from django.contrib import admin

from .models import Position, Detector, Species, Detection

admin.site.register(Position)
admin.site.register(Detector)
admin.site.register(Species)
admin.site.register(Detection)