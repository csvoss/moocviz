## Takes in the raw Harvardx/MITx data
## Outputs a CSV file counting average number of students for each country by courses

import csv

INPUTFILENAMES = [

'../Overall.csv',
'../split_by_country/Unknown_Other.csv',
'../split_by_country/United_States.csv',
'../split_by_country/United_Kingdom.csv',
'../split_by_country/Ukraine.csv',
'../split_by_country/Spain.csv',
'../split_by_country/Russian_Federation.csv',
'../split_by_country/Portugal.csv',
'../split_by_country/Poland.csv',
'../split_by_country/Philippines.csv',
'../split_by_country/Pakistan.csv',
'../split_by_country/Other_South_Asia.csv',
'../split_by_country/Other_South_America.csv',
'../split_by_country/Other_Oceania.csv',
'../split_by_country/Other_North___Central_Amer.,_Caribbean.csv',
'../split_by_country/Other_Middle_East_Central_Asia.csv',
'../split_by_country/Other_Europe.csv',
'../split_by_country/Other_East_Asia.csv',
'../split_by_country/Other_Africa.csv',
'../split_by_country/Nigeria.csv',
'../split_by_country/Morocco.csv',
'../split_by_country/Mexico.csv',
'../split_by_country/Japan.csv',
'../split_by_country/Indonesia.csv',
'../split_by_country/India.csv',
'../split_by_country/Greece.csv',
'../split_by_country/Germany.csv',
'../split_by_country/France.csv',
'../split_by_country/Egypt.csv',
'../split_by_country/Colombia.csv',
'../split_by_country/China.csv',
'../split_by_country/Canada.csv',
'../split_by_country/Brazil.csv',
'../split_by_country/Bangladesh.csv',
'../split_by_country/Australia.csv'
]

DELIMITER = ','
QUOTECHAR = '"'

OUTPUTFOLDER = 'summed_by_course'

FIELDS = ['viewed', 'explored', 'certified', 'grade', 'nevents', 'ndays_act', 'nplay_video', 'nchapters', 'nforum_posts']
FIELDS_AVG = ['viewed', 'explored', 'certified', 'grade', 'events', 'active days', 'video play', 'chapters', 'forum posts']
#[fi+'_avg' for fi in FIELDS]

COURSE = 'course_id'


for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)

        sums_by_fi_by_c = {} ## dictionary (by country) of dictionaries (by field) of sums
        counts_by_fi_by_c = {} ## dictionary (by country) of dictionaries (by field) of the total count seen so far (for average-computation purposes)

        def is_num(string):
            string = str.strip(string)
            return string != '' and string != 'NA' and len(string)>0 

        for row in csvreader:
            course = row[COURSE]
            if not course in sums_by_fi_by_c:
                sums_by_fi_by_c[course] = dict([(fi,0) for fi in FIELDS])
                counts_by_fi_by_c[course] = dict([(fi,0) for fi in FIELDS])
            sums_by_fi = sums_by_fi_by_c[course]
            counts_by_fi = counts_by_fi_by_c[course]
            for fi in FIELDS:
                num = row[fi]
                if is_num(num):
                    num = float(num)
                    sums_by_fi[fi] += num
                    counts_by_fi[fi] += 1
            #print country, sums_by_fi, counts_by_fi


        ## Prevent divide by zero errors when computing average
        for c in counts_by_fi_by_c:
            counts_by_fi = counts_by_fi_by_c[c]
            for fi in counts_by_fi:
                if counts_by_fi[fi] == 0:
                    counts_by_fi[fi] = 1

        ## Compute average
        averages_by_fi_by_c = dict([ (course, dict([(field, round(sums_by_fi_by_c[course][field] / counts_by_fi_by_c[course][field], 2)) for field in FIELDS])) for course in sums_by_fi_by_c])

        outputfilename = OUTPUTFOLDER + '/' + inputfilename.split('/')[-1]

        with open(outputfilename, 'wb') as csv_out:
            csvwriter = csv.writer(csv_out, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['Course'] + FIELDS_AVG)
            for course in sums_by_fi_by_c:
                sums_by_fi = sums_by_fi_by_c[course]
                averages_by_fi = averages_by_fi_by_c[course]
                csvwriter.writerow([course] + [averages_by_fi[fi] for fi in FIELDS])
