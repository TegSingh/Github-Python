import csv
from git import Repo
import os
import sys

# Set the number of commit details to print
NUMBER_OF_COMMITS = int(sys.argv[2])
# Keys: File names, Values: number of authors that contributed to the file
file_dict = {}
    

# Method to print information about the commit
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

# Method to print file_dict dictionary
def print_file_dict():
    for key in file_dict.keys():
        print('Number of commits for file ', key, ': ', file_dict[key])
    print(len(file_dict.keys()))

# Method to initialize the file_dictionary
def initCommitsPerFile(commit_list, n):    
    for i in range(0, n):
        commit = commit_list[i]
        file_info = commit.stats.files
        for key in file_info.keys():
            file_dict[key] = 0
            # print('key: ', key, ', value: ', file_dict[key])
        
# Method to calculate the number of authors that contributed to a file
def calculateCommitsPerFile(commit):        
    file_info = commit.stats.files
    # Increase the value for each file
    for key in file_info.keys():
        file_dict[key] += 1
        print('key: ', key, ', value: ', file_dict[key])


# Method to calculate all the line changes made in one commit in all files
def calculateFileChanges(commit):
    file_keys = commit.stats.files.keys()
    file_info = commit.stats.files
    total_insertions = 0
    total_deletions = 0
    total_lines_changed = 0

    for key in file_keys:        
        changes_list = file_info[key]
        for i in changes_list.keys():
            if i == 'insertions':
                total_insertions += changes_list[i] 
            if i == 'deletions':
                total_deletions += changes_list[i]
            if i == 'lines':
                total_lines_changed += changes_list[i]
        
    return total_insertions, total_deletions, total_lines_changed

# Method to write file dictionary containing commits per file to a csv
def write_file_dict_to_csv(): 
    f = open('Results/File_info/file_info.csv', 'w')
    writer = csv.writer(f)
    table_header = ['File Name and Path', 'Number of commits']
    writer.writerow(table_header)
    for key in file_dict.keys():
        row = [key, file_dict[key]]
        writer.writerow(row)

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
        f = open('Results/Commit_info/commit_info.csv', 'w')
        print("File opened successfully")
    except: 
        print("Error opening file")

    try: 
        writer = csv.writer(f)
        print("Writer created successfully")
    except: 
        print("Error creating writer")

    tableheader = ['Summary', 'Hex code', 'Author Name', 'Author email', 'Parents', 'Date and Time', 'Message', 'Commit number', 'Commit size', "#Files changed", '#Lines Inserted', '#Lines Deleted', '#Lines Changed']
    
    try:
        writer.writerow(tableheader)
        print("Header written sucessfully")
    except:
        print("Error writing to csv file")

    # List all commits
    commit_list = list(repo.iter_commits(repo_branch))
    # Initialize the number of commits per file
    initCommitsPerFile(commit_list, NUMBER_OF_COMMITS)
    
    for i in range(0, NUMBER_OF_COMMITS):
        commit = commit_list[i]
        # print_commit(commit)
        # Changes on Files
        total_insertions, total_deletions, total_lines_changed = calculateFileChanges(commit)
        # Commits of messages
        message = commit.message.split('\n')
        if len(message) == 3:
            result = message[2]
        else: 
            result = message[0]
        # Calculate the number of commits per file
        calculateCommitsPerFile(commit)

        # Write to CSV file
        commit_row = [commit.summary, commit.hexsha, commit.author.name, commit.author.email, commit.parents, commit.authored_datetime, result, commit.count(), commit.size, len(commit.stats.files.keys()), total_insertions, total_deletions, total_lines_changed]
        writer.writerow(commit_row)
        
    print("----------------------------------------------------------------------------")
    
    # Write file_dict to csv file and print that information
    print("Writing Number of commits per file to csv file")
    # print_file_dict()
    write_file_dict_to_csv()

    # Clean up
    print("Cleaning up")
    os.system('rm -rf GitRepo/')
    f.close()

if __name__ == '__main__': 
    main()