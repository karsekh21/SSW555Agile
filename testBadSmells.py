#!usr/bin/python


#Calvin Han
#CS 555
#Homework 4
#I pledge my honor that I have abided by the stevens honor system


import unittest
from GedReader import *


class TestBadSmells(unittest.TestCase):
    def test_SameDate(self):
        self.assertTrue(checkDeatBeforeBirt('1 DEC 2018','1 DEC 2018'))

if __name__ == '__main__':
    unittest.main()
