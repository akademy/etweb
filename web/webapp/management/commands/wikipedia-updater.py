import time
from urllib.parse import urlparse

from wikipedia import WikipediaException
import wikipedia

from django.core.management.base import BaseCommand
from django.db.models import Q

from webapp.models import Analysis, Detection, Detector, Position, Species


class Command(BaseCommand):
	help = 'Update with Wikipedia data'

	PAUSE_TIME_SECONDS = 3
	
	def handle(self, *args, **options):
		
		species_list = Species.objects \
			.exclude(wikidata_url="") \
			.filter(wikipedia_description="")

		total = len(species_list)
		count = 1
		self.stdout.write( f"{total} species found..." )
	
		for species in species_list:

			self.stdout.write()
			self.stdout.write(f"({count}/{total}) {species.scientific_name} ({species.wikidata_url})")

			wikipedia_id = urlparse( species.wikidata_url ).path.split("/")[-1]
			
			try:
				page = wikipedia.page(wikipedia_id)
			except WikipediaException as we:
				self.stderr.write("Error: There's a WikipediaException: " + str(we) )
				continue

			species.wikipedia_description = page.summary
			species.save()

			count += 1
			time.sleep(Command.PAUSE_TIME_SECONDS)
		
			

