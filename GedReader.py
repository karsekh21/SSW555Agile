#!/usr/bin/python


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
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from usXX import utilities_US

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


def saveInfoZeroTag(listOfPpl,listOfFam,code, tag):
    #Dictionary that will contain the info on each indi or fam
    randIndi = {'ID':'N/A','NAME':'N/A','SEX':'N/A','AGE':'N/A','BIRT':'N/A','DEAT':'N/A','FAMC':list(),'FAMS':list(),'ALIVE':True}
    randFam = {'ID':'N/A','MARR':'N/A','DIV':'N/A','HUSB':'N/A','HUSBNAME':'N/A','WIFE':'N/A','WIFENAME':'N/A','CHIL':list()}
    if (tag == 'INDI'):
        randIndi['ID'] = code
        listOfPpl.append(randIndi)
    elif (tag == 'FAM'):
        randFam['ID'] = code
        listOfFam.append(randFam)


def saveInfoOneTag(listOfPpl,listOfFam,code, tag):
    #Dictionary that will contain the info on each indi or fam

    if tag == 'BIRT':
        listOfPpl[-1][tag] = True

    elif tag == 'DEAT':
        listOfPpl[-1]['ALIVE'] = False
        listOfPpl[-1][tag] = True

    elif tag == 'MARR' or tag == 'DIV':
        listOfFam[-1][tag] = True

    elif tag == 'CHIL':
        listOfFam[-1][tag].append(" ".join(code))

    elif tag == 'FAMC' or tag == 'FAMS':
        listOfPpl[-1][tag].append(" ".join(code))

    elif tag in listOfPpl[-1]:
        listOfPpl[-1][tag] = " ".join(code)
    elif tag in listOfFam[-1]:
        if tag == 'HUSB' or tag == 'WIFE':
            for ppl in listOfPpl:
                if " ".join(code) == ppl['ID'] :
                    listOfFam[-1][tag+'NAME'] = ppl['NAME']
        listOfFam[-1][tag] = " ".join(code)


def saveInfoTwoTag(listOfPpl,listOfFam,code, tag):
    #Dictionary that will contain the info on each indi or fam
    if tag == 'BIRT' or tag == 'DEAT':
        listOfPpl[-1][tag] = " ".join(code)
    elif tag == 'DIV' or tag == 'MARR':
        listOfFam[-1][tag] = " ".join(code)



#saveInfo takes in the current row and the file being written in
#Uses a dictionary of all possible combinations of the tags
#Prints out the 2nd half of the output from the current line
def saveInfo(listOfPpl,listOfFam,lines):
    count = 0
    for curLine in lines:
        #Splits the string up by spaces
        row =re.split(r'\s',curLine.strip())
        #calls saveInfo
        #Checks if the current row is lvl 0
        if row[0] == '0':
            #checks if it is an individual or a family
            saveInfoZeroTag(listOfPpl,listOfFam,row[1],row[2])

        #Checks if the current row is lvl 1
        elif row[0]== '1':
            #Place info for the proper tags for ppl list except BIRT and DEAT tag
            saveInfoOneTag(listOfPpl,listOfFam,row[2:],row[1])

        #Checks if it is 2 tag which must be for the a Date
        elif row[0] == '2':
            prevTag =  re.split(r'\s',lines[count-1].strip())[1]

            saveInfoTwoTag(listOfPpl,listOfFam,row[2:],prevTag)

        count+=1

#calculate_age takes in the year born and the year wanted to calc age
#calculates the age of the current individual
#returns the age of the current individual
def calculate_age(born,upTo):
    if((upTo.month, upTo.day) < (born.month, born.day)):
        return upTo.year - born.year - 1
    else:
        return upTo.year - born.year - 0


def checkDeatBeforeBirt(birth,death):
    if birth == 'N/A':
        return False
    if death == 'N/A':
        return True

    born = datetime.strptime(birth,'%d %b %Y')
    died = datetime.strptime(death,'%d %b %Y')

    if (calculate_age(born,died)<0):
        return False
    else:
        return True

#Makes sure that person's dates are before current date
def US01(ppl,fam):
    for x in ppl['FAMS'] :
    	if(x==fam['ID']):
    		birth = datetime.strptime(ppl['BIRT'],'%d %b %Y')
    		death=datetime.today()
    		divorce=datetime.today()
    		marriage=datetime.strptime(fam['MARR'],'%d %b %Y')
    		current=datetime.today()
    		if(ppl['ALIVE']==False):
    			death = datetime.strptime(ppl['DEAT'],'%d %b %Y')
    		if(fam['DIV']!='N/A'):
    			divorce=datetime.strptime(fam['DIV'],'%d %b %Y')
    		if(birth>current or death>current or divorce>current or marriage>current):
    			return False
    for x in ppl['FAMC']:
    	if(x==fam['ID']):
    		birth = datetime.strptime(ppl['BIRT'],'%d %b %Y')
    		death=datetime.today()
    		current=datetime.today()
    		if(ppl['ALIVE']==False):
    			death = datetime.strptime(ppl['DEAT'],'%d %b %Y')
    		if(birth>current or death>current):
    			return False
    return True


#makes sure that birth comes before marriage
def US02(ppl,fam):
    for x in ppl['FAMS'] :
    	if(x==fam['ID']):
    		marriage=datetime.strptime(fam['MARR'],'%d %b %Y')
    		birth = datetime.strptime(ppl['BIRT'],'%d %b %Y')
    		if(marriage<birth):
    			return False
    	return True

#makes sure birth comes before death
def US03(ppl):
	if (ppl['ALIVE']==True):
		return True
	birth = datetime.strptime(ppl['BIRT'],'%d %b %Y')
	death = datetime.strptime(ppl['DEAT'],'%d %b %Y')

	if(death<birth):
		return False
	return True

#makes sure that marriage occurs before a divorce
def US04(fam):
    if(fam['DIV']!='N/A' and fam['MARR']!='N/A'):
        marriage=datetime.strptime(fam['MARR'], '%d %b %Y');
        divorce=datetime.strptime(fam['DIV'], '%d %b %Y');
        if(divorce<marriage):
            return False
    if(fam['DIV']!='N/A' and fam['MARR']=='N/A'):
            return False
    return True

#makes sure that marriage occurs before death
def US05(ppl, fam):
    if (fam['MARR']!='N/A' and ppl['DEAT']!='N/A'):
        for x in ppl['FAMS']:
    		if(fam['ID']==x):
    			death=datetime.strptime(ppl['DEAT'], '%d %b %Y')
    			married=datetime.strptime(fam['MARR'], '%d %b %Y')

    			if(death<married):
    				return False

	return True

#makes sure that divorce occurs before death
def US06(ppl,fam):
    for x in ppl['FAMS'] :
    	if(x==fam['ID'] and fam['DIV']!='N/A'and ppl['DEAT']!='N/A'):
    		death=datetime.strptime(ppl['DEAT'], '%d %b %Y')
    		divorce=datetime.strptime(fam['DIV'], '%d %b %Y')
    		if(death<divorce):
    			return False
    	return True

#makes sure age is <150
def US07(age):
	if(age>=150):
		return False
	return True

#makes sure child is born after their parents' marriage and no more than 9 months after divorce
def US08(ppl,fam):
    for x in ppl['FAMC'] :
        if(fam['ID']==x):
            birth=datetime.strptime(ppl['BIRT'], '%d %b %Y')
            married=datetime.strptime(fam['MARR'], '%d %b %Y')
            if(birth<married):
                return -1
            elif(fam['DIV']!='N/A'):
                divorce=datetime.strptime(fam['DIV'], '%d %b %Y')
                if(relativedelta(birth,divorce).years>0 or relativedelta(birth,divorce).months>=9):
                    return 0
    return 1

def US12(fam,listOfPpl):
    return not husb_not_too_old(fam,listOfPpl) or not wife_not_too_old(fam,listOfPpl)

def US13(ppl,siblings):
    sibsBday = {}
    for sib in siblings:
        for indi in ppl:
            if sib == indi['ID']:
                if indi['BIRT'] in sibsBday:
                    sibsBday[indi['BIRT']]+=1
                    if sibsBday[indi['BIRT']] >= 5:
                        return False
                else:
                    sibsBday[indi['BIRT']]=1
    return True

def US14(fam):
    return len(fam['CHIL']) >=15

def US16(individuals, family, families):
    return no_marr_to_desc(individuals, family, families)

def find_age(start, end):
    """Parse strings as date objects and compare them to get age"""
    try:
        start = parser.parse(start)
        end = parser.parse(end)

        return relativedelta(end, start).years
    except ValueError:
        return 'NA'

def husb_marr_after_14(indiv, fam):
    """Checks if husband is older than 14 when married"""
    if not 'MARR' in fam:
        return False

    husb = fam['HUSB']
    return find_age(indiv[husb]['BIRT'], fam['MARR']) >= 14

def wife_marr_after_14(indiv, fam):
    """Checks if wife is older than 14 when married"""
    if not 'MARR' in fam:
        return False

    wife = fam['WIFE']
    return find_age(indiv[wife]['BIRT'], fam['MARR']) >= 14

def date_within_9mo(date1, date2):
    """Checks if date1 comes 9 months within date2"""
    try:
        date1 = parser.parse(date1, dayfirst=True)
        date2 = parser.parse(date2, dayfirst=True)
        return (date1 - date2).days/30.4 > 9
    except ValueError:
        return False

def date_first(date1, date2):
    """Checks if date1 comes before date2"""
    try:
        date1 = parser.parse(date1)
        date2 = parser.parse(date2)

        return (relativedelta(date2, date1).days >= 0 and
                relativedelta(date2, date1).months >= 0 and
                relativedelta(date2, date1).years >= 0)
    except ValueError:
        return False

def no_bigamy(indiv, fams):
    """Checks that individuals were not spouses in multiple families at the same time"""
    if "FAMS" in indiv and len(indiv["FAMS"]) > 1:
        spouse = "HUSB" if indiv["SEX"] == "F" else "WIFE"
        all_marrs = {}

        for fam in indiv["FAMS"]:
            if not "MARR" in fams[fam]:
                pass
            else:
                if "DIV" in fams[fam]:
                    curr_marr = (fams[fam]["MARR"], fams[fam]["DIV"])
                elif "DEAT" in fams[fam][spouse]:
                    curr_marr = (fams[fam]["MARR"], spouse["DEAT"])
                else:
                    curr_marr = (fams[fam]["MARR"], time.strftime("%d %b %Y"))
                all_marrs[fam] = curr_marr

        for fam in indiv["FAMS"]:
            for marr_fam in all_marrs:
                if ((not fam == marr_fam) and ("MARR" in fams[fam]) and date_first(all_marrs[marr_fam][0], fams[fam]["MARR"])
                   and date_first(fams[fam]["MARR"], all_marrs[marr_fam][1])):
                    return (fam, marr_fam)
        return True
    else:
        return True

def husb_not_too_old(fam, indivs):
    """Check if father is too old"""
    if not get_oldest_child_birth(fam, indivs):
        return True
    else:
        husb = fam["HUSB"]
        for i in indivs:
            if i['ID'] == husb:
                b = i['BIRT']
        return find_age(b , get_oldest_child_birth(fam, indivs)) < 80

def wife_not_too_old(fam, indivs):
    """Check if mother is too old"""
    if not get_oldest_child_birth(fam, indivs):
        return True
    else:
        wife = fam["WIFE"]
        for i in indivs:
            if i['ID'] == wife:
                b = i['BIRT']
        return find_age(b , get_oldest_child_birth(fam, indivs)) < 60

def get_oldest_child_birth(fam, indivs):
    """Gets birth date of eldest child or return false"""
    if "CHIL" in fam:
        children = fam["CHIL"]
        oldest_child_birth = ''
        if children == []:
            return False
        for i in indivs:
            if i['ID'] == children[0]:
                oldest_child_birth = i["BIRT"]
        for child in children:
            if child in indivs and date_first(indivs[child]["BIRT"], oldest_child_birth):
                oldest_child_birth = indivs[child]["BIRT"]
        return oldest_child_birth
    else:
        return False

def multiple_births(indiv, fam):
    if not 'CHIL' in fam:
        return True

    children =fam['CHIL']

    for child1 in children:
        i = 0
        for child2 in children:
            if child1 in indiv and child2 in indiv and indiv[child1]['BIRT'] == indiv[child2]['BIRT']:
                i+=1
            if i == 6:
                return False
    return True

def male_last_names(inds, males):
    """Checks male last names, returns appropriate Boolean for if all male last names consistent"""
    lastNames = []
    for male in males:
        lastNames.append(get_last_name(inds, male))
    return len(set(lastNames))==1

def get_last_name(people, individual):
    """Finds last name from Individual dictionary"""
    surname = people[individual]['NAME'].split()
    return surname[1]

def get_males(families, people):
    """Finds all males in family: Husband and any children who have 'SEX' of 'M'"""
    familyMen = [families['HUSB']]
    children = []
    if 'CHIL' in families:
        children = families['CHIL']
        for kid in children:
            if kid in people and people[kid]['SEX'] == 'M':
                familyMen.append(kid)
    return familyMen

def no_marr_to_desc(individuals, family, families):
    """Main function to check children/descendents against Husband/Wife of family"""
    descendents = []
    husband = ''
    wife = ''
    for x in family:
        for y in families:
            if x==y['ID']:
                husband = y['HUSB']
                wife = y['WIFE']
                descendents += get_desc(individuals, y, families)

    if husband in descendents:
        return True
    elif wife in descendents:
        return True
    else:
        return False

def get_desc(individuals, family, allFam):
    """Function finds children within family, calls get_lower_desc if grandchildren found"""
    if 'CHIL' in family:
        children = family['CHIL']
    else:
        children = []

    if children == []:
        return children
    else:
        families = []
        for kid in children:
            if kid in individuals and 'FAMS' in individuals[kid]:
                families.extend(individuals[kid]['FAMS'])
        if families == []:
            return children
        for fam in map(str, families):

            return children + get_lower_desc(fam, allFam)

def get_lower_desc(family, families):
    """Function finds children, called by get_desc when looking for grandchildren/great-grandchildren"""
    desc = []
    if 'CHIL 'in family:
        desc.extend(families[family]['CHIL'])
    return desc

def birth_before_parents_death(indiv, fam):
    """Returns if mother or father died before birth/conception"""
    if not 'MARR' in fam:
        return False

    if not 'CHIL' in fam:
        return True

    return wife_check(indiv, fam['CHIL'], fam) and husb_check(indiv, fam['CHIL'], fam)

def wife_check(indiv, children, fam):
    """Checks if wife died before birth of child"""
    wife = fam['WIFE']
    if not 'DEAT' in indiv[wife]:
        return True

    for child in children:
        if date_first(indiv[wife]['DEAT'], indiv[child]['BIRT']):
            return False

    return True

def husb_check(indiv, children, fam):
    """Checks if husband died before possible conception of child"""
    husb = fam['HUSB']
    if not 'DEAT' in indiv[husb]:
        return True

    for child in children:
        if date_within_9mo(indiv[child]['BIRT'], indiv[husb]['DEAT']):
            return False

    return True

def print_stuff(listOfPpl,listOfFam):

    from prettytable import PrettyTable

    ind_table=PrettyTable();
    fam_table=PrettyTable();

    ind_table.field_names=["ID","Name","Gender","Birthday","Age","Alive","Death","Child","Spouse"]
    fam_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
     #Creates the table of all families
    for fam in listOfFam:
        fam_table.add_row([fam['ID'],fam['MARR'],fam['DIV'],fam['HUSB'], fam['HUSBNAME'], fam['WIFE'], fam['WIFENAME'], fam['CHIL']])

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
    print('\n')

    #US01
    for ppl in listOfPpl:
		for fam in listOfFam:
			if(US01(ppl,fam)==False):
				print "Error US01: Dates of ",ppl['NAME'],"(",ppl['ID'],") occur after current date in Family ",fam['ID'],"."
	#US02
    for ppl in listOfPpl:
		for fam in listOfFam:
			if(US02(ppl,fam)==False):
				print "Error US02: Birth of ",ppl['NAME'],"(",ppl['ID'],") occurs after his/her marriage in Family ",fam['ID'],"."

    for ppl in listOfPpl:
		for fam in listOfFam:
			if(US03(ppl)==False):
				print "Error US03: Birth of ",ppl['NAME'],"(",ppl['ID'],") occurs after his/her death."
    #US04
    for fam in listOfFam:
    	if(US04(fam)==False):
    		print "Error US04: Divorce date occurs before marriage date in Family ",fam['ID'],"."
    #US05
	for ppl in listOfPpl:
		for fam in listOfFam:
			if(US05(ppl,fam)==False):
				print "Error US05: Marriage date of ",ppl['NAME'],"(",ppl['ID'],") occurs after his/her death date in Family ",fam['ID'],"."
	#US06
	for ppl in listOfPpl:
		for fam in listOfFam:
			if(US06(ppl,fam)==False):
				print "Error US06: Divorce date of ",ppl['NAME'],"(",ppl['ID'],") occurs after his/her death date in Family ",fam['ID'],"."
	#US07
	for ppl in listOfPpl:
		if(US07(ppl['AGE'])==False):
			print "Error US07: ",ppl['NAME'],"(",ppl['ID'],") is more than 150 years old"
	#US08
    for ppl in listOfPpl:
        for fam in listOfFam:
            if(US08(ppl,fam)==0):
              print "Error US08: Birth date of ",ppl['NAME'],"(",ppl['ID'],") occurs > 9 months after his/her parents' divorce date in Family ",fam['ID'],"."
            if(US08(ppl,fam)==-1):
              print "Error US08: Birth date of ",ppl['NAME'],"(",ppl['ID'],") occurs before parents' marriage date in Family ",fam['ID'],"."

    #US12
    for fam in listOfFam:
        if US12(fam,listOfPpl):
            print 'Error US12: A mom is 60 yrs older then child or a dad is 80 yrs older then child in Family '+fam['ID']

    #US13
    for fam in listOfFam:
        if len(fam['CHIL']) >=5:
            if(US13(listOfPpl,fam['CHIL'])):
                print "Error US13: 5 siblings with the same birthdate in family "+ fam['ID']

    #US14
    for fam in listOfFam:
        if US14(fam):
            print "Error US14: More then 15 siblings in the family "+ fam['ID']

    #US16
    for ppl in listOfPpl:
        for fam in listOfFam:
            if  US16(ppl,ppl['FAMS'],listOfFam):
                print "Error US15: "+ppl['NAME'],"(",ppl['ID'],")"+ " is married to a descendent"
                break



#readGED takes in the specified GED file from the user
#Opens the GED file and store each indi and fam in a list
#Reads the content of the GED file and writes the output on the answer.txt file
def readGED(fileName,listOfPpl,listOfFam):

    #Opens the file specified by the User
    rfile = open(fileName,'r')
    #Reads each line and places each line in a list
    lines = rfile.readlines()

    saveInfo(listOfPpl,listOfFam,lines)

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
    #list of INDI and Fam
    listOfPpl = []
    listOfFam = []
    readGED(args.file, listOfPpl, listOfFam)

    print_stuff(listOfPpl, listOfFam)



if __name__ == "__main__":
    main()
