import os, json

def get_source_folder(cwd):
	if os.path.exists('src'):
		while(True):
			src_correct = input('Is "' + cwd + '\\src" your source folder? (y/n) ')
			if src_correct.startswith('y'):
				return 'src'
			elif src_correct.startswith('n'):
				break
	while(True):
		source_dir = input('Where is your source folder? ' + cwd + '\\')
		if os.path.exists(source_dir):
			return source_dir
		else:
			print('The specified path does not exist.\n')

def get_output_folder(cwd):
	if os.path.exists('out'):
		while(True):
			out_correct = input('Is "' + cwd + '\\out" your output folder? (y/n) ')
			if out_correct.startswith('y'):
				return 'out'
			elif out_correct.startswith('n'):
				break
	while(True):
		output_dir = input('Where is your output folder? ' + cwd + '\\')
		if os.path.exists(output_dir):
			return output_dir
		else:
			print('The specified path does not exist.\n')

def write_info_json():
	info_file = open("info.json", "w+")
	cwd = os.getcwd()
	src = get_source_folder(cwd)
	out = get_output_folder(cwd)
	data = {
		'abs_dir': cwd,
		'src_dir': src,
		'out_dir': out,
	}
	print('Writing new data to info.json...')
	info_file.write(json.dumps(data))
	print('Done.')

class Project:

	def __init__(self):
		self.abs_dir = os.getcwd()
		
		info_file_path = self.abs_dir + '\\info.json'
		if os.path.exists(info_file_path):
			data = json.load(open(info_file_path))
			if os.path.exists(data['abs_dir']) and os.path.exists(data['src_dir']) and os.path.exists(data['out_dir']):
				self.abs_dir = data['abs_dir']
				self.src_dir = data['src_dir']
				self.out_dir = data['out_dir']
			else:
				print(info_file_path + ' points to some nonexistent paths. You might want to delete it and rerun this script to generate a new one.')
				exit()
		else:
			print(info_file_path + ' not found!')
			write_info_json()
			data = json.load(open(info_file_path))
			self.abs_dir = data['abs_dir']
			self.src_dir = data['src_dir']
			self.out_dir = data['out_dir']	
		
	def javac(self, file):
		print('Compiling ' + file + '...')
		command = "javac " + file + " -d " + self.out_dir
		os.system(command)
		print('Done.')
		
	def compile(self, dir = 'default'):
		if dir == 'default':
			print('Compiling project...')
			self.compile(self.src_dir)
			return
		print('Searching ' + dir + '...')
		for file in os.listdir(dir):
			if os.path.isdir(dir + '/' + file):
				self.compile(dir + '/' + file)
			else:
				if file.endswith('.java'):
					self.javac(dir + '/' + file)

project = Project()
project.compile()