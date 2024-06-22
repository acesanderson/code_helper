import importlib.util
import argparse
import os

def get_package_path(import_name: str) -> str:
	"""
	Enter the name of the module, it returns the path to the directory containing the module.
	"""
	try:
		# Load the module based on the import name
		spec = importlib.util.find_spec(import_name)
		if not spec:
			print(f"No module named '{import_name}' found")
			return None
		# Get the path to the module
		module_path = spec.origin
		# Return the directory containing the module
		return os.path.dirname(module_path)
	except ModuleNotFoundError:
		print(f"No module named '{import_name}' found")
		return None
	except AttributeError:
		print(f"Could not determine the path for the module named '{import_name}'")
		return None

def combine_code_files(repo_path, module_name):
	"""
	Takes the path and the module name, and it saves a combined file of the repo to a file with the module name + '.txt'
	"""
	output_file = module_name + '.txt'
	with open(output_file, 'w', encoding='utf-8') as outfile:
		for root, dirs, files in os.walk(repo_path):
			for file in files:
				file_path = os.path.join(root, file)
				# Skip the output file itself if it's in the repository
				if file_path == output_file:
					continue
				# You can add more file extensions as needed
				if file.endswith(('.py', '.js', '.java', '.cpp', '.h', '.c', '.cs', '.html', '.css')):
					try:
						with open(file_path, 'r', encoding='utf-8') as infile:
							outfile.write(f"======\n{file_path}\n=======\n")
							outfile.write(infile.read())
							outfile.write("\n\n")
					except Exception as e:
						print(f"Error processing {file_path}: {str(e)}")

def main():
	parser = argparse.ArgumentParser(description="Find a python library path by import name.")
	# Add arguments
	parser.add_argument("input_string", type=str, help="A simple input string")
	# Parse the arguments
	args = parser.parse_args()
	# Access the arguments
	import_name = args.input_string
	package_path = get_package_path(import_name)
	if package_path:
		print(f"The installation path for {import_name} is: {package_path}")
	else:
		print("Module not found.")


module_name = "instructor"
repo_path = get_package_path(module_name)
combine_code_files(repo_path, module_name)

# if __name__ == "__main__":
#     repo_path = input("Enter the path to the repository: ")
#     output_file = input("Enter the name of the output file: ")
	
#     combine_code_files(repo_path, output_file)
#     print(f"All code files have been combined into {output_file}")