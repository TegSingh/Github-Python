import csv
from git import Repo
import os
import sys

# Set the number of commit details to print
NUMBER_OF_COMMITS = int(sys.argv[2])
author_names = []

def main(): 
    # Read command line arguments
    repo_remote = sys.argv[1]
    repo_url = sys.argv[3]
    repo_branch = sys.argv[4]

    if repo_remote == 'remote':
        # Use github link
        try: 
            Repo.clone_from(repo_url, 'GitRepo')
            print("Remote repository cloned successfully")
        except: 
            print("Couldn't clone repository")

    try:
        repo = Repo(repo_url)
        print("Repo instance loaded sucessfully")
    except: 
        print("Could not load repository instance")

    # List all commits
    commit_list = list(repo.iter_commits(repo_branch))
    
    for i in range(len(commit_list)):
        commit = commit_list[i]
        author_names.append(commit.author.name)
        
    for value in set(author_names): 
        print(value)

if __name__ == '__main__': 
    main()