import importlib.util
import argparse
import os
import subprocess

def package_exists(import_name: str) -> bool:
	"""
	Enter the name of the module, it returns True if the module exists, False otherwise.
	"""
	try:
		importlib.util.find_spec(import_name)
		return True
	except ModuleNotFoundError:
		return False

def get_package_path(import_name: str) -> str:
	"""
	Enter the name of the module, it returns the path to the directory containing the module.
	"""
	spec = importlib.util.find_spec(import_name)
	return spec.submodule_search_locations[0] if spec else ""

def gitignore_exists(repo_path: str) -> bool:
	"""
	Enter the path to the repository, it returns True if the .gitignore file exists, False otherwise.
	"""
	gitignore_path = os.path.join(repo_path, ".gitignore")
	return os.path.exists(gitignore_path)

def get_gitignore(repo_path: str) -> str:
	"""
	Find the .gitignore file in the repository if it exists and return the content.
	"""
	gitignore_path = os.path.join(repo_path, ".gitignore")
	with open(gitignore_path, "r") as f:
		gitignore = f.read().split('\n')
	return gitignore

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
	if gitignore_exists(repo_path):
		gitignore = get_gitignore(repo_path)
		tree = exclude_gitignored_files(tree.split('\n'), gitignore)
		tree = "\n".join(tree)
	return tree

def combine_code_files(repo_path, module_name):
	"""
	Takes the path and the module name, and it saves a combined file of the repo to a file with the module name + '.txt'
	"""
	output_file = f'module_files/{module_name}.txt'
	with open(output_file, 'w', encoding='utf-8') as outfile:
		# Add the module name at the top of the file
		outfile.write(f"Module Name: {module_name}\n")
		outfile.write("=============================================\n\n")
		# Add the tree structure at the top of the file
		outfile.write("Tree Structure:\n")
		tree = get_tree(repo_path)
		outfile.write(tree)
		outfile.write("=============================================\n\n")
		for root, dirs, files in os.walk(repo_path):
			for file in files:
				file_path = os.path.join(root, file)
				if gitignore_exists(repo_path):
					gitignore = get_gitignore(repo_path)
					if exclude_gitignored_files([file_path], gitignore) == []:
						continue
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
	"""
	Take user input from command line and combine all code files in the module into a single file.
	"""
	parser = argparse.ArgumentParser(description="Find a python library path by import name.")
	# Add arguments
	parser.add_argument("input_string", type=str, help="A simple input string")
	# Parse the arguments
	args = parser.parse_args()
	# Access the arguments
	module_name = args.input_string
	if package_exists(module_name):
		repo_path = get_package_path(module_name)
		combine_code_files(repo_path, module_name)
		print(f"All code files have been combined into {module_name}.txt")
	else:
		print(f"The module {module_name} does not exist.")


if __name__ == "__main__":
	main()
