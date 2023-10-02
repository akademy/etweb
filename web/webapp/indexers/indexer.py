from abc import ABC, abstractmethod
from typing import List

from webapp.models import Analysis, Detection, Detector, Position, Species


class Indexer(ABC):

	def __init__(self, stdout, stderr ):
		self.stdout = stdout
		self.stderr = stderr
	
	@abstractmethod
	def index_data(self, position: Position, detector: Detector, analysis: Analysis, file_path_list: List[str]) -> bool:
		pass

	def out(self, message, *ps ):
		self.stdout.write(f"-- {message}", *ps )
		
	def error(self, message, *ps ):
		self.stderr.write(f"-- Error: {message}", *ps )
		
	def __str__(self):
		return self.__class__.__name__.lower() + "." + self.__class__.__name__ 
