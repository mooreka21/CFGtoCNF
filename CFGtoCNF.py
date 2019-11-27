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
        # step 2: remove all empty strings
        #for i in range(CNF):
            #if CNF[i] == "e":
                # need to come up with cases & figure out how to delete the empty string while keeping the

        stage2 = ""
        out.write("STEP 2: \n\n" + stage2 + "\n")
        # step 3: remove S0->S (copy S to S0)
        new = start + "0" + CNF[7:CNF.find("\n", 6)]
        CNF = CNF.replace(firstline, new)   # by design, the second line will always begin at index 6 because the first
                                            # line will always be initialized with 5 chars plus the newline character

        stage3 = CNF
        out.write("STEP 3: \n\n" + stage3 + "\n")
        # step 4: remove rules that go to three or more terms

        stage4 = ""
        out.write("STEP 4: \n\n" + stage4 + "\n")
        # step 5: remove rules that have capital letters combined with lowercase letters

        stage5 = ""
        out.write("STEP 5: \n\n" + stage5 + "\n")




my_CFG = convertToString("CFG.txt")

convertToCNF(my_CFG, "test.txt")

