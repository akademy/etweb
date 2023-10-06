import csv
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from webapp.models import Analysis, Detection, Detector, Position, Species
from webapp.indexers.indexer import Indexer


class BTO(Indexer):
	
	def index_data(self, position, detector, analysis, file_path_list):
		
		for path in file_path_list:

			species_dict = {}
			with open(path, newline='') as csv_file:
				reader = csv.DictReader(csv_file)
				for row in reader:

					if row["SPECIES"] in ["bird", "No ID"] :
						continue

					confidence = float(row["PROBABILITY"])
					if confidence < Indexer.CONFIDENCE_LIMIT :
						continue
					
					detection_time = datetime.strptime(
						f"{row['ACTUAL DATE']} {row['TIME']}",
						"%d/%m/%Y %H:%M:%S"
					).replace(tzinfo=ZoneInfo(Indexer.TIMEZONE))
					
					scientific_name = row['SCIENTIFIC NAME']
					
					if scientific_name not in species_dict:
						try:
							species = Species.objects.get(scientific_name__iexact=scientific_name)
						except Species.DoesNotExist:
							species = Species.objects.create(
								common_name=row['ENGLISH NAME'],
								scientific_name=scientific_name,
								description=""
							)  # TODO: Add "Species Group" and "Species" to Species table
						species_dict[scientific_name] = species


					try:
						d = Detection.objects.get(
							date__exact=detection_time,
							species=species_dict[scientific_name],
							analysis=analysis
						)
						if d.confidence < confidence:
							d.confidence = confidence
							d.save()
						
					except Detection.DoesNotExist:
						d = Detection.objects.create(
							date=detection_time,
							species=species_dict[scientific_name],
							analysis=analysis,
							confidence=confidence
						)

		return True
		
