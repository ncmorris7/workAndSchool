import os

countDataSet = 6
totalObs = 300

# a list of the methods to iterate through
types = [
    'TimingsLog7Zip',
    'TimingsLogBatch',
    'TimingsLogMfc1',
    'TimingsLogMfc2',
    'TimingsLogPpmz'
         ]

# populate a dictionary with {dataSet : [possible fileNums]} for the purposes of
# categorizing the files that are opened. 
dataSets = {}
for i in range(countDataSet):
    toAppend = []
    for j in range(i, totalObs, countDataSet):
        toAppend.append(str(j))
    dataSets[str(i)] = toAppend

# a dictionary with {method : {dataSet : [observed values]}}; each method has 6
# dataSets, each dataSet has 50 observations. This creates the shell that will
# be populated in the next step...
d = {
    'TimingsLog7Zip':{},
    'TimingsLogBatch':{},
    'TimingsLogMfc1':{},
    'TimingsLogMfc2':{},
    'TimingsLogPpmz':{}
    }

# fill dictionary d with requisite {dataSet: [observed values]} sub-dictionary
for key in d:
    for i in range(countDataSet):
        d[key].update({str(i):[]})

# create a CSV for easier (? hopefully, I guess?) data validation
report = open('00_Timing_Spreadsheet.csv','w')
report.write('Method, FileNum, DataSet, Time (minutes)\n')


def processLogs(compType, fileNum):
    'Opens file "compType_11_fileNum.txt" and populates dictionary d with calculation time'
    # file i/o
    infile = open('{}_11_{}.txt'.format(compType,fileNum))
    content = infile.read()
    infile.close()

    # iterate through each key (0/1/2/3/4/5) of dataSets; if the file number
    # appears in that key:value, append the observed timing to the appropriate
    # sub-dictionary
    for key in dataSets:
        if fileNum in dataSets[key]:
            d[compType][key].append(float(content.split()[5]))
            # write the observation to the CSV 
            report.write("{}, {}, {}, {}\n".format(compType,fileNum,key,content.split()[5]))

# iterate through the methods
for method in types:
    # iterate through 300 observations per method
    for dSet in range(totalObs):
        processLogs(method,str(dSet))

report.close()

# formatted output
print("{:15}".format('Method'),end = '')
for i in range(6):
    print(f'{i:15}',end = '')
print()
for key in d:
    print(f'{key:15}',end = '\t')
    #print(key, '\tAverage Time')
    for subKey in d[key]:
        print(f'{round(sum(d[key][subKey])/len(d[key][subKey]),14):15}', end = '\t')
    print()
