import answers, glob, os, sys

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

# Update values that change week to week:
prof = 'Walker'
labNum = 3

q1name = 'convert'
q2name = 'mailing_labels'
q3name = 'count_words'

list1 = [5,10.5,15,-20,'6','11.25','16.6','-21']
list2 = [['roger','DODGER','442 Mockingbird Lane','ShreVEPort','WA',33241],
         ['ELAINE','allegra','1525 Schubert Way','tarMAC','Il',61134],
         ['Rowan','Turnbuckle','1 School Road','Toledo','OH',34255],
         ['all','lower','123 Case Place','shortsville','tn',83621],
         ['MALL','CAPS','586 Shoutson Circle','YELLING','MT',90210]]
list3 = [['one opulent orchestra obscures orange oaks',5],
         ['this',1],
         ['this',5],
         ['this answer should be five',0],
         ['always ask an amiable alderman',10]]
         

# for all python files in the folder, append the file names to a list
files = []
for filename in glob.glob('*.py'):
    if filename == 'grader.py' or filename == 'answers.py':
        continue
    forOpen = filename.replace('.py','')
    files.append(forOpen)

# variables to sum results across students
totalFiles = 0
totalCorrectQ1 = 0
totalCorrectQ2 = 0
totalCorrectQ3 = 0

# prepare spreadsheet, one column for each test to be run (will contain Y if test passed or N if not)
finalReport = open('{}_Lab{}_report.csv'.format(prof,labNum),'w')

finalReport.write("StudentName,")

for j in range(len(list1)):
    finalReport.write('{}-test: {},'.format(q1name, j+1))

for k in range(len(list2)):
    finalReport.write('{}-test: {},'.format(q2name, k+1))

for l in range(len(list3)):
    finalReport.write('{}-test: {},'.format(q3name, l+1))

finalReport.write('Total Correct,')
finalReport.write('Total Possible,')
finalReport.write('% correct,')

finalReport.write('\n')

# iterate through the filenames. Import the functions of each opened file into a module (called module)
for i in range(len(files)):
    totalFiles += 1
    try:
        for module in [__import__(files[i])]:

            # create a text file to hold the output of student methods and provide feedback. D2L allows users to
            # attach files in bulk if the name of the file matches the pattern/name of the student. This naming
            # convention ensures that compatibility. 
            filename = files[i] + '.txt'
            outfile = open(filename, 'w')
            allVals = files[i].split(" - ")
            name = allVals[1]

            # prepare student code for inclusion in their feedback file
            studentCode = open("{}.py".format(files[i]))
            studentLines = studentCode.readlines()
            studentCode.close()

            # in the CSV report, add the students name; output to the shell a message alerting user to which students'
            # code is being tested.
            finalReport.write("{},".format(name))
            print("Testing {}".format(name))

            # variables to sum results for each student
            firstQ = 0
            secondQ = 0
            thirdQ = 0
            allQs = [firstQ, secondQ, thirdQ]
            
            # hardcoded variables when you can't use len(list1), etc            
            possibleSecondQ = 0
            possibleFirstQ = 0
            possibleThirdQ = 0
            
            # test the number of docstrings present in the student functions
            docStrings = 0
            
            outfile.write("\n################\n\n#Report for: {}\n\n".format(name))
            outfile.write("Please note that the sample outputs included below are for your reference and are not the basis of your grade.\n\n")
            outfile.write("Your code:\n\n")
            for i in range(len(studentLines)):
                outfile.write("{:2}  {}".format(i+1, studentLines[i]))

            outfile.write("\n\nResults:\n\n")            

            # first question
            # test if the function has docstrings
            # for each value in our test list, execute the students' function and the reference function
            # compare them, record their results, update spreadsheet and feedback file
            try:
                if (eval(f"module.{q1name}").__doc__ is not None):
                    docStrings+=1
                outfile.write("Test case: {}():\n".format(q1name))

               # haven't figured out a clever way to modularize "n"
                try:
                    for n in list1:                        
                        try:
                            stuContent = eval(f"module.{q1name}")(n)
                            ansContent = eval(f"answers.{q1name}")(n)

                            outfile.write(f'{q1name}({n}):\n')

                            firstQ = testEquality(stuContent, ansContent, firstQ)
                        except:
                            outfile.write('error in executing call\n')
                            print('failure in function call')
                            finalReport.write("ERR,")
                            
                        
                except Exception as e:
                    outfile.write("Exception: {}\n".format(e))
                    finalReport.write("ERR,")
                
                outfile.write("{}: {}/{} passed\n\n".format(q1name,firstQ,len(list1)))

                if firstQ == len(list1):
                    totalCorrectQ1 += 1

            except Exception as e:
                outfile.write("Exception running {}: {}\n".format(q1name,e))
                for i in range(len(list1)):
                    finalReport.write("ERR,")
            outfile.write('\n\n')

            # second Question
            try:
                if (eval(f"module.{q2name}").__doc__ is not None):
                    docStrings+=1
                outfile.write("Test case: {}():\n".format(q2name))
               
                try:
                    for sublist in list2:

                        # for a function that prints, rather than returns; redirect standard out to
                        # a file (one for students, one for the reference). Execute the function and reset
                        # standard out. Then, open each file, read the contents into a string, and test if
                        # the strings are equal.
                        # compare, record results, update spreadsheet.
                        original_stdout = sys.stdout # Save a reference to the original standard output
                        try:
                            with open('studentFile.txt', 'w') as f:
                                sys.stdout = f # Change the standard output to the file we created.
                                eval(f"module.{q2name}")(sublist[0],sublist[1],sublist[2],sublist[3],sublist[4],sublist[5])
                                sys.stdout = original_stdout # reset standard out.
                            with open('answerFile.txt','w') as g:
                                sys.stdout = g
                                eval(f"answers.{q2name}")(sublist[0],sublist[1],sublist[2],sublist[3],sublist[4],sublist[5])
                                sys.stdout = original_stdout

                            stuFile = open('studentFile.txt')
                            stuContent = stuFile.read()
                            stuFile.close()

                            ansFile = open('answerFile.txt')
                            ansContent = ansFile.read()
                            ansFile.close()


                            outfile.write(f'{q2name}({sublist[0],sublist[1],sublist[2],sublist[3],sublist[4],sublist[5]}):\n')

                            secondQ = testEquality(stuContent, ansContent, secondQ)

                        except:
                            outfile.write('error in executing call\n')                            
                            sys.stdout = original_stdout
                            print('failure in function call?')
                            finalReport.write("ERR,")
                            
                except Exception as e:
                    outfile.write("Exception: {}\n".format(e))
                    finalReport.write("ERR,")
                
                outfile.write("{}: {}/{} passed\n\n".format(q2name,secondQ,len(list2)))

                if secondQ == len(list2):
                    totalCorrectQ2 += 1
             
            except Exception as e:
                outfile.write("Exception running {}: {}\n".format(q2name,e))
                for i in range(len(list2)):
                    finalReport.write("ERR,")
            outfile.write('\n\n')

            # third question
            try:
                if (eval(f"module.{q3name}").__doc__ is not None):
                    docStrings+=1
                outfile.write("Test case: {}():\n".format(q3name))
               
                try:
                    for sublist in list3:
                        
                        try:
                            stuContent = eval(f"module.{q3name}")(sublist[0], sublist[1])
                            ansContent = eval(f"answers.{q3name}")(sublist[0], sublist[1])

                            outfile.write(f'{q3name}({(sublist[0], sublist[1])}):\n')

                            thirdQ = testEquality(stuContent, ansContent, thirdQ)
                        except:
                            outfile.write('error in executing call\n')
                            print('failure in function call?')
                            finalReport.write("ERR,")                            
                        
                except Exception as e:
                    outfile.write("Exception: {}\n".format(e))
                    finalReport.write("ERR,")
                
                outfile.write("{}: {}/{} passed\n\n".format(q3name,thirdQ,len(list3)))
                if thirdQ == len(list3):
                    totalCorrectQ3 += 1

                # sum all correct answers for individual student, divide by possible correct for % correct
                allCorrect = firstQ + secondQ + thirdQ
                totalPossible = sum([len(list1),len(list2),len(list3)])
                finalReport.write("{},".format(allCorrect))
                finalReport.write("{},".format(totalPossible))
                finalReport.write("{}%".format(round((allCorrect/totalPossible)*100,2)))

            except Exception as e:
                outfile.write("Exception running {}: {}\n".format(q2name,e))
                for i in range(len(list3)):
                    finalReport.write("ERR,")
            outfile.write('\n\n')

            # if the number of docstrings is not equal to the number of questions, add a reminder in the student
            # feedback file
            if docStrings != len(allQs):
                outfile.write("\nPlease remember to include docstrings.")
            outfile.close()

            # student record in final report complete, start next line.
            finalReport.write('\n')
            
                
    except Exception as e:
        print('\n*** *** *** *** *** Compiler Error: {}: {}'.format(files[i],e))
        finalReport.write('compiler error: {}: {}'.format(files[i],e))
        finalReport.write('\n')
    #sys.stdout = original_stdout
    print()
finalReport.close()

# output a quick report across students to the shell
print("Evaluation Complete")
print("{} correct: {}/{}".format(q1name, totalCorrectQ1, totalFiles))
print("{} correct: {}/{}".format(q2name, totalCorrectQ2, totalFiles))
print("{} correct: {}/{}".format(q3name, totalCorrectQ3, totalFiles))
print("Total files: {}".format(totalFiles))

