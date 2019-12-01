#!/usr/bin/python

# CS 357 B
# Fall 2019
# Kayla Moore & Addison Raak


#################################################
# convertToString - reads input file and converting
# to a string
#################################################
def convertToString(inputfile):
    # also need to check that it is in a valid CFG format! consult bio423 labs for similar check
    with open(inputfile, 'r') as file:
        CFG = file.read()
        # remove all return, newline characters, tabs, and spaces
        CFG = CFG.replace("\r", "")
        #CFG = CFG.replace("\n", "")
        CFG = CFG.replace("\t", "")
        CFG = CFG.replace(" ", "")
    return CFG


#################################################
# convertToCNF - takes CFG from convertToString then
# performs conversion to CNF and writes to output file
#################################################
def convertToCNF(CFG, outputfile):
    rules = []
    language = []
    with open(outputfile, "w") as out:
        # step 1: make new start rule
        start = CFG[0]   # finding original start letter
        firstline = start + "0->" + start
        CNF = firstline + "\n" + CFG
        stage1 = CNF
        out.write("STEP 1: \n\n" + stage1 + "\n")

        # step 2: remove all empty strings ------TO-DO--------
        list = CNF.split("\n")  # split up CNF into seperate strings for each line

        for k in range(len(list)):  # loop through each line
            for i in range(len(list[k])):   # loop through contents of line
                if list[k][i] == "e":
                    if list[k][i - 1] == ">" and list[k][i + 1] == "|": # there is another case after e
                        rule = list[k][0]   # find rule that contains e
                        


                    elif list[k][i - 1] == "|" and list[k][i + 1] == "\n":  # there is a case before e


                    elif list[k][i-1] == ">" and list[k][i+1] == "\n":


        stage2 = ""
        out.write("STEP 2: \n\n" + stage2 + "\n")

        # step 3: remove S0->S (copy S to S0)
        # 2nd line always begins at index 6 because step1 initializes the first line with 6 chars
        new = start + "0" + CNF[7:CNF.find("\n", 6)]
        CNF = CNF.replace(firstline, new)   # replace the first line with a copy of the original CFG's first line
        stage3 = CNF
        out.write("STEP 3: \n\n" + stage3 + "\n")

        # step 4: remove rules that go to three or more terms ------TO-DO--------

        stage4 = ""
        out.write("STEP 4: \n\n" + stage4 + "\n")

        # FOR STEP 5 WE MIGHT NEED REGEX TO CHECK UPPER/LOWER
        # step 5: remove rules that have capital letters combined with lowercase letters ------TO-DO--------

        stage5 = ""
        out.write("STEP 5: \n\n" + stage5 + "\n")


# running program
my_CFG = convertToString("CFG.txt")
convertToCNF(my_CFG, "test.txt")
