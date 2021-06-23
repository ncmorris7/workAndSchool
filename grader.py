def testEquality(student, answer, qNum):
    'tests equality of inputs, documents result, updates question number'
    if student == answer:
        qNum += 1
        finalReport.write('Y,')
        result = 'Correct!'
    else:
        finalReport.write('N,')
        result = 'Incorrect.'
    outfile.write('Your Answer:\n{}\nLab Answer:\n{}\nResult: {}\n\n'.format(student, answer,result))
    return qNum

#Update values that change week to week:
prof = 'Settle'
labNum = 9

q1name = 'countDenseDir'
q2name = 'AltPrinter'

toTest = 5

testLists = ['http://facweb.cdm.depaul.edu/asettle/web/thekids.html','http://facweb.cdm.depaul.edu/asettle/web/cookie.html', 'http://facweb.cdm.depaul.edu/asettle/web/catscatscats.html', 'http://facweb.cdm.depaul.edu/asettle/web/test1.html']

import answers, glob, os, sys
files = []
for filename in glob.glob('*.py'):
    if filename == 'grader.py' or filename == 'answers.py':
        continue
    forOpen = filename.replace('.py','')
    files.append(forOpen)

totalFiles = 0
totalCorrectQ1 = 0
totalCorrectQ2 = 0

finalReport = open('{}_Lab{}_report.csv'.format(prof,labNum),'w')

finalReport.write("StudentName,")

for j in range(toTest*2):
    finalReport.write('Q1-test: {},'.format(j+1))

for i in range(len(testLists)):
    finalReport.write("Q2-test: {},".format(i+1))
    

finalReport.write('\n')
for i in range(len(files)):
    totalFiles += 1
    try:
        for module in [__import__(files[i])]:
            
            filename = files[i] + '.txt'
            outfile = open(filename, 'w')
            allVals = files[i].split(" - ")
            name = allVals[1]

            finalReport.write("{},".format(name))
            print("Testing {}".format(name))
            
            firstQ = 0
            possibleFirstQ = 0
            secondQ = 0
            possibleSecondQ = 0
            docStrings = 0
            
            outfile.write("\n################\n\n#Report for: {}\n\n".format(name))

            #First Question
            try:
                if (module.countDenseDir.__doc__ is not None):
                    docStrings+=1
                outfile.write("Test case: {}():\n".format(q1name))
               
                try:
                    for i in range(toTest):

                        outfile.write(f"countDenseDir('dirEx',{i}):\n")

                        stuRes = module.countDenseDir('dirEx',i)
                        ansRes = answers.countDenseDir('dirEx',i)

                        firstQ = testEquality(stuRes, ansRes, firstQ)

                        outfile.write(f"countDenseDir('morrisExample',{i}):\n")

                        stuRes = module.countDenseDir('morrisExample',i)
                        ansRes = answers.countDenseDir('morrisExample',i)

                        firstQ = testEquality(stuRes, ansRes, firstQ)
                        
                except Exception as e:
                    outfile.write("Exception: {}\n".format(e))
                    finalReport.write("ERR,")
                
                outfile.write("{}: {}/{} passed\n\n".format(q1name,firstQ,toTest * 2))
                if firstQ == toTest * 2:
                    totalCorrectQ1 += 1
             
            except Exception as e:
                outfile.write("Exception running {}: {}\n".format(q1name,e))
            outfile.write('\n\n')

            try:
                if (module.AltPrinter.__doc__ is not None):
                    docStrings+=1
                outfile.write("Test case: {}():\n".format(q2name))

                #secondQ
                try:
                    for lst in testLists:
                        outfile.write(f"testAParser({lst}):\n")
                        original_stdout = sys.stdout # Save a reference to the original standard output

                        try:
                            with open('studentFile.txt', 'w') as f:
                                sys.stdout = f # Change the standard output to the file we created.
                                module.testAParser(lst)
                                sys.stdout = original_stdout
                            with open('answerFile.txt','w') as g:
                                sys.stdout = g
                                answers.testAParser(lst)
                                sys.stdout = original_stdout

                            stuFile = open('studentFile.txt')
                            stuContent = stuFile.read()
                            stuFile.close()

                            ansFile = open('answerFile.txt')
                            ansContent = ansFile.read()
                            ansFile.close()

                            secondQ = testEquality(stuContent,ansContent,secondQ)
                            
                        except:
                            outfile.write('error in executing call\n')
                            sys.stdout = original_stdout
                  
                except Exception as e:
                    outfile.write("Exception: {}\n".format(e))
                    finalReport.write("ERR,")
                    
                outfile.write("{}: {}/{}".format(q2name,secondQ,len(testLists)))
                if secondQ == len(testLists):
                    totalCorrectQ2 += 1

            except Exception as e:
                outfile.write("Exception running {}: {}\n".format(q2name,e))
            outfile.write('\n\n')

            if docStrings != 2:
                outfile.write("\nPlease remember to include docstrings.")
            outfile.close()
            finalReport.write('\n')
            
                
    except Exception as e:
        print('\n*** *** *** *** *** Compiler Error: {}: {}'.format(files[i],e))
        finalReport.write('compiler error: {}: {}'.format(files[i],e))
        finalReport.write('\n')
    sys.stdout = original_stdout
    print()
finalReport.close()
print("Evaluation Complete")
print("{} correct: {}/{}".format(q1name, totalCorrectQ1, totalFiles))
print("{} correct: {}/{}".format(q2name, totalCorrectQ2, totalFiles))
print("Total files: {}".format(totalFiles))



