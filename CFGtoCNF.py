#!/usr/bin/python

# CS 357 B
# Fall 2019
# Kayla Moore & Addison Raak
# Python program that converts a Context Free Grammar into Chomsky Normal Form


# ==================================================================================
# convertToString - reads input file and converts it to a string.
# ==================================================================================
def convertToString(inputfile):
    # also need to check that it is in a valid CFG format! consult bio423 labs for similar check
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
    rules = []
    language = []
    with open(outputfile, "w") as out:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # step 1: make new start rule
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        start = CFG[0]   # finding original start letter
        firstline = start + "0->" + start
        CNF = firstline + "\n" + CFG
        stage1 = CNF
        # print updated grammar to output file
        out.write("STEP 1: \n\n" + stage1 + "\n\n")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # step 2: remove all empty string components
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        out.write("STEP 2: \n")
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

                                    # ==================================================================================
                                    # CASE: rule is not combined with any other character
                                    # ==================================================================================
                                    # EXAMPLE: A
                                    if (list[j][location - 1] == ">" or list[j][location - 1] == "|") and (
                                            list[j][location + 1] == "|" or list[j][location + 1] == "\n"):
                                        list[j] = list[j] + "|e"  # propagating empty string
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        #=if list[k][i - 1] == "|":
                                        if "|e" in list[k]:
                                            list[k] = list[k].replace("|e", "")
                                        # e is only case for rule
                                        #if list[k][i - 1] == ">":
                                        elif ">e" in list[k]:
                                            list[k] = list[k].replace(list[k], "")

                                    # ==================================================================================
                                    # CASE: rule is combined with other characters
                                    # ==================================================================================

                                    if location < len(list[k]) - 1:

                                        # there are two chars following rule
                                        # EXAMPLE: AXX or Axx
                                        if (list[j][location + 1] != "|" and list[j][location + 1] != "\n") and (
                                                list[j][location + 1] != rule and list[j][location + 2] != "|" and (
                                                list[j][location + 2] != "\n")) and (
                                                list[j][location + 2] != rule):
                                            list[j] = list[j] + "|" + list[j][location + 1:location + 3]
                                            #
                                            # remove original empty string from rule
                                            #
                                            # there is component before the 'e' component
                                            if list[k][i - 1] == "|":
                                                list[k] = list[k].replace("|e", "")
                                            # e is only case for rule
                                            elif list[k][i - 1] == ">":
                                                list[k] = list[k].replace(list[k], "")

                                        # there are two rules with a character in between
                                        # EXAMPLE: AXA or AxA
                                        if (list[j][location + 1] != "|" and list[j][location + 1] != "\n") and (
                                                list[j][location + 1] != rule) and list[j][location + 2] != "|" and (
                                                list[j][location + 2] != "\n") and (
                                                list[j][location + 2] == rule):
                                            list[j] = list[j] + "|" + \
                                                      list[j][location + 1:location + 3] + "|" + \
                                                      list[j][location:location + 2] + "|" + \
                                                      list[j][location + 1]
                                            #
                                            # remove original empty string from rule
                                            #
                                            # there is component before the 'e' component
                                            if list[k][i - 1] == "|":
                                                list[k] = list[k].replace("|e", "")
                                            # e is only case for rule
                                            elif list[k][i - 1] == ">":
                                                list[k] = list[k].replace(list[k], "")

                                        # there are two rules, then a character following
                                        # EXAMPLE: AAX or AAx
                                        if list[j][location + 1] == rule and list[j][location + 2] != "|" and (
                                                list[j][location + 2] != "\n") and list[j][location + 2] != "" and(
                                                list[j][location + 2] != rule):
                                            list[j] = list[j] + "|" + list[j][location + 1]
                                            #
                                            # remove original empty string from rule
                                            #
                                            # there is component before the 'e' component
                                            if list[k][i - 1] == "|":
                                                list[k] = list[k].replace("|e", "")
                                            # e is only case for rule
                                            elif list[k][i - 1] == ">":
                                                list[k] = list[k].replace(list[k], "")

                                    if location < len(list[k]):

                                        # there is one char proceeding and following rule
                                        # EXAMPLE: XAX or xAx
                                        if (list[j][location - 1] != "|" and list[j][location - 1] != ">") and (
                                                list[j][location + 1] != "|" and list[j][location + 1] != "") and (
                                                list[j][location + 1] != rule) and list[j][location] == rule:

                                            list[j] = list[j] + "|" + list[j][location - 1] + list[j][location + 1]
                                            #
                                            # remove original empty string from rule
                                            #
                                            # there is component before the 'e' component
                                            if list[k][i - 1] == "|":
                                                list[k] = list[k].replace("|e", "")
                                            # e is only case for rule
                                            elif list[k][i - 1] == ">":
                                                list[k] = list[k].replace(list[k], "")

                                        # there is only one char proceeding rule
                                        # EXAMPLE: XA or xA
                                        if (list[j][location - 1] != "|" and list[j][location - 1] != ">") and (
                                                list[j][location + 1] == "|" or list[j][location + 1] == "") and (
                                                list[j][location - 2] == "|" or list[j][location - 2] == ">"):
                                            list[j] = list[j] + "|" + list[j][location - 1]
                                            #
                                            # remove original empty string from rule
                                            #
                                            # there is component before the 'e' component
                                            if list[k][i - 1] == "|":
                                                list[k] = list[k].replace("|e", "")
                                            # e is only case for rule
                                            elif list[k][i - 1] == ">":
                                                list[k] = list[k].replace(list[k], "")

                                        # there is only one character following the rule
                                        # EXAMPLE: AX or Ax
                                        if (list[j][location + 1] != "|" and list[j][location + 1] != "") and (
                                                list[j][location - 1] == "|" or list[j][location - 1] == ">") and (
                                                list[j][location + 2] == "|" or list[j][location + 2] == ""):
                                            list[j] = list[j] + "|" + list[j][location + 1]
                                            #
                                            # remove original empty string from rule
                                            #
                                            # there is component before the 'e' component
                                            if list[k][i - 1] == "|":
                                                list[k] = list[k].replace("|e", "")
                                            # e is only case for rule
                                            elif list[k][i - 1] == ">":
                                                list[k] = list[k].replace(list[k], "")

                                        # there are two rules proceeded by a character
                                        # EXAMPLE: XAA or xAA
                                        if (list[j][location - 1] != rule and list[j][location - 1] != "|") and (
                                                list[j][location - 1] != ">" and list[j][location + 1] == rule):
                                            list[j] = list[j] + "|" + list[j][location - 1]
                                            #
                                            # remove original empty string from rule
                                            #
                                            # there is component before the 'e' component
                                            if list[k][i - 1] == "|":
                                                list[k] = list[k].replace("|e", "")
                                            # e is only case for rule
                                            elif list[k][i - 1] == ">":
                                                list[k] = list[k].replace(list[k], "")

                                    # there are two chars proceeding rule
                                    # EXAMPLE: XXA or xxA
                                    if (list[j][location - 1] != "|" and list[j][location - 1] != ">") and (
                                            list[j][location - 2] != "|" and list[j][
                                        location - 2] != ">") and (
                                            list[j][location - 2] != rule):
                                        list[j] = list[j] + "|" + list[j][location - 2:location]
                                        #
                                        # remove original empty string from rule
                                        #
                                        # there is component before the 'e' component
                                        if list[k][i - 1] == "|":
                                            list[k] = list[k].replace("|e", "")
                                        # e is only case for rule
                                        elif list[k][i - 1] == ">":
                                            list[k] = list[k].replace(list[k], "")

                string = ""
                for i in range(len(list)):
                    string = string + list[i] + "\n"

                    CNF = CNF.replace(CNF[0:], string)
                count = sum('e' in s for s in list)
                stage2 = CNF
                out.write(stage2 + "\n")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # step 3: remove S0->S (copy S to S0)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # 2nd line always begins at index 6 because step1 initializes the first line with 6 chars
        new = start + "0" + CNF[7:CNF.find("\n", 6)]
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
        out.write("STEP 3: \n" + stage3 + "\n\n\n")

        # check to see if any rule goes to itself
        # make sure no components are just one upper case letter
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # step 4: remove rules that go to three or more terms ------TO-DO--------
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        for k in range(len(mylist)):
            for i in range(len(mylist[k])):
                if "->" and "|" not in mylist[k][i:i+3]:
                    triple = mylist[k][i:i+3]

        stage4 = ""
        out.write("STEP 4: \n\n" + stage4 + "\n")

        # FOR STEP 5 WE MIGHT NEED REGEX TO CHECK UPPER/LOWER
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # step 5: remove rules that have capital letters combined with lowercase letters ------TO-DO--------
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        stage5 = ""
        out.write("STEP 5: \n\n" + stage5 + "\n")


# Runs the program
my_CFG = convertToString("CFG.txt")
convertToCNF(my_CFG, "test.txt")

#my_CFG = convertToString("CFG2.txt")
#convertToCNF(my_CFG, "test2.txt")