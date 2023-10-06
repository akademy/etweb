import time
import requests
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
from django.db.models import Q

from webapp.models import Species


class Command(BaseCommand):
	help = 'Enter wikipedia data into the database. Do not override old data.'

	WIKIDATA_URL = 'https://query.wikidata.org/sparql'
	PAUSE_TIME_SECONDS = 3
	
	def handle(self, *args, **options):

		species_list = Species.objects.filter(
			Q(wikidata_url="") | 
			Q(wikipedia_url="") |
			Q(wikimedia_url="") |
			Q(wikimedia_photo_urls="")
		)

		self.stdout.write( str(len(species_list)) + " species found..." )
		
		query_template = self.sparql_wikidata_template()
		for species in species_list:

			self.stdout.write()
			self.stdout.write(species.scientific_name)

			r = requests.get(Command.WIKIDATA_URL, params={
				'format': 'json', 
				'query': query_template.format(scientific_name=species.scientific_name)
			})
			data = r.json()
			# self.stdout.write(str(data))
			
			result = self.collate_result( data )
			
			if result is not None:

				changed = False
				if species.wikidata_url == "":
					species.wikidata_url = result["wikidata"]
					changed = True
					
				if species.wikipedia_url == "":
					species.wikipedia_url = result["wikipedia"]
					changed = True
					
				if species.wikimedia_url == "":
					species.wikimedia_url = result["wikimedia"]
					changed = True

				if species.wikimedia_photo_urls == "":
					species.wikimedia_photo_urls = "###".join(result["wikimedia_photos"])
					changed = True
					
				if changed :
					species.save()
				
				self.stdout.write("wikidata_url: " + species.wikidata_url)
				self.stdout.write("wikipedia_url: " + species.wikipedia_url)
				self.stdout.write("wikimedia_url: " + species.wikimedia_url)
				self.stdout.write("wikimedia_photo_urls: " + str(species.wikimedia_photo_urls) )
			
			time.sleep(Command.PAUSE_TIME_SECONDS)
	
	def collate_result(self, data):
		
		if "results" in data and \
			"bindings" in data["results"] and \
			len(data["results"]["bindings"]):
			
			bidding = data["results"]["bindings"][0]
			results = {
				"wikidata": bidding["wikidata"]["value"] if "wikidata" in bidding else "",
				"wikipedia": bidding["wikipedia"]["value"] if "wikipedia" in bidding else "",
				"wikimedia": bidding["wikimedia"]["value"] if "wikimedia" in bidding else "",
				"wikimedia_photos" : [
					self.adjust_photo_urls(bidding["wikimedia_photos"]["value"])
				] if "wikimedia_photos" in bidding else [],
			}
			
			for bidding in data["results"]["bindings"][1:]:
				
				if bidding["wikidata"]["value"] != results["wikidata"]:
					self.stderr.write("Error: Too many 'wikidata' entries from wikidata")
					return None

				if bidding["wikipedia"]["value"] != results["wikipedia"]:
					self.stderr.write("Error: Too many 'wikipedia' entries from wikidata")
					return None

				if bidding["wikimedia"]["value"] != results["wikimedia"]:
					self.stderr.write("Error: Too many 'wikimedia' entries from wikidata")
					return None

				results["wikimedia_photos"].append( self.adjust_photo_urls(bidding["wikimedia_photos"]["value"]) )
				
			return results
		
		return None
			

	def adjust_photo_urls(self, photo_url):
		
		photo_url_template = "https://commons.wikimedia.org/w/index.php?title=Special:Redirect/file/{file_name}"
	
		parse = urlparse(photo_url)
		photo_file_name = parse.path.split("/")[-1]
		
		return photo_url_template.format(file_name=photo_file_name)


	@staticmethod
	def sparql_wikidata_template():
		# Add double {{ }} to escape
		return """
SELECT  ?wikidata ?wikipedia ?wikimedia ?wikimedia_photos
WHERE 
{{
	?wikidata wdt:P225 "{scientific_name}".
	
	?wikipedia schema:about ?wikidata ;
			schema:inLanguage "en" ;
			schema:isPartOf <https://en.wikipedia.org/>.
	
	OPTIONAL {{
		?wikidata wdt:P18 ?wikimedia_photos.

		?wikimedia schema:about ?wikidata ;
				schema:inLanguage "en" ;
				schema:isPartOf <https://commons.wikimedia.org/>.
	}}
	
	SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
"""

