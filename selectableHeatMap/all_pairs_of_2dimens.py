## Takes in the raw Harvardx/MITx data
## Outputs a CSV files for all possible two dimensions
## return : xth cell,yth cell, all corresponding pair of coords, all corresponding averages of other fields 

import csv
import math

#GLOBAL VARS
#defualt size of heatMap table
heatWidth = 450
heatHeight = 400
ROW = 30
COL = 30

################## Linear_x vs Linear_y ###############
#for each field
MAXS = {}      
MINS = {}
numRow ={}
numCol = {}
cellWidth = {}
cellHeight = {}
scaleFuncX = {}
scaleFuncY = {}
linearMapCellX = {}
linearMapCellY = {}


INPUTFILENAMES = [
    'test_HMX.csv'
]

DELIMITER = ','
QUOTECHAR = '"'

OUTPUTFOLDER = "heatMap_files"
fieldX = ["ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
fieldY = ["grade","ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
all_field = list(set(fieldX+fieldY))
all_field_ave = [ fi+"_ave" for fi in all_field]
all_field_ave_overall = [ fi+"_ave_overall" for fi in all_field]
dim_2D = []
for x in fieldX:
    for y in fieldY:
        dim_2D.append( (x,y))
        
for fi in all_field:
    MAXS[fi] = 0
    MINS[fi] = 0

def P(num, field): #parse function
    if field == "grade":
        return num*100
    return num

def is_num(string):
    string = str.strip(string)
    return string != '' and string != 'NA' and len(string)>0

for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for row in csvreader:
            for fi in all_field:
                if is_num(row[fi]):
                    MAXS[fi] = max( MAXS[fi], P(float(row[fi]), fi))
                    MINS[fi] = min( MINS[fi], P(float(row[fi]), fi))

#setting ranges for heat map's x,y dimesions 
#if a field has 20 ranges, we don't need initial ROW = 30;
#type-- grade: 0-1, number of activities: integer
for fi in all_field: 
    if MAXS[fi] < ROW:
        numRow[fi] = int(math.ceil(MAXS[fi]))
        cellHeight[fi] = round( 1.0*heatHeight/numRow[fi], 1)
    else:
        numRow[fi] = ROW
        cellHeight[fi] = round( 1.0*heatHeight/ROW, 1)
    if MAXS[fi] < COL:
        numCol[fi] = int(math.ceil(MAXS[fi]))
        cellWidth[fi] = round( 1.0*heatWidth/numCol[fi], 1)
    else:
        numCol[fi] = COL
        cellWidth[fi] = round( 1.0*heatWidth/COL, 1)



# functions: input number to cell number 
#for fi in all_field:
    #linearMapCellX[fi] = lambda x:  numCol[fi]-1 if x == MAXS[fi] else int(math.floor(x/MAXS[fi]*numCol[fi]))
    #linearMapCellY[fi] = lambda x:  numRow[fi]-1 if x == MAXS[fi] else int(math.floor(x/MAXS[fi]*numRow[fi]))

def linearMapCell(dimMax, field, num):  #numCol[fi]
    if num == MAXS[field]:
        return dimMax[field]-1
    else:
       return  int(math.floor(num/MAXS[field]*dimMax[field]))
        

heatTables = {}      # cell(xth,yth): number of students
heatTableList = {}   # cell(xth,yth)[fi]: list of particular field
heatTableAve ={}     # cell(xth,yth)[fi]: ave of particular field
OverAve = []         # ave of particular field overall /all_field/
OverList = {}      #for purpose to find OverAve
for (x,y) in dim_2D:
    heatTables[x+'-'+y] = {}
    heatTableAve[x+'-'+y] = {}
    heatTableList[x+'-'+y] = {}
    for fi in all_field:
        OverList[fi] = []; 
        heatTableAve[x+'-'+y][fi] = {}   # cell(xth,yth)[field] : ave of that field
        heatTableList[x+'-'+y][fi]  = {} # cell(xth,yth)[field] : list of all numbers of that field/ for computation of heatTableAve

# loading and reading input files
for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for data in csvreader:
            for (x,y) in dim_2D:
                #mathching data (a student) to a cell
                if is_num(data[x]) and is_num(data[y]):
                    colNum = linearMapCell( numCol, x, P(float(data[x]), x))
                    rowNum = linearMapCell( numRow, y, P(float(data[y]), y))
                    #colNum = linearMapCellX[x](float(data[x]) ) #cell num of x coord
                    #rowNum = int(math.floor(float(data[y])/MAXS[y]*numRow[y]))#linearMapCellY[y](float(data[y]) ) #cell num of y coord

                    if 30<rowNum:
                        print "fishy", MAXS[y], rowNum
                    if not (colNum, rowNum) in heatTables[x+'-'+y]:
                        heatTables[x+'-'+y][(colNum, rowNum)] = 1
                    else:
                        heatTables[x+'-'+y][(colNum, rowNum)] +=1
                    #finding list of other attrs of a cell
                    for fi in all_field:
                        heatTableList[x+'-'+y][fi][(colNum, rowNum)] = []
                        if is_num(data[fi]):
                            heatTableList[x+'-'+y][fi][(colNum, rowNum)].append( P(float(data[fi]), fi) )

#finding heatTableAve from heatTableList (each cell's other DIMS' averages)
for (x,y) in dim_2D:
    for coord in heatTables[x+'-'+y]:
        for fi in all_field:
            if len(heatTableList[x+'-'+y][fi][coord]) > 0:
                heatTableAve[x+'-'+y][fi][coord] = 1.0*sum(heatTableList[x+'-'+y][fi][coord])/len(heatTableList[x+'-'+y][fi][coord])
            else:
                heatTableAve[x+'-'+y][fi][coord] = 0
            OverList[fi].append( heatTableAve[x+'-'+y][fi][coord] ) 
            
                
#finding OverAve from OverList (overall other DIMS' averages)
for fi in all_field:
    if len(OverList[fi]) > 0:
        OverAve.append(int( round(1.0*sum(OverList[fi])/len(OverList[fi]), 0) ))           
    else:
        OverAve.append( 0 )
        
#finding peaks of number of students: for color legend:
PEAKS = {}
for (x,y) in dim_2D:
    PEAKS[x+'-'+y] = [0]*6
    for coord in heatTables[x+'-'+y]:
        if heatTables[x+'-'+y][coord] > PEAKS[x+'-'+y][0]:
            PEAKS[x+'-'+y][0] = heatTables[x+'-'+y][coord]
            PEAKS[x+'-'+y].sort()
    PEAKS[x+'-'+y] = list(set( [0]+PEAKS[x+'-'+y]))
    PEAKS[x+'-'+y].sort()


        
#writing outpute file            
for (x,y) in dim_2D:
    # output file about each cell
    outputfilename1 = OUTPUTFOLDER + '/' + "linearScale-" + x + "-linearScale-" + y + ".csv"
    with open(outputfilename1, 'wb') as csv_out1:
        csvwriter1 = csv.writer(csv_out1, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter1.writerow(["colNum"]+ ["rowNum"] + ["totalStudents"] + all_field_ave)
        for coord in heatTables[x+'-'+y]:
            aves = [ heatTableAve[x+'-'+y][fi][coord] for fi in all_field]
            csvwriter1.writerow([coord[0]] + [coord[1]] + [heatTables[x+'-'+y][coord]] + aves)
            
        for i in range(numCol[x]):
            for j in range(numRow[y]):
                if not (i, j) in heatTables[x+'-'+y]:
                    csvwriter1.writerow([i] + [j] + [0] + [0 for fi in all_field] )
                    
                    
                    

    # output file about heatTable
    outputfilename2 = OUTPUTFOLDER + '/' + "table-linearScale-" + x + "-linearScale-" + y + ".csv"
    with open(outputfilename2, 'wb') as csv_out2:
        csvwriter2 = csv.writer(csv_out2, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter2.writerow(["matrixRow"] + ["matrixCol"] + ["cellWidth"] + ["cellHeight"]+ all_field_ave_overall+["maxX", "maxY"]+["peaks"])
        csvwriter2.writerow([numRow[y]] + [numCol[x]] + [cellWidth[x]] + [cellHeight[y]] + OverAve + [MAXS[x], MAXS[y]] + [tuple(PEAKS[x+'-'+y])])




    
############### Logarithmic_x vs Logarithmic_y  ###################


#for each field
MAXS = {}      
MINS = {}
numRow ={}
numCol = {}
cellWidth = {}
cellHeight = {}
scaleFuncX = {}
scaleFuncY = {}
logMapCellX = {}
logMapCellY = {}


INPUTFILENAMES = [
    'test_HMX.csv'
]

DELIMITER = ','
QUOTECHAR = '"'

OUTPUTFOLDER = "heatMap_files"
fieldX = ["ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
fieldY = ["grade","ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
all_field = list(set(fieldX+fieldY))
all_field_ave = [ fi+"_ave" for fi in all_field]
all_field_ave_overall = [ fi+"_ave_overall" for fi in all_field]
dim_2D = []
for x in fieldX:
    for y in fieldY:
        dim_2D.append( (x,y))
        
for fi in all_field:
    MAXS[fi] = 0
    MINS[fi] = 0

def P(num, field): #parse function
    if field == "grade":
        return num*100
    return num

    
def is_num(string):
    string = str.strip(string)
    return string != '' and string != 'NA' and len(string)>0

for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for row in csvreader:
            for fi in all_field:
                if is_num(row[fi]):
                    MAXS[fi] = max( MAXS[fi], P(float(row[fi]), fi))
                    MINS[fi] = min( MINS[fi], P(float(row[fi]), fi))

#setting ranges for heat map's x,y dimesions 
#if a field has 20 ranges, we don't need initial ROW = 30;
#type-- grade: 0-1, number of activities: integer
for fi in all_field: 
    if MAXS[fi] < ROW:
        numRow[fi] = int(math.ceil(MAXS[fi]))
        cellHeight[fi] = round( 1.0*heatHeight/numRow[fi], 1)
    else:
        numRow[fi] = ROW
        cellHeight[fi] = round( 1.0*heatHeight/ROW, 1)
    if MAXS[fi] < COL:
        numCol[fi] = int(math.ceil(MAXS[fi]))
        cellWidth[fi] = round( 1.0*heatWidth/numCol[fi], 1)
    else:
        numCol[fi] = COL
        cellWidth[fi] = round( 1.0*heatWidth/COL, 1)



# functions: input number to cell number 

def logMapCell(dimMax, field, num):
    if num == MAXS[field]:
        return dimMax[field]-1
    return int(math.floor(math.log(num, MAXS[field])*dimMax[fi]))
    
def linearMapCell(dimMax, field, num):  #dimMax ->numRow, numCol
    if num == MAXS[field]:
        return dimMax[field]-1
    else:
       return  int(math.floor(num/MAXS[field]*dimMax[field]))

   

heatTables = {}      # cell(xth,yth): number of students
heatTableList = {}   # cell(xth,yth)[fi]: list of particular field
heatTableAve ={}     # cell(xth,yth)[fi]: ave of particular field
OverAve = []         # ave of particular field overall /all_field/
OverList = {}      #for purpose to find OverAve
for (x,y) in dim_2D:
    heatTables[x+'-'+y] = {}
    heatTableAve[x+'-'+y] = {}
    heatTableList[x+'-'+y] = {}
    for fi in all_field:
        OverList[fi] = []; 
        heatTableAve[x+'-'+y][fi] = {}   # cell(xth,yth)[field] : ave of that field
        heatTableList[x+'-'+y][fi]  = {} # cell(xth,yth)[field] : list of all numbers of that field/ for computation of heatTableAve

# loading and reading input files
for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for data in csvreader:
            for (x,y) in dim_2D:
                #mathching data (a student) to a cell
                if is_num(data[x]) and is_num(data[y]) and float(data[x]) != 0 and float(data[y]) !=0: #log scale doesn't account 0
                    colNum = logMapCell(numCol, x, P(float(data[x]), x )) #cell num of x coord
                    rowNum = logMapCell(numRow, y, P(float(data[y]), y )) #cell num of y coord
                    if not (colNum, rowNum) in heatTables[x+'-'+y]:
                        heatTables[x+'-'+y][(colNum, rowNum)] = 1
                    else:
                        heatTables[x+'-'+y][(colNum, rowNum)] +=1
                    #finding list of other attrs of a cell
                    for fi in all_field:
                        heatTableList[x+'-'+y][fi][(colNum, rowNum)] = []
                        if is_num(data[fi]):
                            heatTableList[x+'-'+y][fi][(colNum, rowNum)].append( P(float(data[fi]), fi) )

#finding heatTableAve from heatTableList (each cell's other DIMS' averages)
for (x,y) in dim_2D:
    for coord in heatTables[x+'-'+y]:
        for fi in all_field:
            if len(heatTableList[x+'-'+y][fi][coord]) > 0:
                heatTableAve[x+'-'+y][fi][coord] = 1.0*sum(heatTableList[x+'-'+y][fi][coord])/len(heatTableList[x+'-'+y][fi][coord])
            else:
                heatTableAve[x+'-'+y][fi][coord] = 0
            OverList[fi].append( heatTableAve[x+'-'+y][fi][coord] ) 
            
                
#finding OverAve from OverList (overall other DIMS' averages)
for fi in all_field:
    if len(OverList[fi]) > 0:
        OverAve.append(int( round(1.0*sum(OverList[fi])/len(OverList[fi]), 0) ))           
    else:
        OverAve.append( 0 )
        
#finding peaks of number of students: for color legend:
PEAKS = {}
for (x,y) in dim_2D:
    PEAKS[x+'-'+y] = [0]*6
    for coord in heatTables[x+'-'+y]:
        if heatTables[x+'-'+y][coord] > PEAKS[x+'-'+y][0]:
            PEAKS[x+'-'+y][0] = heatTables[x+'-'+y][coord]
            PEAKS[x+'-'+y].sort()
    PEAKS[x+'-'+y] = list(set( [0]+PEAKS[x+'-'+y]))
    PEAKS[x+'-'+y].sort()


        
#writing outpute file            
for (x,y) in dim_2D:
    # output file about each cell
    outputfilename1 = OUTPUTFOLDER + '/' + "logScale-" + x + "-logScale-" + y + ".csv"
    with open(outputfilename1, 'wb') as csv_out1:
        csvwriter1 = csv.writer(csv_out1, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter1.writerow(["colNum"]+ ["rowNum"] + ["totalStudents"] + all_field_ave)
        for coord in heatTables[x+'-'+y]:
            aves = [ heatTableAve[x+'-'+y][fi][coord] for fi in all_field]
            csvwriter1.writerow([coord[0]] + [coord[1]] + [heatTables[x+'-'+y][coord]] + aves)
            
        for i in range(numCol[x]):
            for j in range(numRow[y]):
                if not (i, j) in heatTables[x+'-'+y]:
                    csvwriter1.writerow([i] + [j] + [0] + [0 for fi in all_field] )
                    
                    
                    

    # output file about heatTable
    outputfilename2 = OUTPUTFOLDER + '/' + "table-logScale-" + x + "-logScale-" + y + ".csv"
    with open(outputfilename2, 'wb') as csv_out2:
        csvwriter2 = csv.writer(csv_out2, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter2.writerow(["matrixRow"] + ["matrixCol"] + ["cellWidth"] + ["cellHeight"]+ all_field_ave_overall+["maxX", "maxY"]+["peaks"])
        csvwriter2.writerow([numRow[y]] + [numCol[x]] + [cellWidth[x]] + [cellHeight[y]] + OverAve + [MAXS[x], MAXS[y]] + [tuple(PEAKS[x+'-'+y])])


    
            

############## Logarithmic_x vs Linear_y ##############3

#for each field
MAXS = {}      
MINS = {}
numRow ={}
numCol = {}
cellWidth = {}
cellHeight = {}
scaleFuncX = {}
scaleFuncY = {}
MapCellX = {}
MapCellY = {}


INPUTFILENAMES = [
    'test_HMX.csv'
]

DELIMITER = ','
QUOTECHAR = '"'

OUTPUTFOLDER = "heatMap_files"
fieldX = ["ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
fieldY = ["grade","ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
all_field = list(set(fieldX+fieldY))
all_field_ave = [ fi+"_ave" for fi in all_field]
all_field_ave_overall = [ fi+"_ave_overall" for fi in all_field]
dim_2D = []
for x in fieldX:
    for y in fieldY:
        dim_2D.append( (x,y))

def P(num, field): #parse function
    if field == "grade":
        return num*100
    return num
       
for fi in all_field:
    MAXS[fi] = 0
    MINS[fi] = 0
    
def is_num(string):
    string = str.strip(string)
    return string != '' and string != 'NA' and len(string)>0

for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for row in csvreader:
            for fi in all_field:
                if is_num(row[fi]):
                    MAXS[fi] = max( MAXS[fi], P(float(row[fi]), fi))
                    MINS[fi] = min( MINS[fi], P(float(row[fi]), fi))

#setting ranges for heat map's x,y dimesions 
#if a field has 20 ranges, we don't need initial ROW = 30;
#type-- grade: 0-1, number of activities: integer
for fi in all_field: 
    if MAXS[fi] < ROW:
        numRow[fi] = int(math.ceil(MAXS[fi]))
        cellHeight[fi] = round( 1.0*heatHeight/numRow[fi], 1)
    else:
        numRow[fi] = ROW
        cellHeight[fi] = round( 1.0*heatHeight/ROW, 1)
    if MAXS[fi] < COL:
        numCol[fi] = int(math.ceil(MAXS[fi]))
        cellWidth[fi] = round( 1.0*heatWidth/numCol[fi], 1)
    else:
        numCol[fi] = COL
        cellWidth[fi] = round( 1.0*heatWidth/COL, 1)

# functions: input number to cell number 
def logMapCell(dimMax, field, num):
    if num == MAXS[field]:
        return dimMax[field]-1
    return int(math.floor(math.log(num, MAXS[field])*dimMax[fi]))
    
def linearMapCell(dimMax, field, num):  #dimMax ->numRow, numCol
    if num == MAXS[field]:
        return dimMax[field]-1
    else:
       return  int(math.floor(num/MAXS[field]*dimMax[field]))

heatTables = {}      # cell(xth,yth): number of students
heatTableList = {}   # cell(xth,yth)[fi]: list of particular field
heatTableAve ={}     # cell(xth,yth)[fi]: ave of particular field
OverAve = []         # ave of particular field overall /all_field/
OverList = {}      #for purpose to find OverAve
for (x,y) in dim_2D:
    heatTables[x+'-'+y] = {}
    heatTableAve[x+'-'+y] = {}
    heatTableList[x+'-'+y] = {}
    for fi in all_field:
        OverList[fi] = []; 
        heatTableAve[x+'-'+y][fi] = {}   # cell(xth,yth)[field] : ave of that field
        heatTableList[x+'-'+y][fi]  = {} # cell(xth,yth)[field] : list of all numbers of that field/ for computation of heatTableAve

# loading and reading input files
for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for data in csvreader:
            for (x,y) in dim_2D:
                #mathching data (a student) to a cell
                if is_num(data[x]) and is_num(data[y]) and float(data[x]) !=0 : #log scale x doesn't account 0
                    colNum = logMapCell(numCol, x, P(float(data[x]), x) ) #cell num of x coord
                    rowNum = linearMapCell(numRow, y, P(float(data[y]), y) ) #cell num of y coord
                    if not (colNum, rowNum) in heatTables[x+'-'+y]:
                        heatTables[x+'-'+y][(colNum, rowNum)] = 1
                    else:
                        heatTables[x+'-'+y][(colNum, rowNum)] +=1
                    #finding list of other attrs of a cell
                    for fi in all_field:
                        heatTableList[x+'-'+y][fi][(colNum, rowNum)] = []
                        if is_num(data[fi]):
                            heatTableList[x+'-'+y][fi][(colNum, rowNum)].append( P(float(data[fi]), fi) )

#finding heatTableAve from heatTableList (each cell's other DIMS' averages)
for (x,y) in dim_2D:
    for coord in heatTables[x+'-'+y]:
        for fi in all_field:
            if len(heatTableList[x+'-'+y][fi][coord]) > 0:
                heatTableAve[x+'-'+y][fi][coord] = 1.0*sum(heatTableList[x+'-'+y][fi][coord])/len(heatTableList[x+'-'+y][fi][coord])
            else:
                heatTableAve[x+'-'+y][fi][coord] = 0
            OverList[fi].append( heatTableAve[x+'-'+y][fi][coord] ) 
            
                
#finding OverAve from OverList (overall other DIMS' averages)
for fi in all_field:
    if len(OverList[fi]) > 0:
        OverAve.append(int( round(1.0*sum(OverList[fi])/len(OverList[fi]), 0) ))           
    else:
        OverAve.append( 0 )
        
#finding peaks of number of students: for color legend:
PEAKS = {}
for (x,y) in dim_2D:
    PEAKS[x+'-'+y] = [0]*6
    for coord in heatTables[x+'-'+y]:
        if heatTables[x+'-'+y][coord] > PEAKS[x+'-'+y][0]:
            PEAKS[x+'-'+y][0] = heatTables[x+'-'+y][coord]
            PEAKS[x+'-'+y].sort()
    PEAKS[x+'-'+y] = list(set( [0]+PEAKS[x+'-'+y]))
    PEAKS[x+'-'+y].sort()


        
#writing outpute file            
for (x,y) in dim_2D:
    # output file about each cell
    outputfilename1 = OUTPUTFOLDER + '/' + "logScale-" + x + "-linearScale-" + y + ".csv"
    with open(outputfilename1, 'wb') as csv_out1:
        csvwriter1 = csv.writer(csv_out1, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter1.writerow(["colNum"]+ ["rowNum"] + ["totalStudents"] + all_field_ave)
        for coord in heatTables[x+'-'+y]:
            aves = [ heatTableAve[x+'-'+y][fi][coord] for fi in all_field]
            csvwriter1.writerow([coord[0]] + [coord[1]] + [heatTables[x+'-'+y][coord]] + aves)
            
        for i in range(numCol[x]):
            for j in range(numRow[y]):
                if not (i, j) in heatTables[x+'-'+y]:
                    csvwriter1.writerow([i] + [j] + [0] + [0 for fi in all_field] )
                    
                    
                    

    # output file about heatTable
    outputfilename2 = OUTPUTFOLDER + '/' + "table-logScale-" + x + "-linearScale-" + y + ".csv"
    with open(outputfilename2, 'wb') as csv_out2:
        csvwriter2 = csv.writer(csv_out2, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter2.writerow(["matrixRow"] + ["matrixCol"] + ["cellWidth"] + ["cellHeight"]+ all_field_ave_overall+["maxX", "maxY"]+["peaks"])
        csvwriter2.writerow([numRow[y]] + [numCol[x]] + [cellWidth[x]] + [cellHeight[y]] + OverAve + [MAXS[x], MAXS[y]] + [tuple(PEAKS[x+'-'+y])])


    
            

############### Linear_x vs Logarithmic_y ##############

#for each field
MAXS = {}      
MINS = {}
numRow ={}
numCol = {}
cellWidth = {}
cellHeight = {}
scaleFuncX = {}
scaleFuncY = {}
MapCellX = {}
MapCellY = {}


INPUTFILENAMES = [
    'test_HMX.csv'
]

DELIMITER = ','
QUOTECHAR = '"'

OUTPUTFOLDER = "heatMap_files"
fieldX = ["ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
fieldY = ["grade","ndays_act","nevents","nplay_video","nchapters","nforum_posts"]
all_field = list(set(fieldX+fieldY))
all_field_ave = [ fi+"_ave" for fi in all_field]
all_field_ave_overall = [ fi+"_ave_overall" for fi in all_field]
dim_2D = []
for x in fieldX:
    for y in fieldY:
        dim_2D.append( (x,y))
        
for fi in all_field:
    MAXS[fi] = 0
    MINS[fi] = 0
    
def is_num(string):
    string = str.strip(string)
    return string != '' and string != 'NA' and len(string)>0


def P(num, field): #parse function
    if field == "grade":
        return num*100
    return num

for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for row in csvreader:
            for fi in all_field:
                if is_num(row[fi]):
                    MAXS[fi] = max( MAXS[fi], P(float(row[fi]), fi))
                    MINS[fi] = min( MINS[fi], P(float(row[fi]), fi))

#setting ranges for heat map's x,y dimesions 
#if a field has 20 ranges, we don't need initial ROW = 30;
#type-- grade: 0-1, number of activities: integer
for fi in all_field: 
    if MAXS[fi] < ROW:
        numRow[fi] = int(math.ceil(MAXS[fi]))
        cellHeight[fi] = round( 1.0*heatHeight/numRow[fi], 1)
    else:
        numRow[fi] = ROW
        cellHeight[fi] = round( 1.0*heatHeight/ROW, 1)
    if MAXS[fi] < COL:
        numCol[fi] = int(math.ceil(MAXS[fi]))
        cellWidth[fi] = round( 1.0*heatWidth/numCol[fi], 1)
    else:
        numCol[fi] = COL
        cellWidth[fi] = round( 1.0*heatWidth/COL, 1)


# functions: input number to cell number

def logMapCell(dimMax, field, num):
    if num == MAXS[field]:
        return dimMax[field]-1
    return int(math.floor(math.log(num, MAXS[field])*dimMax[fi]))
    
def linearMapCell(dimMax, field, num):  #dimMax ->numRow, numCol
    if num == MAXS[field]:
        return dimMax[field]-1
    else:
       return  int(math.floor(num/MAXS[field]*dimMax[field]))   

heatTables = {}      # cell(xth,yth): number of students
heatTableList = {}   # cell(xth,yth)[fi]: list of particular field
heatTableAve ={}     # cell(xth,yth)[fi]: ave of particular field
OverAve = []         # ave of particular field overall /all_field/
OverList = {}      #for purpose to find OverAve
for (x,y) in dim_2D:
    heatTables[x+'-'+y] = {}
    heatTableAve[x+'-'+y] = {}
    heatTableList[x+'-'+y] = {}
    for fi in all_field:
        OverList[fi] = []; 
        heatTableAve[x+'-'+y][fi] = {}   # cell(xth,yth)[field] : ave of that field
        heatTableList[x+'-'+y][fi]  = {} # cell(xth,yth)[field] : list of all numbers of that field/ for computation of heatTableAve

# loading and reading input files
for inputfilename in INPUTFILENAMES:
    with open(inputfilename, 'rb') as csv_in:
        csvreader = csv.DictReader(csv_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for data in csvreader:
            for (x,y) in dim_2D:
                #mathching data (a student) to a cell
                if is_num(data[x]) and is_num(data[y]) and float(data[y]) != 0: #log scale y doesn't account 0
                    colNum = linearMapCell(numCol, x, P(float(data[x]), x) ) #cell num of x coord
                    rowNum = logMapCell(numRow, y, P(float(data[y]), y) ) #cell num of y coord
                    if not (colNum, rowNum) in heatTables[x+'-'+y]:
                        heatTables[x+'-'+y][(colNum, rowNum)] = 1
                    else:
                        heatTables[x+'-'+y][(colNum, rowNum)] +=1
                    #finding list of other attrs of a cell
                    for fi in all_field:
                        heatTableList[x+'-'+y][fi][(colNum, rowNum)] = []
                        if is_num(data[fi]):
                            heatTableList[x+'-'+y][fi][(colNum, rowNum)].append( P(float(data[fi]), fi) )

#finding heatTableAve from heatTableList (each cell's other DIMS' averages)
for (x,y) in dim_2D:
    for coord in heatTables[x+'-'+y]:
        for fi in all_field:
            if len(heatTableList[x+'-'+y][fi][coord]) > 0:
                heatTableAve[x+'-'+y][fi][coord] = 1.0*sum(heatTableList[x+'-'+y][fi][coord])/len(heatTableList[x+'-'+y][fi][coord])
            else:
                heatTableAve[x+'-'+y][fi][coord] = 0
            OverList[fi].append( heatTableAve[x+'-'+y][fi][coord] ) 
            
                
#finding OverAve from OverList (overall other DIMS' averages)
for fi in all_field:
    if len(OverList[fi]) > 0:
        OverAve.append(int( round(1.0*sum(OverList[fi])/len(OverList[fi]), 0) ))           
    else:
        OverAve.append( 0 )
        
#finding peaks of number of students: for color legend:
PEAKS = {}
for (x,y) in dim_2D:
    PEAKS[x+'-'+y] = [0]*6
    for coord in heatTables[x+'-'+y]:
        if heatTables[x+'-'+y][coord] > PEAKS[x+'-'+y][0]:
            PEAKS[x+'-'+y][0] = heatTables[x+'-'+y][coord]
            PEAKS[x+'-'+y].sort()
    PEAKS[x+'-'+y] = list(set( [0]+PEAKS[x+'-'+y]))
    PEAKS[x+'-'+y].sort()


        
#writing outpute file            
for (x,y) in dim_2D:
    # output file about each cell
    outputfilename1 = OUTPUTFOLDER + '/' + "linearScale-" + x + "-logScale-" + y + ".csv"
    with open(outputfilename1, 'wb') as csv_out1:
        csvwriter1 = csv.writer(csv_out1, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter1.writerow(["colNum"]+ ["rowNum"] + ["totalStudents"] + all_field_ave)
        for coord in heatTables[x+'-'+y]:
            aves = [ heatTableAve[x+'-'+y][fi][coord] for fi in all_field]
            csvwriter1.writerow([coord[0]] + [coord[1]] + [heatTables[x+'-'+y][coord]] + aves)
            
        for i in range(numCol[x]):
            for j in range(numRow[y]):
                if not (i, j) in heatTables[x+'-'+y]:
                    csvwriter1.writerow([i] + [j] + [0] + [0 for fi in all_field] )
                    
                    
                    

    # output file about heatTable
    outputfilename2 = OUTPUTFOLDER + '/' + "table-linearScale-" + x + "-logScale-" + y + ".csv"
    with open(outputfilename2, 'wb') as csv_out2:
        csvwriter2 = csv.writer(csv_out2, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        csvwriter2.writerow(["matrixRow"] + ["matrixCol"] + ["cellWidth"] + ["cellHeight"]+ all_field_ave_overall+["maxX", "maxY"]+["peaks"])
        csvwriter2.writerow([numRow[y]] + [numCol[x]] + [cellWidth[x]] + [cellHeight[y]] + OverAve + [MAXS[x], MAXS[y]] + [tuple(PEAKS[x+'-'+y])])


    
            

            

                         


     
    

                         


     
    



                         


     
    




            

                         


     
    

