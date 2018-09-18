#!usr/bin/python


#Calvin Han, Matt Sirota, Karun Sekhar
#CS 555
#Project 03
#I pledge my honor that I have abided by the stevens honor system

#Theese modules are used in order to use certain functions
import prettytable
import os
import re
import gzip
import argparse
import csv
from datetime import datetime, date

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


def checkDeatBeforeBirt(birth,death):
    if birth == 'N/A':
        return False
    else:
        if death == 'N/A':
            return True
        else:
            birth = datetime.strptime(birth,'%d %b %Y')
            death = datetime.strptime(death,'%d %b %Y')
            return (calculate_age(birth,death)>=0)




#saveInfo takes in the current row and the file being written in
#Uses a dictionary of all possible combinations of the tags
#Prints out the 2nd half of the output from the current line
def saveInfo(listOfPpl,listOfFam,row):
    #Dictionary that will contain the info on each indi or fam
    randIndi = {'ID':'N/A','NAME':'N/A','SEX':'N/A','AGE':'N/A','BIRT':'N/A','DEAT':'N/A','FAMC':'N/A','FAMS':'N/A','ALIVE':True}
    randFam = {'ID':'N/A','MARR':'N/A','DIV':'N/A','HUSB':'N/A','HUSBNAME':'N/A','WIFE':'N/A','WIFENAME':'N/A','CHIL':list()}

    #Checks if the current row is lvl 0
    if row[0] == '0':
        #checks if it is an individual or a family
        if row[2] == 'INDI':
            randIndi['ID'] = row[1]
            listOfPpl.append(randIndi)
        elif row[2] == 'FAM':
            randFam['ID'] = row[1]
            listOfFam.append(randFam)
    #Checks if the current row is lvl 1
    elif row[0]== '1':
        #Place info for the proper tags for ppl list except BIRT and DEAT tag
        if row[1] in listOfPpl[-1] and row[1] != 'BIRT' and row[1] != 'DEAT':
            listOfPpl[-1][row[1]] = " ".join(row[2:])
        #Place a marker for BIRT tag to show it was called
        elif row[1] == 'BIRT':
            listOfPpl[-1][row[1]] = True
        #Place a marker for DEAT tag to show it was called
        elif row[1] == 'DEAT':
            listOfPpl[-1][row[1]] = True
            listOfPpl[-1]['ALIVE']= False
        #Place info for the proper tags for fam list
        elif row[1] in listOfFam[-1] and row[1] != 'MARR' and row[1] != 'DIV' and row[1] != 'CHIL':
            listOfFam[-1][row[1]] = " ".join(row[2:])
            if row[1] == 'HUSB' or row[1] == 'WIFE':
                for ppl in listOfPpl:
                    if " ".join(row[2:]) == ppl['ID'] :
                        listOfFam[-1][row[1]+'NAME'] = ppl['NAME']
        elif row[1] == 'MARR':
            listOfPpl[-1][row[1]] = True
        elif row[1] == 'DIV':
            listOfPpl[-1][row[1]] = True
        elif row[1] == 'CHIL':
            listOfFam[-1][row[1]].append(" ".join(row[2:]))

    #Checks if it is 2 tag which must be for the a Date
    elif row[0] == '2':
        if row[1] == 'DATE':
            if listOfPpl[-1]['BIRT'] and not isinstance(listOfPpl[-1]['BIRT'], str):
                listOfPpl[-1]['BIRT'] = " ".join(row[2:])
            elif listOfPpl[-1]['DEAT'] and not isinstance(listOfPpl[-1]['DEAT'], str):
                listOfPpl[-1]['DEAT'] = " ".join(row[2:])
            elif listOfFam[-1]['MARR']:
                listOfFam[-1]['MARR'] = " ".join(row[2:])
            elif listOfFam[-1]['DIV']:
                listOfFam[-1]['DIV'] = " ".join(row[2:])
        else:
            print('Error:Date was given but no tag before accepted it')

#calculate_age takes in the year born and the year wanted to calc age
#calculates the age of the current individual
#returns the age of the current individual
def calculate_age(born,upTo):
    return upTo.year - born.year - ((upTo.month, upTo.day) < (born.month, born.day))


#readGED takes in the specified GED file from the user
#Opens the GED file and store each indi and fam in a list
#Reads the content of the GED file and writes the output on the answer.txt file
def readGED(fileName):
    #list of INDI and Fam
    listOfPpl = []
    listOfFam = []

    from prettytable import PrettyTable

    ind_table=PrettyTable();
    fam_table=PrettyTable();

    ind_table.field_names=["ID","Name","Gender","Birthday","Age","Alive","Death","Child","Spouse"]
    fam_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

    #Opens the file specified by the User
    rfile = open(fileName,'r')
    #Reads each line and places each line in a list
    lines = rfile.readlines()

    #For loop goes through the entire lines list
    for row in lines:
        #Splits the string up by spaces
        currLine =re.split(r'\s',row.strip())
        #calls saveInfo
        saveInfo(listOfPpl,listOfFam,currLine)


    #Creates the table of all families
    for fam in listOfFam:
        fam_table.add_row([fam['ID'],fam['MARR'],fam['DIV'],fam['HUSB'], fam['HUSBNAME'], fam['WIFE'], fam['WIFENAME'], fam['CHIL']])

    print'\n'

    #Creates the table of all Individuals
    for ppl in listOfPpl:
        #Used to check the age of the Individuals
        born = datetime.strptime(ppl['BIRT'],'%d %b %Y')
        if (ppl['ALIVE']):
            upTo = date.today()
        else:
            upTo = datetime.strptime(ppl['DEAT'],'%d %b %Y')
        ppl['AGE'] = calculate_age(born,upTo)
        ind_table.add_row([ppl['ID'],ppl['NAME'],ppl['SEX'],ppl['BIRT'], ppl['AGE'], ppl['ALIVE'],ppl['DEAT'], ppl['FAMC'], ppl['FAMS']])

    print ('Individuals')
    print ind_table
    print('\n')
    print ('Families')
    print fam_table

    rfile.close()


#Script accepts a Ged File
#Script open GED file and reads each line
#Prints each lines' Lvl, Id, Valid, and Arg
def main():
    #Creates args that will hold the specific arguments passed by the user
    global args
    parser = argparse.ArgumentParser('''
    Program takes in a GED file and outputs the Lvl, ID, Validity, and
    arg of each line in the GED file. The script only takes 1 argument which is the full path
    of the file
    ''')
    #parser will receive the args from the user and place them in the field 'file'
    parser.add_argument('file',type =str,help="Full path name of File")
    #places the field 'file' into args
    args = parser.parse_args()

    #checks the field 'file' a legitimate path to the file
    if (not os.path.isfile(args.file)):
        print 'ERROR: file '+'"'+args.file+'"'+' does not exist'
        return 0

    #checks the field 'file' and sees if it is a ged file
    if not (re.search(r'\.ged$',args.file)):
        print 'ERROR: file '+'"'+args.file+'"'+' is not a ged file'
        return 0

    #calls function readGED to store info of user
    readGED(args.file)


if __name__ == "__main__":
    main()
