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
        # CFG = CFG.replace("\n", "")
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
        out.write("STEP 1: \n" + stage1 + "\n\n")

        # step 2: remove all empty strings ------TO-DO--------
        list = CNF.split("\n")  # split up CNF into seperate strings for each line
        count = sum('e' in s for s in list)
        while count > 0:
            for loop in range(count):
                for k in range(len(list)):  # loop through each line
                    for i in range(len(list[k])):   # loop through contents of line
                        if list[k][i] == "e":
                            rule = list[k][0]   # find rule that contains e
                            for j in range(len(list)):  # search through to find the rule in contents of other rules
                                if list[j].find(rule) != 0:    # so we don't count the rule itself
                                    location = list[j].find(rule)
                                    if location == -1:
                                        continue

                                    # case: rule is not combined with any other character
                                    if (list[j][location - 1] == ">" or list[j][location - 1] == "|") and (
                                            list[j][location + 1] == "|" or list[j][location + 1] == "\n"):
                                        list[j] = list[j] + "|e"  # propagating empty string
                                        # remove original empty string from rule
                                        if list[k][i - 1] == "|" and list[k][i] == "e":  # there is a case before e
                                            list[k] = list[k].replace("|e", "")
                                        elif list[k][i - 1] == ">" and list[k][i] == "e":  # e is only case for rule
                                            list[k] = list[k].replace(list[k], "")

                                    # case: rule is combined with chars
                                    # there are two chars proceeding rule
                                    elif (list[j][location - 1] != "|" and list[j][location - 1] != ">") and (
                                            list[j][location - 2] != "|" and list[j][location - 2] != ">"):
                                        list[j] = list[j] + "|" + list[j][location - 2:location]
                                        # remove original empty string from rule
                                        if list[k][i - 1] == "|" and list[k][i] == "e":  # there is a case before e
                                            list[k] = list[k].replace("|e", "")
                                        elif list[k][i - 1] == ">" and list[k][i] == "e":  # e is only case for rule
                                            list[k] = list[k].replace(list[k], "")
                                    # there is one char proceeding and following rule
                                    # elif (list[j][location - 1] != "|" and list[j][location - 1] != ">") and (
                                    #       list[j][location + 1] != "|" and list[j][location + 1] != "\n"):
                                    #     list[j] = list[j] + "|" + list[j][location - 1] + list[j][location + 1]
                                    # there is one char proceeding rule
                                    elif list[j][location - 1] != "|" and list[j][location - 1] != ">":
                                        list[j] = list[j] + "|" + list[j][location - 1]
                                    # there are two chars following rule
                                    # if (list[j][location + 1] != "|" and list[j][location + 1] != "\n") and (
                                    # list[j][location + 2] != "|" and list[j][location + 2] != "\n"):
                                    # list[j] = list[j] + "|" + list[j][location - 2:location]

                string = ""
                for i in range(len(list)):
                    string = string + list[i] + "\n"

                    CNF = CNF.replace(CNF[0:], string)
                count = sum('e' in s for s in list)

        stage2 = CNF
        out.write("STEP 2: \n" + stage2 + "\n")

        # step 3: remove S0->S (copy S to S0)
        # 2nd line always begins at index 6 because step1 initializes the first line with 6 chars
        new = start + "0" + CNF[7:CNF.find("\n", 6)]
        CNF = CNF.replace(firstline, new)   # replace the first line with a copy of the original CFG's first line
        stage3 = CNF
        out.write("STEP 3: \n" + stage3 + "\n\n\n")

        # check to see if any rule goes to itself
        # make sure no components are just one upper case letter
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
