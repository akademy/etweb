from django.contrib import admin

from .models import Analysis, Detector, Detection, Position, Species

admin.site.register(Analysis)
admin.site.register(Position)
admin.site.register(Detector)
admin.site.register(Detection)
admin.site.register(Species)
