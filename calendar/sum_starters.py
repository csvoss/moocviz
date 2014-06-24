## Takes in the raw Harvardx/MITx data
## Outputs a CSV file counting the number of students that started their course on day Date

import csv

inputfilename = "HMXPC13_DI_v2_5-14-14.csv"
delimiter = ","
quotechar = '|'

outputfilename = "summed_startdates.csv"

with open(inputfilename, 'rb') as csv_in:
    csvreader = csv.DictReader(csv_in, delimiter=delimiter, quotechar=quotechar)

    sums = {}

    def is_date(string):
        return string.count('-')==2

    for row in csvreader:
        date = row["start_time_DI"]
        if is_date(date):
            if date in sums:
                sums[date] += 1
            else:
                sums[date] = 1

    with open(outputfilename, 'wb') as csv_out:
        csvwriter = csv.writer(csv_out, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Date', 'Sum'])
        for date in sums.keys():
            csvwriter.writerow([date, sums[date]])
