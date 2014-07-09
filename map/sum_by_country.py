## Takes in the raw Harvardx/MITx data
## Outputs a CSV file aggregating the data by country, for the MAP visualization

import csv

INPUTFILENAMES = [
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

DELIMITER = ','
QUOTECHAR = '"'

OUTPUTFOLDER = 'summed_by_country'

FIELDS = ['registered', 'viewed', 'explored', 'certified', 'grade', 'nevents', 'ndays_act', 'nplay_video', 'nchapters', 'nforum_posts']
FIELDS_AVG = [fi+'_avg' for fi in FIELDS]

COUNTRY = 'final_cc_cname_DI'

for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)

        sums_by_fi_by_c = {} ## dictionary (by country) of dictionaries (by field) of sums
        counts_by_fi_by_c = {} ## dictionary (by country) of dictionaries (by field) of the total count seen so far (for average-computation purposes)

        def is_num(string):
            string = str.strip(string)
            return string != '' and string != 'NA' and len(string)>0 

        for row in csvreader:
            country = row[COUNTRY]
            if not country in sums_by_fi_by_c:
                sums_by_fi_by_c[country] = dict([(fi,0) for fi in FIELDS])
                counts_by_fi_by_c[country] = dict([(fi,0) for fi in FIELDS])
            sums_by_fi = sums_by_fi_by_c[country]
            counts_by_fi = counts_by_fi_by_c[country]
            for fi in FIELDS:
                num = row[fi]
                if is_num(num):
                    num = float(num)
                    sums_by_fi[fi] += num
                    counts_by_fi[fi] += 1

        ## Prevent divide by zero errors when computing average
        for c in counts_by_fi_by_c:
            counts_by_fi = counts_by_fi_by_c[c]
            for fi in counts_by_fi:
                if counts_by_fi[fi] == 0:
                    counts_by_fi[fi] = 1

        ## Compute average from sums and counts
        averages_by_fi_by_c = dict([ (country, dict([(field, sums_by_fi_by_c[country][field] / counts_by_fi_by_c[country][field]) for field in FIELDS])) for country in sums_by_fi_by_c])

        outputfilename = OUTPUTFOLDER + '/' + inputfilename.split('/')[-1]

        with open(outputfilename, 'wb') as csv_out:
            csvwriter = csv.writer(csv_out, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['Country'] + FIELDS + FIELDS_AVG)
            for country in sums_by_fi_by_c:
                sums_by_fi = sums_by_fi_by_c[country]
                averages_by_fi = averages_by_fi_by_c[country]
                csvwriter.writerow([country] +[sums_by_fi[fi] for fi in FIELDS] + [averages_by_fi[fi] for fi in FIELDS])
