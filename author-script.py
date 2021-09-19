import csv
from git import Repo
import os
import sys

# Set the number of commit details to print
NUMBER_OF_COMMITS = int(sys.argv[2])

# Dictionary of Dictionaries
author_dict = {}
author_list = []

# Method to initialize author dictionary
def init_author_dict():
    for author in author_list:
        author_dict[author] = {"number_of_commits": 0, "first_commit_hex": "", "first_commit_time": "", "last_commit_hex": "", "last_commit_time": "", "frequency": 0.0, "time_of_most_activity": ""}
    
def update_author_dict(commit):
    author_dict[commit.author.name]["number_of_commits"] += 1
    

    # set initial values for the first commit
    if author_dict[commit.author.name]["first_commit_time"] == "":
        author_dict[commit.author.name]["first_commit_hex"] = commit.hexsha
        author_dict[commit.author.name]["first_commit_time"] = commit.authored_datetime
    
    # set initial values for the last commit
    if author_dict[commit.author.name]["last_commit_time"] == "":
        author_dict[commit.author.name]["last_commit_hex"] = commit.hexsha
        author_dict[commit.author.name]["last_commit_time"] = commit.authored_datetime
    

    # update the first commit values
    if commit.authored_datetime < author_dict[commit.author.name]["first_commit_time"]:
        author_dict[commit.author.name]["first_commit_hex"] = commit.hexsha
        author_dict[commit.author.name]["first_commit_time"] = commit.authored_datetime
    
    # update the last commit values
    if commit.authored_datetime > author_dict[commit.author.name]["last_commit_time"]:
        author_dict[commit.author.name]["last_commit_hex"] = commit.hexsha
        author_dict[commit.author.name]["last_commit_time"] = commit.authored_datetime
    
# Main method
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
        f = open('Results/Author_info/author_info.csv', 'w')
        print("File opened successfully")
    except: 
        print("Error opening file")

    try: 
        writer = csv.writer(f)
        print("Writer created successfully")
    except: 
        print("Error creating writer")

    tableheader = ['Author name', 'Author email', 'Number of commits', 'First commit hex', 'First commit time', 'Last commit hex', 'Last commit time', 'Frequency', 'Time of most activity']
    
    try:
        writer.writerow(tableheader)
        print("Header written sucessfully")
    except:
        print("Error writing to csv file")

    # Read author names and store them in an array
    try: 
        with open('Results/Author_info/author_name_list.txt', 'r') as f:
            for author in f:
                # Remove the eol character
                author = author.replace('\n', '')
                # Add to list
                author_list.append(author)
    except:
        print("Error loading author file")

    print(author_list)
    # List all commits
    commit_list = list(repo.iter_commits(repo_branch))
    
    # initialize author dictionary
    init_author_dict()

    for i in range(len(commit_list)):
        commit = commit_list[i]
        # Update author dictionary after every discovered commit
        update_author_dict(commit)
        
    # Write to CSV file
    for key, value in author_dict.items():
        author_row = [
            key, 
            author_dict[key]["number_of_commits"],  
            author_dict[key]["first_commit_hex"], 
            author_dict[key]["first_commit_time"], 
            author_dict[key]["last_commit_hex"], 
            author_dict[key]["last_commit_time"], 
            author_dict[key]["frequency"], 
            author_dict[key]["time_of_most_activity"]
        ]
        writer.writerow(author_row)

    # print(author_dict)
    
    # Calculate the number of commits and confirm
    sum = 0
    for key in author_dict: 
        sum += author_dict[key]["number_of_commits"]
    print(sum)
    
    print("----------------------------------------------------------------------------")
    
    # Clean up
    print("Cleaning up")
    f.close()

if __name__ == '__main__': 
    main()