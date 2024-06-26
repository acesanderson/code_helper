import argparse
import subprocess
import os
import re

def run_and_capture_command(command):
    """
    Run a command and capture its output.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return f"Command Output:\n{result.stdout}\nError Output:\n{result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Command failed with exit code {e.returncode}.\nOutput:\n{e.output}\nError:\n{e.stderr}"

def get_shell_history(num_commands=10):
    """
    Retrieve the last N commands from the shell history file.
    """
    history_file = os.path.expanduser('~/.bash_history')  # Default to bash history
    if 'ZSH_VERSION' in os.environ:
        history_file = os.path.expanduser('~/.zsh_history')
    
    if not os.path.exists(history_file):
        return "No history file found."

    try:
        with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
            history = f.readlines()
        
        # Clean and get the last N commands
        cleaned_history = []
        for line in reversed(history):
            # Remove timestamps for zsh history
            line = re.sub(r'^: \d+:\d+;', '', line.strip())
            if line and not line.startswith('#'):
                cleaned_history.append(line)
                if len(cleaned_history) == num_commands:
                    break
        
        return "Recent Commands:\n" + "\n".join(reversed(cleaned_history))
    except Exception as e:
        return f"Failed to retrieve shell history.\nError:\n{str(e)}"

def get_current_directory():
    """
    Get the current working directory.
    """
    return f"Current Directory: {os.getcwd()}"

def get_environment_vars():
    """
    Get relevant environment variables.
    """
    relevant_vars = ['PWD', 'HOME', 'USER', 'SHELL', 'TERM', 'PATH']
    env_info = "Environment Variables:\n"
    for var in relevant_vars:
        env_info += f"{var}: {os.environ.get(var, 'Not set')}\n"
    return env_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture terminal information and run commands.")
    parser.add_argument("-c", "--command", help="The command to run and capture")
    parser.add_argument("-n", "--num_history", type=int, default=10, help="Number of recent commands to retrieve from history")
    args = parser.parse_args()

    print(get_current_directory())
    print("\n" + get_environment_vars())
    print("\n" + get_shell_history(args.num_history))

    if args.command:
        print("\n" + run_and_capture_command(args.command))