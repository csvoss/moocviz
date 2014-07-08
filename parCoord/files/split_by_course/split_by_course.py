import csv

inputfilename = '../Overall.csv'
delimiter = ','
quotechar = '"'

course_column = "course_id"

def sanitize(filename):
    invalid_chars = '\/:*?"<>|'
    for c in invalid_chars:
        filename = filename.replace(c, '_')
    return filename

with open(inputfilename, 'rb') as csv_in:
    csvreader = csv.DictReader(csv_in, delimiter=delimiter, quotechar=quotechar)
    
    csvwriters = {} ## Dictionary from course ID to csvwriter
    csvfiles = {} ## Solely for the purpose of closing them later
    
    keys = ["course_id","userid_DI","registered","viewed","explored","certified","final_cc_cname_DI","LoE_DI","YoB","gender","grade","start_time_DI","last_event_DI","nevents","ndays_act","nplay_video","nchapters","nforum_posts","roles","incomplete_flag"]
    
    def listify(row):
        return [row[key] for key in keys]
    
    for row in csvreader:
        course = row[course_column]
        if not course in csvwriters: ## Might need to initialize a new writer
            fi = open(sanitize(course+'.csv'), 'wb')
            csvfiles[course] = fi
            csvwriters[course] = csv.writer(fi, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
            csvwriters[course].writerow(keys)
        csvwriters[course].writerow(listify(row))
    
    for writer in csvfiles.values():
        writer.close()
