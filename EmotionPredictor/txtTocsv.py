import csv

# Open CSV file for writing
with open('emotions.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)

    # Read from the emotion.txt file
    with open('emotion.txt') as fh:
        for line in fh:
            # Split by ; and remove any extra spaces or newline chars
            row = [item.strip() for item in line.strip().split(';')]
            writer.writerow(row)
