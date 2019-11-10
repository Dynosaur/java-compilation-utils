'''
author: https://github.com/Dynosaur
version: 1.0
'''

import os, json
from pathlib import Path

class Project:

	def __init__(self):
		self.path = os.getcwd()
		self.info_file_path = self.path + '\\info.json'

		if os.path.exists(self.info_file_path):
			info_file = open(self.info_file_path)
			try:
				data = json.load(info_file)
				
				abs_dir = data['abs_dir']
				if abs_dir != self.path:
					raise ValueError(self.info_file_path + ' has an abs_dir path for another directory.')
				else:
					self.abs_dir = abs_dir
				
				src_dir = data['src_dir']
				if not os.path.exists(src_dir):
					raise ValueError(self.info_file_path + ' source directory does not exist.')
				else:
					self.src_dir = src_dir
				
				out_dir = data['out_dir']
				if not os.path.exists(out_dir):
					raise ValueError(self.info_file_path + ' output directory does not exist.')
				else:
					self.out_dir = out_dir
					
				info_file.close()
			except json.decoder.JSONDecodeError:
				info_file.close()
				self.bad_info_file()
			except ValueError as e:
				info_file.close()
				print(str(e))
				self.bad_info_file()
		else:
			while True:
				user_input = input('Could not find ' + self.info_file_path + ', would you like to generate a new one? (y/n) ')
				if user_input.casefold().startswith('y'):
					self.new_info_file()
					break
				elif user_input.casefold().startswith('n'):
					exit()
	
	def bad_info_file(self):
		while True:
			user_input = input(self.info_file_path + ' is corrupted, would you like to make a new one? (y/n) ')
			if user_input.casefold().startswith('y'):
				self.new_info_file()
				return
			elif user_input.casefold().startswith('n'):
				print('It is reccomended that you delete info.json, then rerun this script to generate a new one.')
				exit()

	def new_info_file(self):
		if os.path.exists(self.info_file_path):
			os.remove('info.json')
		info_file = open("info.json", "w+")
		self.abs_dir = os.getcwd()
		self.src_dir = self.get_source_folder()
		self.out_dir = self.get_output_folder()
		data = {
			'abs_dir': self.abs_dir,
			'src_dir': self.src_dir,
			'out_dir': self.out_dir,
		}
		print('Writing new data to info.json...')
		info_file.write(json.dumps(json.loads(json.dumps(data)), indent=4))
		print('Done.')
		
	def get_source_folder(self):
		guess_dir = self.path + '\\src'
		if os.path.exists(guess_dir):
			while True:
				src_correct = input('\nIs ' + guess_dir + ' your source folder? (y/n) ')
				if src_correct.casefold().startswith('y'):
					return guess_dir
				elif src_correct.casefold().startswith('n'):
					break
		while True:
			source_dir = self.path + '\\' + input('\nWhere is your source folder? ' + os.path.basename(self.path) + '\\')
			if os.path.exists(source_dir):
				if os.path.isdir(source_dir):
					return source_dir
				else:
					print('The specified path is not a directory.')
			else:
				print('The specified path does not exist.')

			while True:
				create_new = input('Would you like to create it? ')
				if create_new.casefold().startswith('y'):
					os.mkdir(source_dir)
					return source_dir
				elif create_new.casefold().startswith('n'):
					break

	def get_output_folder(self):
		guess_dir = self.path + '\\out'
		if os.path.exists(guess_dir):
			while True:
				out_correct = input('Is ' + guess_dir + ' your output folder? (y/n) ')
				if out_correct.casefold().startswith('y'):
					return guess_dir
				elif out_correct.casefold().startswith('n'):
					break
		while True:
			output_dir = self.path + '\\' + input('Where is your output folder? ' + os.path.basename(self.path) + '\\')
			if os.path.exists(output_dir):
				return output_dir
			else:
				print('The specified path does not exist.\n')

			while True:
				create_new = input('Would you like to create it? ')
				if create_new.casefold().startswith('y'):
					os.mkdir(output_dir)
					return output_dir
				elif create_new.casefold().startswith('n'):
					break

	def javac(self, file):
			print('Compiling ' + file + '...')
			command = 'javac -classpath ' + self.out_dir + ' ' + file + ' -d ' + self.out_dir
			os.system(command)
			print('Done.')
	
	def compile(self, dir = 'default'):
		if dir == 'default':
			print('Compiling project...')
			self.compile(self.src_dir)
			return
		print('Searching ' + dir + '...')
		file_list = os.listdir(dir)
		if len(file_list) == 0:
			print('No files found.')
		else:
			for file in file_list:
				if os.path.isdir(dir + '/' + file):
					self.compile(dir + '/' + file)
				else:
					if file.endswith('.java'):
						self.javac(dir + '/' + file)

print()
project = Project()
project.compile()