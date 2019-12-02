#!/usr/bin/python

# CS 357 B
# Fall 2019
# Kayla Moore & Addison Raak

import re


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
        # CFG = CFG.replace("\n", "")
        CFG = CFG.replace("\t", "")
        CFG = CFG.replace(" ", "")
    return CFG


#################################################
# convertToCNF - takes CFG from convertToString then
# performs conversion to CNF and writes to output file
#################################################
def convertToCNF(CFG, outputfile):
    with open(outputfile, "w") as out:
        # STEP 1: make new start rule
        start = CFG[0]   # finding original start letter
        firstline = start + "0->" + start
        CNF = firstline + "\n" + CFG
        stage1 = CNF
        # print updated grammar to output file
        out.write("STEP 1: \n\n" + stage1 + "\n\n")

        # STEP 2: remove all empty strings ------TO-DO--------
        mylist = CNF.split("\n")  # split up CNF into seperate strings for each line
        count = sum('e' in s for s in mylist)
        while count > 0:
            for loop in range(count):
                for k in range(len(mylist)):  # loop through each line
                    for i in range(len(mylist[k])):   # loop through contents of line
                        if mylist[k][i] == "e":
                            rule = mylist[k][0]   # find rule that contains e
                            for j in range(len(mylist)):  # search through to find the rule in contents of other rules
                                if mylist[j].find(rule) != 0:    # so we don't count the rule itself
                                    location = mylist[j].find(rule)
                                    if location == -1:
                                        continue

                                    # case: rule is not combined with any other character
                                    if (mylist[j][location - 1] == ">" or mylist[j][location - 1] == "|") and (
                                            mylist[j][location + 1] == "|" or mylist[j][location + 1] == "\n"):
                                        mylist[j] = mylist[j] + "|e"  # propagating empty string
                                        # remove original empty string from rule
                                        if mylist[k][i - 1] == "|" and mylist[k][i] == "e":  # there is a case before e
                                            mylist[k] = mylist[k].replace("|e", "")
                                        elif mylist[k][i - 1] == ">" and mylist[k][i] == "e":  # e is only case for rule
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                    # case: rule is combined with chars
                                    # there are two chars proceeding rule
                                    elif (mylist[j][location - 1] != "|" and mylist[j][location - 1] != ">") and (
                                            mylist[j][location - 2] != "|" and mylist[j][location - 2] != ">"):
                                        mylist[j] = mylist[j] + "|" + mylist[j][location - 2:location]
                                        # remove original empty string from rule
                                        if mylist[k][i - 1] == "|" and mylist[k][i] == "e":  # there is a case before e
                                            mylist[k] = mylist[k].replace("|e", "")
                                        elif mylist[k][i - 1] == ">" and mylist[k][i] == "e":  # e is only case for rule
                                            mylist[k] = mylist[k].replace(mylist[k], "")
                                    # there is one char proceeding and following rule
                                    # elif (list[j][location - 1] != "|" and list[j][location - 1] != ">") and (
                                    #       list[j][location + 1] != "|" and list[j][location + 1] != "\n"):
                                    #     list[j] = list[j] + "|" + list[j][location - 1] + list[j][location + 1]
                                    # there is one char proceeding rule
                                    elif mylist[j][location - 1] != "|" and mylist[j][location - 1] != ">":
                                        mylist[j] = mylist[j] + "|" + mylist[j][location - 1]
                                    # there are two chars following rule
                                    # if (list[j][location + 1] != "|" and list[j][location + 1] != "\n") and (
                                    # list[j][location + 2] != "|" and list[j][location + 2] != "\n"):
                                    # list[j] = list[j] + "|" + list[j][location - 2:location]
                # convert list back into string
                string = ""
                for i in range(len(mylist)):
                    string = string + mylist[i] + "\n"
                    CNF = CNF.replace(CNF[0:], string)
                count = sum('e' in s for s in mylist)

        stage2 = CNF
        # print updated grammar to output file
        out.write("STEP 2: \n\n" + stage2 + "\n")

        # STEP 3: remove S0->S (copy S to S0) and remove any solo rules within a rule's contents
        new = start + "0" + CNF[7:CNF.find("\n", 6)]    # first line is initialized with 6 chars; start index of line 2
        CNF = CNF.replace(firstline, new)   # replace the first line with a copy of the original CFG's first line

        # remove any rules that point to a solo rule (single uppercase character)
        mylist = CNF.split("\n")  # split up CNF into separate strings for each line
        print(mylist)
        copy = ""
        for k in range(len(mylist)):
            for i in range(len(mylist[k])-1):
                if i != 0:
                    # first location of rule contents
                    if mylist[k][i-1] == ">" and mylist[k][i+1] == "|" and mylist[k][i].isupper():
                        rule = mylist[k][i]
                        print(rule)
                        for j in range(len(mylist)-1):
                            if mylist[j][0] == rule:
                                copy = mylist[j][mylist[j].find(">")+1:]
                                print(copy)
                        mylist[k] = mylist[k].replace(mylist[k][i], copy)
                        print(mylist[k])
                        print(i)
                    # middle location of rule contents
                    elif mylist[k][i - 1] == "|" and mylist[k][i + 1] == "|" and mylist[k][i].isupper():
                        rule = mylist[k][i]
                        print(rule)
                        for j in range(len(mylist) - 1):
                            if mylist[j][0] == rule:
                                copy = mylist[j][mylist[j].find(">") + 1:]
                                print(copy)
                        mylist[k] = mylist[k].replace(mylist[k][i], copy)
                        print(mylist[k])
                        print(i)
                    # last location of rule contents
                    # elif mylist[k][i-1] == "|" and mylist[k][i+1] == "" and mylist[k][i].isupper():
                    #     rule = mylist[k][i]
                    #     print(rule)
                    #     for j in range(len(mylist) - 1):
                    #         if mylist[j][0] == rule:
                    #             copy = mylist[j][mylist[j].find(">") + 1:]
                    #             print(copy)
                    #     mylist[k] = mylist[k].replace(mylist[k][i], copy)
                    #     print(mylist[k])
                    #     print(i)
                    # last location of rule contents
                    elif mylist[k][-2] == "|" and mylist[k][-1].isupper():
                        rule = mylist[k][-1]
                        for j in range(len(mylist)-1):
                            if mylist[j][0] == rule:
                                copy = mylist[j][mylist[j].find(">") + 1:]
                        mylist[k] = mylist[k].replace(mylist[k][-1], copy)

        # convert list back into string
        string = ""
        for i in range(len(mylist)):
            string = string + mylist[i] + "\n"
            CNF = CNF.replace(CNF[0:], string)
        stage3 = CNF
        # print updated grammar to output file
        out.write("STEP 3: \n\n" + stage3 + "\n")

        # STEP 4: remove rules that go to three or more terms ------TO-DO--------
        for k in range(len(mylist)):
            for i in range(len(mylist[k])):
                if "->" and "|" not in mylist[k][i:i+3]:
                    triple = mylist[k][i:i+3]

        stage4 = ""
        out.write("STEP 4: \n\n" + stage4 + "\n")

        # FOR STEP 5 WE MIGHT NEED REGEX TO CHECK UPPER/LOWER
        # STEP 5: remove rules that have capital letters combined with lowercase letters ------TO-DO--------

        stage5 = ""
        out.write("STEP 5: \n\n" + stage5 + "\n")


# running program
my_CFG = convertToString("CFG.txt")
convertToCNF(my_CFG, "test.txt")

#my_CFG = convertToString("CFG2.txt")
#convertToCNF(my_CFG, "test2.txt")