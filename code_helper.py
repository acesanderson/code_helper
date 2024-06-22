import importlib.util
import argparse
import os
import subprocess

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

def get_gitignore(repo_path: str) -> str:
	"""
	Find the .gitignore file in the repository if it exists and return the content.
	"""
	gitignore_path = os.path.join(repo_path, ".gitignore")
	if os.path.exists(gitignore_path):
		with open(gitignore_path, "r") as f:
			gitignore = f.read().split('\n')
			return gitignore
	return "No .gitignore file found"

def exclude_gitignored_files(list_of_files, gitignore: list) -> list:
	"""
	Looks through a list of files and determines which ones are gitignored.
	Returns a list of the files that are NOT gitignored.
	"""
	# Remove empty lines from the gitignore
	gitignore = [line for line in gitignore if line]
	# Remove comments from the gitignore
	gitignore = [line for line in gitignore if not line.startswith("#")]
	# Remove the files that are gitignored
	for line in gitignore:
		# Remove the gitignore line from the list of files
		list_of_files = [file for file in list_of_files if line not in file]
	return list_of_files


def get_tree(repo_path: str) -> str:
	"""
	Takes the repo path and returns the tree structure of the repository as a string.
	This will go at the top of the module_file to provide more context for the LLM.
	"""
	subprocess.run(["tree", repo_path, "-o", "tree.txt"])
	# read the result from the file
	with open("tree.txt", "r") as f:
		tree = f.read()
	# remove the file after reading
	os.remove("tree.txt")
	# use exclude_gitignored_files to remove gitignored files from the tree
	gitignore = get_gitignore(repo_path)
	if gitignore != "No .gitignore file found":
		tree = exclude_gitignored_files(tree.split('\n'), gitignore)
	tree = "\n".join(tree)
	return tree

def combine_code_files(repo_path, module_name):
	"""
	Takes the path and the module name, and it saves a combined file of the repo to a file with the module name + '.txt'
	"""
	output_file = f'module_files/{module_name}.txt'
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