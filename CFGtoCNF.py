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
        CFG = CFG.replace("\n", "")
        CFG = CFG.replace("\t", "")
        CFG = CFG.replace(" ", "")
    return CFG


#################################################
# convertToCNF - takes CFG from convertToString then
# performs conversion to CNF and writes to output file
#################################################
def convertToCNF(CFG, outputfile):
    with open(outputfile, "w") as out:
        CNF = CFG # placeholder for now
        out.write(CNF)
