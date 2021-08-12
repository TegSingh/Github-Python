import csv
from git import Repo

def main(): 
    try: 
        repo = Repo() 
        print("Repo instance loaded successfully")
    except: 
        print("Couldn't load repo instance")

    try: 
        f = open('commit_info.csv', 'w')
        print("File opened successfully")
    except: 
        print("Error opening file")

    try: 
        writer = csv.writer(f)
        print("Writer created successfully")
    except: 
        print("Error creating writer"),

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