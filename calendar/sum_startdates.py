## Takes in the raw Harvardx/MITx data
## Outputs a CSV file counting the number of students that started their course on day Date

import csv

inputfilenames = [
    '../HMXPC13_DI_v2_5-14-14.csv',
    '../by_course/HarvardX_CB22x_2013_Spring.csv',
    '../by_course/HarvardX_CS50x_2012.csv',
    '../by_course/HarvardX_ER22x_2013_Spring.csv',
    '../by_course/HarvardX_PH207x_2012_Fall.csv',
    '../by_course/HarvardX_PH278x_2013_Spring.csv',
    '../by_course/MITx_14.73x_2013_Spring.csv',
    '../by_course/MITx_2.01x_2013_Spring.csv',
    '../by_course/MITx_3.091x_2012_Fall.csv',
    '../by_course/MITx_3.091x_2013_Spring.csv',
    '../by_course/MITx_6.002x_2012_Fall.csv',
    '../by_course/MITx_6.002x_2013_Spring.csv',
    '../by_course/MITx_6.00x_2012_Fall.csv',
    '../by_course/MITx_6.00x_2013_Spring.csv',
    '../by_course/MITx_7.00x_2013_Spring.csv',
    '../by_course/MITx_8.02x_2013_Spring.csv',
    '../by_course/MITx_8.MReV_2013_Summer.csv',
]
delimiter = ','
quotechar = '"'

outputfolder = 'summed_startdates'

fields = ['start_time_DI', 'last_event_DI']

for inputfilename in inputfilenames:
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

        outputfilename = outputfolder + '/' + inputfilename.split('/')[-1]

        with open(outputfilename, 'wb') as csv_out:
            csvwriter = csv.writer(csv_out, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['Date'] + fields)
            for date in sums.keys():
                csvwriter.writerow([date] +[sums_by_field[fi][date] for fi in fields])
