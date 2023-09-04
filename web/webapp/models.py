from django.db import models


class Position(models.Model):
	name = models.CharField(max_length=500)
	lat_long = models.CharField(max_length=100)
	description = models.CharField(max_length=4096)

	def __str__(self):
		return self.name


class Detector(models.Model):
	models.ForeignKey(Position, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	description = models.CharField(max_length=4096)

	def __str__(self):
		return self.name


class Species(models.Model):
	common_name = models.CharField(max_length=500)
	scientific_name = models.CharField(max_length=500)
	description = models.CharField(max_length=4096)

	def __str__(self):
		return self.common_name


class Detection(models.Model):
	detector = models.ForeignKey(Detector, on_delete=models.CASCADE)
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	date = models.DateTimeField("date detected")
	confidence = models.DecimalField(decimal_places=4, max_digits=6)

	def __str__(self):
		return self.species.common_name
