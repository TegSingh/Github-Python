import csv
from git import Repo
import os
import sys
import datetime

# Set the number of commit details to print
NUMBER_OF_COMMITS = int(sys.argv[2])

# Dictionary of Dictionaries
author_dict = {}
author_list = []

# Method to initialize author dictionary
def init_author_dict():
    for author in author_list:
        author_dict[author] = {"number_of_commits": 0, "first_commit_hex": "", "first_commit_time": "", "last_commit_hex": "", "last_commit_time": "", "frequency": 0.0, "0-4": 0, "4-8": 0, "8-12" : 0, "12-16": 0, "16-20" : 0, "20-24": 0}


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

    # Convert the datetime object to some time value
    # Note: The commit object also gives the timezone relative to the UTC (GMT)
    authored_time = datetime.time(commit.authored_datetime.hour, commit.authored_datetime.minute, commit.authored_datetime.second)
    
    # Add the number of commits in a particular timeslot [4 hour long timeslots]
    if authored_time >= datetime.time(0, 0, 0) and authored_time <= datetime.time(3, 59, 59): 
        author_dict[commit.author.name]["0-4"] += 1
    if authored_time >= datetime.time(4, 0, 0) and authored_time <= datetime.time(7, 59, 59):     
        author_dict[commit.author.name]["4-8"] += 1
    if authored_time >= datetime.time(8, 0, 0) and authored_time <= datetime.time(11, 59, 59):     
        author_dict[commit.author.name]["8-12"] += 1
    if authored_time >= datetime.time(12, 0, 0) and authored_time <= datetime.time(15, 59, 59):     
        author_dict[commit.author.name]["12-16"] += 1
    if authored_time >= datetime.time(16, 0, 0) and authored_time <= datetime.time(19, 59, 59):     
        author_dict[commit.author.name]["16-20"] += 1
    if authored_time >= datetime.time(20, 0, 0) and authored_time <= datetime.time(23, 59, 59):     
        author_dict[commit.author.name]["20-24"] += 1


# Method to calculate commit frequency for a particular author
def calculate_author_commit_frequency(key): 
    time_difference = author_dict[key]["last_commit_time"] - author_dict[key]["first_commit_time"]
    total_seconds = time_difference.total_seconds()
    # Note that the frequency is per day
    total_days = total_seconds / 86400
    if total_days == 0: 
        daily_frequency = 1.000
    else: 
        daily_frequency = author_dict[key]["number_of_commits"]/total_days
    author_dict[key]["frequency"] = round(daily_frequency, 3)


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

    tableheader = ['Author name', 'Number of commits', 'First commit hex', 'First commit time', 'Last commit hex', 'Last commit time', 'Frequency', '0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
    
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

    # List all commits
    commit_list = list(repo.iter_commits(repo_branch))
    
    # initialize author dictionary
    init_author_dict()

    for i in range(len(commit_list)):
        commit = commit_list[i]
        # Update author dictionary after every discovered commit
        update_author_dict(commit)
        
    # Loop through the authors again to find the frequency and activity values
    for key, value in author_dict.items():
        calculate_author_commit_frequency(key)

    # Write to CSV file
    # 0-4, 4-8
    for key, value in author_dict.items():
        author_row = [
            key, 
            author_dict[key]["number_of_commits"],  
            author_dict[key]["first_commit_hex"], 
            author_dict[key]["first_commit_time"], 
            author_dict[key]["last_commit_hex"], 
            author_dict[key]["last_commit_time"], 
            author_dict[key]["frequency"], 
            author_dict[key]["0-4"],
            author_dict[key]["4-8"],
            author_dict[key]["8-12"],
            author_dict[key]["12-16"],
            author_dict[key]["16-20"],
            author_dict[key]["20-24"]
        ]
        writer.writerow(author_row)
     
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