import csv

try: 
    f = open('commit_info.csv', 'w')
    print("File opened successfully")
except: 
    print("Error opening file")

try: 
    writer = csv.writer(f)
except: 
    print("Error creating writer")

tableheader = ['name', 'age']
data = ['Tegveer', 20]

try:
    writer.writerow(tableheader)
    writer.writerow(data)
except:
    print("Error writing to csv file")
f.close()