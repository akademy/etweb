import uuid

from django.db import models


class WMModel(models.Model):
	class Meta:
		abstract = True

	uuid = models.UUIDField( default=uuid.uuid4, editable=False, unique=True)

	added = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Position(WMModel):
	name = models.CharField(max_length=500)
	lat_long = models.CharField(max_length=100)
	description = models.TextField(max_length=4096)


class Detector(WMModel):
	position = models.ForeignKey(Position, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	description = models.TextField(max_length=4096)


class Analysis(WMModel):
	name = models.CharField(max_length=500)
	description = models.TextField(max_length=4096)
	url = models.CharField(max_length=500, blank=True)


class Species(WMModel):
	common_name = models.CharField(max_length=500)
	scientific_name = models.CharField(max_length=500)
	description = models.TextField(max_length=4096)

	wikidata_url = models.URLField(max_length=256)
	wikipedia_url = models.URLField(max_length=256)
	wikimedia_url = models.URLField(max_length=256)
	wikimedia_photo_urls = models.URLField(max_length=1033)
	
	def __str__(self):
		return self.common_name


class Detection(WMModel):
	detector = models.ForeignKey(Detector, on_delete=models.CASCADE)
	analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	date = models.DateTimeField("date detected")
	confidence = models.DecimalField(decimal_places=4, max_digits=5)  # Between 0.0000 and 1.0000

	def __str__(self):
		return self.species.common_name + " on " + str(self.date)
