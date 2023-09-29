from django.core.management.base import BaseCommand
from webapp.models import Analysis, Detection, Detector, Position, Species


class Command(BaseCommand):
	help = 'Count the data in the database'

	def handle(self, *args, **options):
		
		objects = [
			(Position, "Positions"),
			(Detector, "Detectors"),
			(Analysis, "Analyses"),
			(Detection, "Detections"),
			(Species, "Species")
		]
		
		count_all = 0
		for obj, name in objects:
			count = obj.objects.count()
			self.stdout.write(str(count) + " " + name)
			count_all += count
			
		self.stdout.write()
		self.stdout.write(str(count_all) + " objects in total")
		
			

