import csv
from git import Repo
import os
import sys

# Set the number of commit details to print
COMMITS_TO_PRINT = 0

def main(): 
    # Read command line arguments
    repo_remote = sys.argv[1]
    repo_url = sys.argv[3]

    if repo_remote == 'remote':
        # Use github link
        try: 
            Repo.clone_from(repo_url, 'GitRepo')
            print("Remote repository cloned successfully")
        except: 
            print("Couldn't clone repository")

    # Get the number of commits to be printed
    COMMITS_TO_PRINT = sys.argv[2]
    

    try:
        repo = Repo('GitRepo')
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

    tableheader = ['name', 'age']
    data = [['Tegveer', 20], 
            ['Hello world', 21],
            ['lorem', 23], 
            ['ipsum', 19]]

    try:
        writer.writerow(tableheader)
        writer.writerows(data)
        print("Rows written sucessfully")
    except:
        print("Error writing to csv file")
    
    # Clean up
    print("Cleaning up")
    os.system('rm -rf GitRepo/')
    f.close()

if __name__ == '__main__': 
    main()