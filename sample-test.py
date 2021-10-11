import os
import sys
import csv

def main():

    # Initialize the values required
    tests_total = 0
    duration_avg = 0
    duration_min = 0 
    duration_max = 0

    # values to calculate failure rate
    total_tests_passed = 0
    total_tests_failed = 0

    latest_pass = 1
    history_length = 1
    average_test_total = 0
    
    file_write = open('Results/Tests/result.csv', 'w')
    csv_writer = csv.writer(file_write)
    
    with open('Sampledataset-Sheet1.csv') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            # Print the column name
            if line_count == 0:

                line_count += 1
                # Write the first row onto the result file
                table_header = ["Build", "Test suite", "Duration", "Failed", "Average duration", "Maximum duration", "Minimum duration", "Failure rate"]
                csv_writer.writerow(table_header)

            # Print the values for each column
            else:
                
                # Set up the values for the given values
                build = int(row[0])
                test_suite = row[1]
                duration = int(row[2])
                failed = row[3]
                average_duration = 0
                minimum_duration = 0
                maximum_duration = 0
                failure_rate = 0.0

                # Update the average duration
                if line_count == 1:
                    average_duration = duration
                    duration_avg = duration
                else:           
                    duration_avg = (duration_avg*(line_count - 1) + duration) / (line_count)
                    average_duration = duration_avg 

                # Update the maximum duration
                if duration > duration_max:
                    maximum_duration = duration
                    duration_max = duration
                else:
                    maximum_duration = duration_max
                
                # Update the minimum duration
                if line_count == 1:
                    minimum_duration = duration
                    duration_min = duration
                else:
                    if duration < duration_min:
                        minimum_duration = duration
                        duration_min = duration
                    else: 
                        minimum_duration = duration_min
                
                # Update the failure rate
                if failed == 'TRUE':
                    total_tests_failed = total_tests_failed + 1
                else:
                    total_tests_passed = total_tests_passed + 1
                
                # Convert the failure rate to desirable floating point value
                failure_rate = float(total_tests_failed) / float(total_tests_passed + total_tests_failed) * 1000
                int_failure_rate = int(failure_rate)
                failure_rate = float(int_failure_rate)/1000
                line_count += 1

                # Write the table rows
                table_row = [build, test_suite, duration, failed, average_duration, maximum_duration, minimum_duration, failure_rate]
                csv_writer.writerow(table_row)

if __name__ == '__main__':
    main()