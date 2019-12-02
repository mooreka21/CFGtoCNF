#!/usr/bin/python

# CS 357 B
# Fall 2019
# Kayla Moore & Addison Raak
# Python program that converts a Context Free Grammar into Chomsky Normal Form


#################################################
# convertToString - reads input file and converting
# to a string. Assumes inputfile is in valid CFG format
#################################################
def convertToString(inputfile):
    with open(inputfile, 'r') as file:
        CFG = file.read()
        # remove all returns, tabs, and spaces
        CFG = CFG.replace("\r", "")
        CFG = CFG.replace("\t", "")
        CFG = CFG.replace(" ", "")
    # returns the CFG as a string with all spacing removed
    return CFG


# ==================================================================================
# convertToCNF - takes CFG from convertToString then performs conversion to CNF and
#                writes to the output file.
#
# Everything on the left side of the arrow, we refer to as 'rules'
# Everything on the right side of the arrow, we refer to as 'components'
#
# ==================================================================================
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
        msg = "STEP 2: \n"
        while count > 0:
            for loop in range(count):
                for k in range(len(mylist)):  # loop through each line
                    for i in range(len(mylist[k])):   # loop through contents of line
                        if mylist[k][i] == "e":
                            rule = mylist[k][0]   # find rule that contains e
                            for j in range(len(mylist)):  # search through to find the rule in contents of other rules
                                location = mylist[j].find(rule)
                                if location == -1:
                                    continue
                                if location == 0:
                                    location = mylist[j].find(rule, 1)
                                # ==================================================================================
                                # CASE: rule is not combined with any other character
                                # ==================================================================================
                                # EXAMPLE: A
                                if (mylist[j][location - 1] == ">" or mylist[j][location - 1] == "|") and (
                                        mylist[j][location + 1] == "|" or mylist[j][location + 1] == "\n"):
                                    mylist[j] = mylist[j] + "|e"  # propagating empty string
                                    #
                                    # remove original empty string from rule
                                    #
                                    # there is component before the 'e' component
                                    #=if mylist[k][i - 1] == "|":
                                    if "|e" in mylist[k]:
                                        mylist[k] = mylist[k].replace("|e", "")
                                    # e is only case for rule
                                    #if mylist[k][i - 1] == ">":
                                    elif ">e" in mylist[k]:
                                        mylist[k] = mylist[k].replace(mylist[k], "")

                                # ==================================================================================
                                # CASE: rule is combined with other characters
                                # ==================================================================================

                                if location < len(mylist[j]) - 2:

                                    # there are two chars following rule
                                    # EXAMPLE: AXX or Axx
                                    if (mylist[j][location + 1] != "|" and mylist[j][location + 1] != "\n") and (
                                            mylist[j][location + 1] != rule and mylist[j][location + 2] != "|" and (
                                            mylist[j][location + 2] != "\n")) and (
                                            mylist[j][location + 2] != rule):
                                        mylist[j] = mylist[j] + "|" + mylist[j][location + 1:location + 3]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                    # there are two rules with a character in between
                                    # EXAMPLE: AXA or AxA
                                    if (mylist[j][location + 1] != "|" and mylist[j][location + 1] != "\n") and (
                                            mylist[j][location + 1] != rule) and mylist[j][location + 2] != "|" and (
                                            mylist[j][location + 2] != "\n") and (
                                            mylist[j][location + 2] == rule):
                                        mylist[j] = mylist[j] + "|" + \
                                                  mylist[j][location + 1:location + 3] + "|" + \
                                                  mylist[j][location:location + 2] + "|" + \
                                                  mylist[j][location + 1]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                    # there are two rules, then a character following
                                    # EXAMPLE: AAX or AAx
                                    if mylist[j][location + 1] == rule and mylist[j][location + 2] != "|" and (
                                            mylist[j][location + 2] != "\n") and mylist[j][location + 2] != "" and(
                                            mylist[j][location + 2] != rule) and mylist[j][location] == rule:
                                        mylist[j] = mylist[j] + "|" + mylist[j][location + 2]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                if location <= len(mylist[j]) - 2:

                                    # there is one char proceeding and following rule
                                    # EXAMPLE: XAX or xAx
                                    if (mylist[j][location - 1] != "|" and mylist[j][location - 1] != ">") and (
                                            mylist[j][location - 1] != rule) and (
                                            mylist[j][location + 1] != "|" and mylist[j][location + 1] != "") and (
                                            mylist[j][location + 1] != rule) and mylist[j][location] == rule:

                                        mylist[j] = mylist[j] + "|" + mylist[j][location - 1] + mylist[j][location + 1]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                    # there is only one char proceeding rule
                                    # EXAMPLE: XA or xA
                                    if (mylist[j][location - 1] != "|" and mylist[j][location - 1] != ">") and (
                                            mylist[j][location + 1] == "|" or mylist[j][location + 1] == "") and (
                                            mylist[j][location - 2] == "|" or mylist[j][location - 2] == ">"):
                                        mylist[j] = mylist[j] + "|" + mylist[j][location - 1]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                    # there is only one character following the rule
                                    # EXAMPLE: AX or Ax
                                    if (mylist[j][location + 1] != "|" and mylist[j][location + 1] != "") and (
                                            mylist[j][location - 1] == "|" or mylist[j][location - 1] == ">") and (
                                            mylist[j][location + 2] == "|" or mylist[j][location + 2] == ""):
                                        mylist[j] = mylist[j] + "|" + mylist[j][location + 1]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                    # there are two rules proceeded by a character
                                    # EXAMPLE: XAA or xAA
                                    if (mylist[j][location - 1] != rule and mylist[j][location - 1] != "|") and (
                                            mylist[j][location - 1] != ">" and mylist[j][location + 1] == rule):
                                        mylist[j] = mylist[j] + "|" + mylist[j][location - 1]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")

                                # there are two chars proceeding rule
                                # EXAMPLE: XXA or xxA
                                if (mylist[j][location - 1] != "|" and mylist[j][location - 1] != ">") and (
                                        mylist[j][location - 2] != "|" and mylist[j][
                                    location - 2] != ">") and (
                                        mylist[j][location - 2] != rule):
                                    mylist[j] = mylist[j] + "|" + mylist[j][location - 2:location]
                                    #
                                    # remove original empty string from rule
                                    #
                                    # there is component before the 'e' component
                                    if mylist[k][i - 1] == "|":
                                        mylist[k] = mylist[k].replace("|e", "")
                                    # e is only case for rule
                                    elif mylist[k][i - 1] == ">":
                                        mylist[k] = mylist[k].replace(mylist[k], "")

                                    # there is only one char proceeding rule
                                    # EXAMPLE: XA or xA
                                    if (mylist[j][location - 1] != "|" and mylist[j][location - 1] != ">") and (
                                            mylist[j][location - 2] == "|" or mylist[j][location - 2] == ">"):
                                        mylist[j] = mylist[j] + "|" + mylist[j][location - 1]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if mylist[k][i - 1] == "|":
                                            mylist[k] = mylist[k].replace("|e", "")
                                        # e is only case for rule
                                        elif mylist[k][i - 1] == ">":
                                            mylist[k] = mylist[k].replace(mylist[k], "")
                # check that list doesnt have an empty value
                if mylist[len(mylist) - 1] == "":
                    mylist.remove(mylist[len(mylist) - 1])
                # convert list back to string
                string = ""
                for i in range(len(mylist)):
                    string = string + mylist[i] + "\n"
                    CNF = CNF.replace(CNF[0:], string)
                count = sum('e' in s for s in mylist)

                stage2 = CNF
                # print updated grammar to output file
                out.write(msg + "\n" + stage2 + "\n")
                msg = ""

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
                    elif mylist[k][i-1] == "|" and mylist[k][i+1] == "" and mylist[k][i].isupper():
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
                    elif mylist[k][-2] == "|" and mylist[k][-1].isupper():
                        rule = mylist[k][-1]
                        for j in range(len(mylist)-1):
                            if mylist[j][0] == rule:
                                copy = mylist[j][mylist[j].find(">") + 1:]
                        mylist[k] = mylist[k].replace(mylist[k][-1], copy)

        # check that list doesnt have an empty value
        if mylist[len(mylist)-1] == "":
            mylist.remove(mylist[len(mylist)-1])
        # convert list back into string
        string = ""
        for i in range(len(mylist)):
            string = string + mylist[i] + "\n"
            CNF = CNF.replace(CNF[0:], string)
        stage3 = CNF
        # print updated grammar to output file
        out.write("STEP 3: \n\n" + stage3 + "\n")

        # STEP 4: remove rules that go to three or more terms ------TO-DO--------
        alpha = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
        lower = alpha.split(" ")
        upper = alpha.upper().split(" ")
        #for k in range(len(mylist)):
            #for i in range(len(mylist[k])):
                #if mylist[k][i:i+3]:
                    #triple = mylist[k][i:i+3]

        stage4 = ""
        out.write("STEP 4: \n\n" + stage4 + "\n")

        # STEP 5: remove rules that have capital letters combined with lowercase letters
        rulecount = 1
        index = 0
        for k in range(len(mylist)):
            for i in range(len(mylist[k])-1):
                if mylist[k][i] in lower and mylist[k][i+1] in upper:
                    if mylist[k][i] != index:
                        new = upper[0] + str(rulecount)
                        rulecount += 1
                        index = mylist[k][i]
                        mylist.append(new + "->" + mylist[k][i])
                    mylist[k] = mylist[k].replace(mylist[k][i], new)
                elif mylist[k][i] in upper and mylist[k][i+1] in lower:
                    if mylist[k][i+1] != index:
                        new = upper[1] + str(rulecount)
                        rulecount += 1
                        index = mylist[k][i+1]
                        mylist.append(new + "->" + index)
                    mylist[k] = mylist[k].replace(mylist[k][i+1], new)

        # convert list back into string
        string = ""
        for i in range(len(mylist)):
            string = string + mylist[i] + "\n"
            CNF = CNF.replace(CNF[0:], string)
        stage5 = CNF
        out.write("STEP 5: \n\n" + stage5 + "\n")

        # CFG successfully converted into Chomsky Normal Form!
        out.write("\n-------CFG SUCCESSFULLY CONVERTED TO CNF!-------")


# Runs the program
my_CFG = convertToString("CFG.txt")
convertToCNF(my_CFG, "test.txt")

my_CFG2 = convertToString("CFG2.txt")
convertToCNF(my_CFG2, "test2.txt")

my_CFG3 = convertToString("CFG3.txt")
convertToCNF(my_CFG3, "test3.txt")