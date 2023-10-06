import time
from urllib.parse import urlparse

import wikipedia

from django.core.management.base import BaseCommand
from django.db.models import Q

from webapp.models import Analysis, Detection, Detector, Position, Species


class Command(BaseCommand):
	help = 'Update with Wikipedia data'

	PAUSE_TIME_SECONDS = 3
	
	def handle(self, *args, **options):
		
		species_list = Species.objects.filter(
			Q(wikidata_url__isnull=False) &
			Q(wikipedia_description="")
		)

		self.stdout.write( str(len(species_list)) + " species found..." )
	
		for species in species_list:

			self.stdout.write()
			self.stdout.write(f"{species.scientific_name} ({species.wikidata_url})")

			wikipedia_id = urlparse( species.wikidata_url ).path.split("/")[-1]
			page = wikipedia.page(wikipedia_id)

			species.wikipedia_description = page.summary
			species.save()

			time.sleep(Command.PAUSE_TIME_SECONDS)
		
			

