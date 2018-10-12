import unittest

from GedReader import US01, US02, US03, US04, US05, US06, US07, US08
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
		self.assertEqual(US05({'FAMS':'F1', 'DEAT':'2 DEC 2010'},{'ID':'F1','MARR':'4 OCT 2005'}),True)
	def test_US06(self):
		self.assertEqual(US06({'FAMS':['F1'], 'DEAT':'2 DEC 2005'},{'ID':'F1','DIV':'4 OCT 2010'}),False)
	def test_US07(self):
		self.assertEqual(US07(149),True)
	def test_US08(self):
		self.assertEqual(US08({'FAMC':['F1'], 'BIRT':'2 DEC 2002'},{'ID':'F1','MARR':'4 OCT 2005','DIV':'5 DEC 2006'}),-1)



#randIndi = {'ID':'N/A','NAME':'N/A','SEX':'N/A','AGE':'N/A','BIRT':'N/A','DEAT':'N/A','FAMC':list(),'FAMS':list(),'ALIVE':True}
#randFam = {'ID':'N/A','MARR':'N/A','DIV':'N/A','HUSB':'N/A','HUSBNAME':'N/A','WIFE':'N/A','WIFENAME':'N/A','CHIL':list()}

if __name__ == '__main__':
	unittest.main()