import unittest

from GedReader import US01, US02, US03, US04, US05, US06, US07, US08, US09, US12,US14,US15,US16,US17,US18,US23,US24,US25
from datetime import datetime, date

class TestUserStories(unittest.TestCase):
    def test_US01(self):
		self.assertEqual(US01({'BIRT':'2 DEC 1980','DEAT':'10 OCT 2018', 'FAMS':['F1'], 'FAMC':[], 'ALIVE':False},{'ID':'F1','MARR':'4 OCT 2005','DIV':'5 DEC 2006'}),True)
    def test_US02(self):
		self.assertEqual(US02({'FAMS':['F1'], 'BIRT':'2 DEC 1990'},{'ID':'F1','MARR':'4 OCT 2010'}),True)
    def test_US03(self):
		self.assertEqual(US03({'BIRT':'23 OCT 1999','DEAT':'20 SEP 1995', 'ALIVE':False}),False)
    def test_US04(self):
		self.assertEqual(US04({'DIV':'23 OCT 2000','MARR':'27 NOV 1995'}),True)
    def test_US05(self):
		self.assertEqual(US05({'FAMS':['F1'], 'DEAT':'2 DEC 2010'},{'ID':'F1','MARR':'4 OCT 2005'}),True)
    def test_US06(self):
		self.assertEqual(US06({'FAMS':['F1'], 'DEAT':'2 DEC 2005'},{'ID':'F1','DIV':'4 OCT 2010'}),False)
    def test_US07(self):
		self.assertEqual(US07(149),True)
    def test_US08(self):
		self.assertEqual(US08({'FAMC':['F1'], 'BIRT':'2 DEC 2002'},{'ID':'F1','MARR':'4 OCT 2005','DIV':'5 DEC 2006'}),-1)
    def test_US09(self):
        self.assertEqual(US08({'FAMC':['F1'], 'BIRT':'2 DEC 2002'},{'ID':'F1','MARR':'4 OCT 2005','DIV':'5 DEC 2006'}),-1)
    def test_US10(self):
        self.assertEqual(US08({'FAMC':['F1'], 'BIRT':'2 DEC 2002'},{'ID':'F1','MARR':'4 OCT 2005','DIV':'5 DEC 2006'}),-1)
    def test_US12(self):
        listOfPpl=[]
        joe = {'BIRT': '15 JUL 1600', 'FAMS': 'F23', 'NAME': 'Joe /Smith/', 'ALIVE': False, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I01', 'DEAT': '31 DEC 1900', 'SEX': 'M'}
        jane = {'BIRT': '23 SEP 1900', 'FAMS': 'N/A', 'NAME': 'Jane /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'F23': 'N/A', 'ID': 'I19', 'DEAT': 'N/A', 'SEX': 'F'}
        jen = {'BIRT': '23 SEP 1900', 'FAMS': 'F23', 'NAME': 'Jennifer /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I07', 'DEAT': 'N/A', 'SEX': 'F'}
        jon = {'BIRT': '23 SEP 1900', 'FAMS': 'F23', 'NAME': 'Jon /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I26', 'DEAT': 'N/A', 'SEX': 'F'}
        listOfPpl.append(joe)
        listOfPpl.append(jane)
        listOfPpl.append(jen)
        listOfPpl.append(jon)
        fam = {'HUSBNAME': 'Joe /Smith/', 'CHIL': ['I19', 'I26'], 'MARR': '14 FEB 2001', 'WIFE': 'I07', 'DIV': '14 FEB 2000', 'HUSB': 'I01', 'ID': 'F23', 'WIFENAME': 'Jennifer /Smith/'}
    	self.assertEqual(US12(fam,listOfPpl),True)
    def test_US13(self):
        listOfPpl = []
        jen = {'BIRT': '23 SEP 1900', 'FAMS': 'F23', 'NAME': 'Jennifer /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I1', 'DEAT': 'N/A', 'SEX': 'F'}
        listOfPpl.append(jen)
        jen = {'BIRT': '23 SEP 1900', 'FAMS': 'F23', 'NAME': 'Jennifer /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I2', 'DEAT': 'N/A', 'SEX': 'F'}
        listOfPpl.append(jen)
        jen = {'BIRT': '23 SEP 1900', 'FAMS': 'F23', 'NAME': 'Jennifer /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I3', 'DEAT': 'N/A', 'SEX': 'F'}
        listOfPpl.append(jen)
        jen = {'BIRT': '23 SEP 1900', 'FAMS': 'F23', 'NAME': 'Jennifer /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I4', 'DEAT': 'N/A', 'SEX': 'F'}
        listOfPpl.append(jen)
        jen = {'BIRT': '23 SEP 1900', 'FAMS': 'F23', 'NAME': 'Jennifer /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I5', 'DEAT': 'N/A', 'SEX': 'F'}
        listOfPpl.append(jen)
        self.assertEqual(US13(listOfPpl,['I1','I2','I3','I4','I5']),False)
    def test_US14(self):
        x = 0
        listofChildren = []
        while x<15 :
            listofChildren.append(x)
            x+=1

        fam = {'CHIL':listofChildren}
        self.assertEqual(US14(fam),True)
    def test_US15(self):
        self.assertEqual(US08({'FAMC':['F1'], 'BIRT':'2 DEC 2002'},{'ID':'F1','MARR':'4 OCT 2005','DIV':'5 DEC 2006'}),-1)
    def test_US16(self):
        listOfPpl=[]
        listOfFam=[]
        joe = {'BIRT': '15 JUL 1600', 'FAMS': ['F23','F100'], 'NAME': 'Joe /Smith/', 'ALIVE': False, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I01', 'DEAT': '31 DEC 1900', 'SEX': 'M'}
        jane = {'BIRT': '23 SEP 1900', 'FAMS': [], 'NAME': 'Jane /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'F23': 'N/A', 'ID': 'I19', 'DEAT': 'N/A', 'SEX': 'F'}
        jen = {'BIRT': '23 SEP 1900', 'FAMS': ['F23','F100'], 'NAME': 'Jennifer /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I07', 'DEAT': 'N/A', 'SEX': 'F'}
        jon = {'BIRT': '23 SEP 1900', 'FAMS': ['F23'], 'NAME': 'Jon /Smith/', 'ALIVE': True, 'AGE': 'N/A', 'FAMC': 'N/A', 'ID': 'I26', 'DEAT': 'N/A', 'SEX': 'F'}
        listOfPpl.append(joe)
        listOfPpl.append(jane)
        listOfPpl.append(jen)
        listOfPpl.append(jon)
        fam = {'HUSBNAME': 'Joe /Smith/', 'CHIL': ['I19', 'I26'], 'MARR': '14 FEB 2001', 'WIFE': 'I07', 'DIV': '14 FEB 2000', 'HUSB': 'I01', 'ID': 'F23', 'WIFENAME': 'Jennifer /Smith/'}
        listOfFam.append(fam)
        fam = {'HUSBNAME': 'Joe /Smith/', 'CHIL': [], 'MARR': '14 FEB 2001', 'WIFE': 'I19', 'DIV': '14 FEB 2000', 'HUSB': 'I01', 'ID': 'F100', 'WIFENAME': 'Jane /Smith/'}
        listOfFam.append(fam)

        self.assertEqual(US16(joe,'F100',listOfFam),False)
    def test_US18(self):
        self.assertEqual(US18({'ID':'I1','FAMS':['F1'], 'FAMC':['F2']},[{'ID':'I2', 'FAMS':['F1'], 'FAMC':['F2']}]),False)
    def test_US21(self):
        self.assertEqual(US21({'ID':'I1', 'NAME':'Matt','BIRT':'2 DEC 2005','SEX':'F'},[{'ID':'I2', 'NAME':'Matt','BIRT':'2 DEC 2005'}]),False)
    def test_US22(self):
        self.assertEqual(US22({'ID':'I1', 'NAME':'Matt','BIRT':'2 DEC 2005','SEX':'M'},[{'ID':'I2', 'NAME':'Matt','BIRT':'2 DEC 2005'}]),False)
    def test_US23(self):
        self.assertEqual(US23({'ID':'I1', 'NAME':'Matt','BIRT':'2 DEC 2005'},[{'ID':'I2', 'NAME':'Matt','BIRT':'2 DEC 2005'}]),False)
    def test_US24(self):
        self.assertEqual(US24({'ID': 'F1', 'HUSBNAME':'Todd', 'WIFENAME':'Dorine', 'MARR':'7 FEB 1983'},[{'ID': 'F2', 'HUSBNAME':'Todd', 'WIFENAME':'Dorine', 'MARR':'7 FEB 1983'}]),False)
    def test_US25(self):
        self.assertEqual(US25({'ID':'I1', 'NAME':'Matt','BIRT':'2 DEC 2005', 'FAMC':['F1']},[{'ID':'I2', 'NAME':'Matt','BIRT':'2 DEC 2005', 'FAMC':['F1']}]),False)







#randIndi = {'ID':'N/A','NAME':'N/A','SEX':'N/A','AGE':'N/A','BIRT':'N/A','DEAT':'N/A','FAMC':list(),'FAMS':list(),'ALIVE':True}
#randFam = {'ID':'N/A','MARR':'N/A','DIV':'N/A','HUSB':'N/A','HUSBNAME':'N/A','WIFE':'N/A','WIFENAME':'N/A','CHIL':list()}

if __name__ == '__main__':
	unittest.main()
