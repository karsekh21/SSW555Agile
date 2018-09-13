#!usr/bin/python


#Calvin Han
#CS 555
#Project 02
#I pledge my honor that I have abided by the stevens honor system


import os
import re
import gzip
import argparse
import csv

#checkTags takes in the current row and the file being written in
#Uses a dictionary of all possible combinations of the tags
#Prints out the 2nd half of the output from the current line
def checkTags(row,file):
    length = len(row)
    lvl = {}
    #0 is special cases
    #1 Normal cases
    lvl['0'] = {'FAM':0,'INDI':0,'HEAD':1,'TRLR':1,'NOTE':1,}
    lvl['1'] = {'NAME':1,'SEX':1,'BIRT':1,'DEAT':1,'FAMC':1,'FAMS':1,'MARR':1,'HUSB':1,'WIFE':1,'CHIL':1,'DIV':1}
    lvl['2'] = {'DATE':1}

    if row[0] in lvl:
        if row[1] in lvl[row[0]]:
            if (lvl[row[0]][row[1]]==0):
                file.write('<-- '+row[0]+'|'+row[1]+'|'+'N|'+" ".join(row[2:])+'\n')
            else:
                file.write('<-- '+row[0]+'|'+row[1]+'|'+'Y|'+" ".join(row[2:])+'\n')

        elif(length>2 and row[2] in lvl[row[0]]):
            file.write('<-- '+row[0]+'|'+" ".join(row[2:])+'|'+'Y|'+row[1]+'\n')
        else:
            args = ''
            if length > 2:
                args = " ".join(row[2:])
            file.write('<-- '+row[0]+'|'+row[1]+'|'+'N|'+args+'\n')
    else:
        args = ''
        if length > 2:
            args = " ".join(row[2:])
        file.write('<-- '+row[0]+'|'+row[1]+'|'+'N|'+args+'\n')


#readGED takes in the specified GED file from the user
#Opens the GED file and a file called answers.txt
#Reads the content of the GED file and writes the output on the answer.txt file
def readGED(fileName):
    rfile = open(fileName,'r')
    wfile = open('answers.txt','w')
    lines = rfile.readlines()

    for row in lines:
        wfile.write("--> "+row.strip()+'\n')
        currLine =re.split(r'\s',row.strip())
        checkTags(currLine,wfile)

    rfile.close()
    wfile.close()


#Script accepts a Ged File
#Script open GED file and reads each line
#Prints each lines' Lvl, Id, Valid, and Arg
def main():
    global args
    parser = argparse.ArgumentParser('''
    Program takes in a GED file and outputs the Lvl, ID, Validity, and
    arg of each line in the GED file. The script only takes 1 argument which is the full path
    of the file
    ''')
    parser.add_argument('file',type =str,help="Full path name of File")
    args = parser.parse_args()

    if (not os.path.isfile(args.file)):
        print 'ERROR: file '+'"'+args.file+'"'+' does not exist'
        return 0

    if not (re.search(r'\.ged$',args.file)):
        print 'ERROR: file '+'"'+args.file+'"'+' is not a ged file'
        return 0

    readGED(args.file)


if __name__ == "__main__":
    main()
