path = "contains unorganized .py files"

import glob, os
to set up all of the new python files to test:
for filename in glob.glob(os.path.join(path,'*.py')):
    try:
        identifiers = filename.split('-')
        name = identifiers[2].split()
        finalName = "{}{}".format(name[1],name[0])
        infile = open(filename,'r')
        content = infile.read()
        infile.close()
        studentFile = open(finalName+'.py','w')
        studentFile.write(content)
        studentFile.close
    except:
        pass

files = []

import MorrisAnswers404_6

for filename in glob.glob('*.py'):
    if filename == 'grader.py' or filename == "MorrisAnswers404_6.py":
        continue
    forOpen = filename.replace('.py','')
    files.append(forOpen)
for i in range(len(files)):
    try:
        for module in [__import__(files[i])]:
            print("\n################\n\n#Report for: {}\n\n################".format(files[i]))
            try:
                for j in range(-2,6):
                    if module.catAge(j) != MorrisAnswers404_6.catAge(j):
                        print("ERROR ON catAge")
                    else:
                        print("catAge passed for {}".format(j))
                if module.catAge("j") != MorrisAnswers404_6.catAge("j"):
                        print("Error on catAge exception")
            except:
                print("catAge ERROR "+files[i])
            try: #try second method
                testlist = [ "empty.txt", "file1.txt", "blort.txt"]
                for test in testlist:
                    module.formatNames(test)
                    print("formatNames passed for {}".format(test))
            except:
                print("formatNames ERROR "+files[i])
    except:
        print('\n*** *** *** *** *** Compiler Error: {}'.format(files[i]))
