from django.core.management.base import BaseCommand
from webapp.models import Analysis, Detection, Detector, Position, Species


class Command(BaseCommand):
	help = 'Enter wikipedia data into the database. Do not override old data.'

	def handle(self, *args, **options):

		self.stdout.write("Not implemented")
		
			

