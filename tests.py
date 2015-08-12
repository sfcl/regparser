#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import unittest
from glob import glob
from regparser import regparser

class SyntaxParserChecker(unittest.TestCase):
    def setUp(self):
        self.files_list = glob('regs/*.reg')
        self.reg = regparser()
        self.reg.read_files_list(self.files_list)
        self.tmp = ''

    def test_get_key_type1(self):
        self.tmp = self.reg.get_item_type('hex:00,00,00,00')
        self.assertEqual(self.tmp, 'binary')
    
    def test_get_key_type2(self):
        self.tmp = self.reg.get_item_type('"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        self.assertEqual(self.tmp, 'string')
        
    def test_get_value1(self):
        self.tmp = self.reg.get_item_value('"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        self.assertEqual(self.tmp, '"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
    
    def test_get_value2(self):
        self.tmp = self.reg.double_characters('"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        self.assertEqual(self.tmp, '"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
    
    def test_get_value3(self):
        self.tmp = self.reg.double_characters('"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        self.assertEqual(self.tmp, '"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        
    def test_get_value4(self):
        self.tmp = self.reg.double_characters(r'"[open(\"%1\")]"')
        self.assertEqual(self.tmp, r'"[open(\""%1\"")]"')
    
    def test_is_path1(self):
        self.tmp = self.reg.is_directory('hex:00,00,00,00')
        self.assertTrue(self.tmp == False)
    
    def test_is_path2(self):
        self.tmp = self.reg.is_directory('"C:\EGRPORA\bin\ifbld60.exe,-1"')
        self.assertTrue(self.tmp)
        
    def test_is_path3(self):
        self.tmp = self.reg.is_directory('"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        self.assertTrue(self.tmp)

    def test_text_proc1_1(self):
        self.tmp = self.reg.text_proc1('3,0,3a,00,5c,00,45,00,47,00,52,00,50', debug=True)
        self.assertEqual(self.tmp, '03 00 3a 00 5c 00 45 00 47 00 52 00 50')
        
    def test_text_proc1_2(self):
        self.tmp = self.reg.text_proc1('0,00,00,0', debug=True)
        self.assertEqual(self.tmp, '00 00 00 00')
        
    def test_text_proc1_3(self):
        self.tmp = self.reg.double_characters('00 00 00 00', debug=True)
        self.assertEqual(self.tmp, '00 00 00 00')
    
if __name__ == '__main__':
    unittest.main()
