#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import unittest
from glob import glob
from regparser import regparser

# self.assertEqual(self.seq, list(range(10)))
# self.assertTrue(element in self.seq)


class SyntaxParserChecker(unittest.TestCase):
    def setUp(self):
        self.files_list = glob('regs/*.reg')
        self.reg = regparser()
        self.reg.read_files_list(self.files_list)
        self.tmp = ''

    def test_get_key_type1(self):
        self.tmp = self.reg.get_item_type('hex:00,00,00,00')
        self.assertEqual(self.tmp, 'hex')
    
    def test_get_key_type2(self):
        self.tmp = self.reg.get_item_type('C:\\EGRPORA\\bin\\ifbld60.exe,-1')
        self.assertEqual(self.tmp, 'string')
        
    
    def test_get_key_type3(self):
        self.tmp = self.reg.get_item_type('C:\\EGRPORA\\bin\\ifbld60.exe,-1')
        self.assertEqual(self.tmp, 'string')
    
    
if __name__ == '__main__':
    unittest.main()
