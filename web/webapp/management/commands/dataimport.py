import os, os.path, glob

import tomli

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string

from webapp.models import Analysis, Detection, Detector, Position, Species
from webapp.indexers.indexer import Indexer


class Command(BaseCommand):
	help = 'Enter new data into the database. Do not override old data.'

	# DATA_FOLDER = "/media/matthew/Data/Git/Work/Earth Trust/ETWeb/data/"
	DATA_FOLDER = "/media/matthew/Data/Git/Work/Earth Trust/ETWeb/data-test/"
	
	def handle(self, *args, **options):
		
		self.stdout.write("Work in progress....!!!!")

		# self.stdout.write(os.getcwd()) /media/matthew/Data/Git/Work/Earth Trust/ETWeb/web

		meta_file_name = "meta.toml"

		dirs = os.listdir(Command.DATA_FOLDER)
		for name in dirs:
			data_folder_analysis = os.path.join( Command.DATA_FOLDER, name )
			self.stdout.write( f"Processing '{name}' folder ({data_folder_analysis})" )

			metafile = os.path.join( data_folder_analysis, meta_file_name )
			try:
				with open(metafile, "rb") as f:
					meta = tomli.load(f)
			except IOError:
				self.stderr.write( f"- Error: Missing metafile ({metafile})" )
				continue


			uuid = meta['position']['uuid']
			try:
				position = Position.objects.get(uuid=uuid)
			except Position.DoesNotExist:
				self.stderr.write( f"- Error: Position NOT found with id ({uuid})" )
				continue
			except ValidationError:
				self.stderr.write( f"- Error: Position does not have valid uuid '{uuid}'" )
				continue

			uuid = meta['analysis']['uuid']
			try:
				analysis = Analysis.objects.get(uuid=uuid)
			except Analysis.DoesNotExist:
				self.stderr.write( f"- Error: Analysis NOT found with id ({uuid})" )
				continue
			except ValidationError:
				self.stderr.write( f"- Error: Analysis does not have valid uuid '{uuid}'" )
				continue

			uuid = meta['detector']['uuid']
			try:
				detector = Detector.objects.get(uuid=uuid)
			except Detector.DoesNotExist:
				self.stderr.write( f"- Error: Detector NOT found with id ({uuid})" )
				continue
			except ValidationError:
				self.stderr.write( f"- Error: Detector does not have valid uuid '{uuid}'" )
				continue
				
			try:
				indexer = self.get_indexer_class( meta["indexer"]["class_name"] )
			except ImportError:
				self.stderr.write( f"- Error: Failed to find indexer for '{meta['indexer']['class_name']}'" )
				continue	


			data_folder_analysis_data = data_folder_analysis + "/*." + meta["indexer"]["file_types"]
			data_file_paths = glob.glob(data_folder_analysis_data)
			
			if len(data_file_paths) == 0 :
				self.stderr.write( f"- Error: No files found to process ({data_folder_analysis_data})" )
				continue
				
			self.stdout.write( f"- Indexer: {indexer}" )
			self.stdout.write( f"- Position: {position} ({position.uuid})" )
			self.stdout.write( f"- Detector: {detector} ({detector.uuid})" )
			self.stdout.write( f"- Analysis: {analysis} ({analysis.uuid})" )
			self.stdout.write( f"- Files: {len(data_file_paths)} {meta['indexer']['file_types']}" )

			
			success = indexer.index_data(position, detector, analysis, data_file_paths)
			if not success:
				self.stderr.write( f"- Error: Problem in (Indexer:{indexer})" )


	def get_indexer_class(self, class_name:str ) -> Indexer:
		"""
		This just returns the indexer for the current data
		(It's really in function so my IDE recognises it is of type Indexer ;) )
		:param class_name: A string from the meta file saying which class to load
		:return: An instance of the class
		"""
		class_name_lower = class_name.lower()
		return import_string(f'webapp.indexers.{class_name_lower}.{class_name}')(self.stdout, self.stderr)


