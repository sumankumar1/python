import os
import re
import pandas as pd
from git import Repo

def clone_github_repo(repo_url, local_dir):
    """
    Clones a GitHub repository to a local directory.
    
    Parameters:
        repo_url (str): URL of the GitHub repository.
        local_dir (str): Path to clone the repository to.

    Returns:
        str: Path to the cloned repository.
    """
    if os.path.exists(local_dir):
        print(f"Repository already exists at {local_dir}. Pulling latest changes...")
        repo = Repo(local_dir)
        repo.remotes.origin.pull()
    else:
        print(f"Cloning repository from {repo_url} to {local_dir}...")
        Repo.clone_from(repo_url, local_dir)
    return local_dir

def analyze_repository(repo_path):
    """
    Analyzes a software repository for missing documentation and poorly commented code.
    
    Parameters:
        repo_path (str): Path to the root of the repository.

    Returns:
        pd.DataFrame: Summary of the analysis for each Python file.
    """
    results = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                analysis = analyze_file(file_path)
                results.append(analysis)

    return pd.DataFrame(results)

def analyze_file(file_path):
    """
    Analyzes a single Python file for documentation and comment quality.

    Parameters:
        file_path (str): Path to the Python file.

    Returns:
        dict: Analysis results for the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    docstring_lines = count_docstring_lines(lines)
    comment_lines = count_comment_lines(lines)

    return {
        "File": file_path,
        "Total Lines": total_lines,
        "Docstring Coverage (%)": round((docstring_lines / total_lines) * 100, 2) if total_lines > 0 else 0,
        "Comment Coverage (%)": round((comment_lines / total_lines) * 100, 2) if total_lines > 0 else 0,
    }

def count_docstring_lines(lines):
    """
    Counts the lines covered by docstrings in a Python file.

    Parameters:
        lines (list): List of lines in the file.

    Returns:
        int: Number of docstring lines.
    """
    docstring_pattern = r'"""'
    inside_docstring = False
    docstring_lines = 0

    for line in lines:
        if re.search(docstring_pattern, line):
            inside_docstring = not inside_docstring
            docstring_lines += 1
        elif inside_docstring:
            docstring_lines += 1

    return docstring_lines

def count_comment_lines(lines):
    """
    Counts the lines with comments in a Python file.

    Parameters:
        lines (list): List of lines in the file.

    Returns:
        int: Number of comment lines.
    """
    comment_pattern = r"#"
    comment_lines = sum(1 for line in lines if re.search(comment_pattern, line.strip()))
    return comment_lines
	
	
# Define the GitHub repository URL and local directory
github_repo_url = "https://github.com/sumankumar1/python.git"
local_repository_path = "./cloned_repo_python"

# Clone the repository
repo_path = clone_github_repo(github_repo_url, local_repository_path)

# Analyze the repository
results_df = analyze_repository(repo_path)

# Display the results
results_df