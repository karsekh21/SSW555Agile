import os
import re
import gzip
import argparse
import csv
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class utilities_US:
    #Makes sure that person's dates are before current date
    def US01(ppl,fam):
        if(ppl['FAMS']==fam['ID']):
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
        if(ppl['FAMC']==fam['ID']):
            birth = datetime.strptime(ppl['BIRT'],'%d %b %Y')
            death=datetime.today()
            current=datetime.today()
            if(ppl['ALIVE']==False):
                death = datetime.strptime(ppl['DEAT'],'%d %b %Y')
            if(birth>current or death>current):
                return False
        return True;

    #makes sure that birth comes before marriage
    def US02(ppl,fam):
        if(ppl['FAMS']==fam['ID']):
            marriage=datetime.strptime(fam['MARR'],'%d %b %Y')
            birth = datetime.strptime(ppl['BIRT'],'%d %b %Y')
            if(marriage<birth):
                return False
        return True

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
            if(fam['ID']==ppl['FAMS']):
                death=datetime.strptime(ppl['DEAT'], '%d %b %Y')
                married=datetime.strptime(fam['MARR'], '%d %b %Y')
                if(death<married):
                    return False
        return True;

    #makes sure that divorce occurs before death
    def US06(ppl,fam):
        if(ppl['FAMS']==fam['ID'] and fam['DIV']!='N/A'and ppl['DEAT']!='N/A'):
            death=datetime.strptime(ppl['DEAT'], '%d %b %Y')
            divorce=datetime.strptime(fam['DIV'], '%d %b %Y')
            if(death<divorce):
                return False
        return True;

    #makes sure age is <150
    def US07(age):
        if(age>=150):
            return False
        return True

    #makes sure child is born after their parents' marriage and no more than 9 months after divorce
    def US08(ppl,fam):
        if(fam['ID']==ppl['FAMC']):
            birth=datetime.strptime(ppl['BIRT'], '%d %b %Y')
            married=datetime.strptime(fam['MARR'], '%d %b %Y')
            if(birth<married):
                return -1
            elif(fam['DIV']!='N/A'):
                divorce=datetime.strptime(fam['DIV'], '%d %b %Y')
                if(relativedelta(birth,divorce).years>0 or relativedelta(birth,divorce).months>=9):
                    return 0



    def US13(ppl,siblings):
        sibsBday = {}
        for sib in siblings:
            for indi in ppl:
                if sib == indi['ID']:
                    if indi['BIRT'] in sibsBday:
                        sibsBday[indi['BIRT']]+=1
                        if sibsBday[indi['BIRT']] == 5:
                            return False
                    else:
                        sibsBday[indi['BIRT']]=1
        return True

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
            return find_age(indivs[husb]["BIRT"], get_oldest_child_birth(fam, indivs)) < 80

    def wife_not_too_old(fam, indivs):
        """Check if mother is too old"""
        if not get_oldest_child_birth(fam, indivs):
            return True
        else:
            wife = fam["WIFE"]
            return find_age(indivs[wife]["BIRT"], get_oldest_child_birth(fam, indivs)) < 60

    def get_oldest_child_birth(fam, indivs):
        """Gets birth date of eldest child or return false"""
        if "CHIL" in fam:
            children = fam["CHIL"]
            oldest_child_birth = indivs[children[0]]["BIRT"]
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

    def fewer_than_15_siblings(fam):
        if 'CHIL' in fam:
            return len(fam['CHIL']) < 15
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
        husband = family['HUSB']
        wife = family['WIFE']
        descendents = get_desc(individuals, family, families)

        print family
        print descendents
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
