#!usr/bin/python


#Calvin Han
#CS 555
#Homework 4
#I pledge my honor that I have abided by the stevens honor system


import unittest
from GedReader import *


class TestDeatBeforeBirt(unittest.TestCase):
    def test_SameDate(self):
        self.assertTrue(checkDeatBeforeBirt('1 DEC 2018','1 DEC 2018'))

    def test_BirtBeforeDeat(self):
        self.assertTrue(checkDeatBeforeBirt('1 DEC 2018','4 DEC 2019'))

    def test_DeatBeforeBirth(self):
        self.assertFalse(checkDeatBeforeBirt('4 DEC 2019','1 DEC 2018'))

    def test_NoBirth(self):
        self.assertFalse(checkDeatBeforeBirt('N/A','1 DEC 2018'))

    def test_NoDeat(self):
        self.assertTrue(checkDeatBeforeBirt('1 Dec 2018','N/A'))

if __name__ == '__main__':
    unittest.main()
