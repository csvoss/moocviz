## Takes in the raw Harvardx/MITx data
## Outputs a CSV file counting the number of students that started their course on day Date

import csv

inputfilename = '../HMXPC13_DI_v2_5-14-14.csv'
delimiter = ','
quotechar = '|'

fields = ['start_time_DI', 'last_event_DI']

outputfilename = 'summed_startdates.csv'

with open(inputfilename, 'rb') as csv_in:
    csvreader = csv.DictReader(csv_in, delimiter=delimiter, quotechar=quotechar)

    sums_by_field = dict([(fi, {}) for fi in fields]) ## dictionary (by field) of dictionaries (by date)

    def is_date(string):
        return string.count('-')==2

    for row in csvreader:
        for fi in fields:
            date = row[fi]
            if is_date(date):
                sums = sums_by_field[fi]
                if not date in sums:
                    for fi in fields:
                        sums_by_field[fi][date] = 0
                sums[date] += 1

    with open(outputfilename, 'wb') as csv_out:
        csvwriter = csv.writer(csv_out, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Date'] + fields)
        for date in sums.keys():
            csvwriter.writerow([date] +[sums_by_field[fi][date] for fi in fields])

raw_input()