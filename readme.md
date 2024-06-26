# Code Helper Overview

This script, code_helper.py, is a utility for debugging and collaborative coding with Language Learning Models (LLMs). Its main functions are:

- Combining all code files from a specified module or repository into a single file.
- Generating a tree structure of the repository.
- Copying the combined code and tree structure to the clipboard.

## Key Features:

- Can be run with a module name, a path to a repository, or in the current directory.
- Excludes files that are gitignored in the repository.
- Generates a tree structure of the repository for context.
- Supports various file extensions (.py, .js, .java, .cpp, .h, .c, .cs, .html, .css).
- Copies the output to the clipboard for easy pasting into LLM interfaces like Claude.

## Main Components:

- Command-line interface: Uses argparse to handle different input methods (module name, path, or current directory).
- Module/package handling: Functions to check if a package exists and find its path.
- File processing: Functions to walk through directories, read files, and combine their contents.
- Gitignore handling: Functions to read and apply .gitignore rules.
- Tree structure generation: Uses the tree command to generate a visual representation of the repository structure.
- Clipboard interaction: Uses pyperclip to copy the output to the clipboard.

## Usage:

```bash
python code_helper.py <module_name>: Combines code from a specified Python module.
python code_helper.py -p /path/to/repo: Combines code from a specified repository path.
python code_helper.py -c: Combines code from the current directory.
```

The script generates a file named <module_name>.txt or <directory_name>.txt containing the combined code and tree structure.