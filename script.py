import csv
from git import Repo
import os
import sys

# Set the number of commit details to print
COMMITS_TO_PRINT = 10


def main(): 
    try: 
        Repo.clone_from('https://github.com/TegSingh/DjangoDelights', 'DjangoDelights')
        print("Remote repository cloned successfully")
    except: 
        print("Couldn't clone repository")

    try:
        repo = Repo('DjangoDelights')
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
    f.close()

if __name__ == '__main__': 
    main()