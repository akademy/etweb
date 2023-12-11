import csv
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from webapp.models import Analysis, Detection, Detector, Position, Species
from webapp.indexers.indexer import Indexer


class BirdNet(Indexer):

	def index_data(self, position, detector, analysis, file_path_list):
		
		file_total = len(file_path_list)
		file_count = 1
		for path in file_path_list:
			
			self.out(f"({file_count}/{file_total}) Processing {path}")

			try:
				recording_time = self._datetime_from_filename(path)
			except (IndexError, ValueError):
				self.error( f"Wrong filename, can't extract date-time. ({path})")
				return False

			species_dict = {}
			with open(path, newline='') as csv_file:
				reader = csv.DictReader(csv_file)
				for row in reader:

					scientific_name = row['Scientific name']
					if scientific_name not in species_dict:
						try:
							species = Species.objects.get(scientific_name__iexact=scientific_name)
						except Species.DoesNotExist:
							species = Species.objects.create(
								common_name=row['Common name'],
								scientific_name=scientific_name,
								description=""
							)
						species_dict[scientific_name] = species


					confidence = float(row["Confidence"])
					detection_time = recording_time + timedelta(seconds=float(row['Start (s)']))
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
			file_count += 1
			
		return True

	
	@staticmethod
	def _datetime_from_filename(path):
		"""
		Extract date and time from filename
			e.g. "EARTH_20220809_025600.BirdNET.results.csv"
		:param filename: filename or filepath
		:return: dict {'filename': filename, 'date': date, 'time': time}
		:raise: ValueError if can't read data from name
		"""
		filename = os.path.basename(path).replace(",", "-")
		date_and_time = filename.split("_")
		date = date_and_time[1]
		time = date_and_time[2].split(".")[0]

		# test are numbers
		_ = int(date)
		_ = int(time)

		return datetime.strptime(f"{date} {time}", "%Y%m%d %H%M%S").replace(tzinfo=ZoneInfo(Indexer.TIMEZONE))
		
