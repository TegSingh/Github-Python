import csv
from git import Repo
import os
import sys

# Set the number of commit details to print
COMMITS_TO_PRINT = int(sys.argv[2])

def print_commit(commit):
    print("----------------------------------------------------------------------------")
    print("Hash code: ", str(commit.hexsha))
    print("Commit summary: ", commit.summary)
    print("Author name: {} email: {}".format(commit.author.name, commit.author.email))
    print("Parents: ", commit.parents)
    print("Datetime commit was authorized: ", str(commit.authored_datetime))
    message = commit.message.split('\n')
    if len(message) == 3:
        print("Commit Message: ", message[2])
    else: 
        print("Commit Message: ", message[0])
    print(str("Commit Number: {} and Size: {}".format(commit.count(), commit.size)))
    print("Number of Files changed: ", len(commit.stats.files.keys()))

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

    try: 
        f = open('commit_info.csv', 'w')
        print("File opened successfully")
    except: 
        print("Error opening file")

    try: 
        writer = csv.writer(f)
        print("Writer created successfully")
    except: 
        print("Error creating writer")

    tableheader = ['Summary', 'Hex code', 'Author Name', 'Author email', 'Parents', 'Date and Time', 'Message', 'Commit number', 'Commit size', "#Files changed"]
    
    try:
        writer.writerow(tableheader)
        print("Header written sucessfully")
    except:
        print("Error writing to csv file")

    # List all commits
    commit_list = list(repo.iter_commits(repo_branch))
    for i in range(0, COMMITS_TO_PRINT):
        commit = commit_list[i]
        # Print commits if need be
        print_commit(commit)
        message = commit.message.split('\n')
        if len(message) == 3:
            result = message[2]
        else: 
            result = message[0]
        commit_row = [commit.summary, commit.hexsha, commit.author.name, commit.author.email, commit.parents, commit.authored_datetime, result, commit.count(), commit.size, len(commit.stats.files.keys())]
        writer.writerow(commit_row)
   
    print("----------------------------------------------------------------------------")
    # Clean up
    print("Cleaning up")
    os.system('rm -rf GitRepo/')
    f.close()

if __name__ == '__main__': 
    main()