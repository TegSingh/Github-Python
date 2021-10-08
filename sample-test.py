import os
import sys
import csv

# Initialize the values required
tests_total = 0
duration_avg = 0
duration_min = 0 
duration_max = 0
failure_rate = 0
latest_pass = 1
history_length = 1
average_test_total = 0

def main():
    try: 
        file_read = open('Sampledataset-Sheet1.csv', 'r')
        file_write = open('Results/Tests/result.csv', 'w')
    except:
        print("Could not open file and writer")

    writer = csv.writer(file_write)


if __name__ == '__main__':
    main()