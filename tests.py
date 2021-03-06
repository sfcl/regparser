#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import unittest
from glob import glob
from regparser import regparser
from convchars.ucs2utf import usc2utf

class SyntaxParserChecker(unittest.TestCase):
    def setUp(self):
        self.files_list = glob('regs/*.reg')
        self.reg = regparser()
        self.reg.read_files_list(self.files_list)
        self.tmp = ''

    def test_root1(self):
        self.tmp = self.reg.get_root('HKEY_LOCAL_MACHINE')
        self.assertEqual(self.tmp, 'HKLM')
        
        
    def test_get_subkey1(self):
        self.tmp = self.reg.reg_subkey(r'HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\ORACLE\\HOME0')
        self.assertEqual(self.tmp, r'SOFTWARE\Wow6432Node\ORACLE\HOME0')
    
    def test_get_subkey2(self):
        self.reg.read_from_files = False
        self.tmp = self.reg.reg_subkey(r'HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\ORACLE\HOME0')
        self.assertEqual(self.tmp, r'SOFTWARE\Wow6432Node\ORACLE\HOME0')
        
    def test_get_key_type1(self):
        self.tmp = self.reg.get_item_type('hex:00,00,00,00')
        self.assertEqual(self.tmp, 'binary')
    
    def test_get_key_type2(self):
        self.tmp = self.reg.get_item_type('"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        self.assertEqual(self.tmp, 'string')
        
    def test_get_value1(self):
        self.tmp = self.reg.get_item_value('"C:\\EGRPORA\\bin\\ifbld60.exe,-1"')
        self.assertEqual(self.tmp, 'C:\\EGRPORA\\bin\\ifbld60.exe,-1')
    
    def test_get_value2(self):
        self.tmp = self.reg.double_characters('C:\\EGRPORA\\bin\\ifbld60.exe,-1')
        self.assertEqual(self.tmp, 'C:\\EGRPORA\\bin\\ifbld60.exe,-1')
    
    def test_get_value3(self):
        self.tmp = self.reg.double_characters('C:\\EGRPORA\\bin\\ifbld60.exe,-1')
        self.assertEqual(self.tmp, 'C:\\EGRPORA\\bin\\ifbld60.exe,-1')
        
    def test_get_value4(self):
        self.tmp = self.reg.double_characters(r'[open(\"%1\")]')
        self.assertEqual(self.tmp, r'[open(\""%1\"")]')
    
    def test_get_value5(self):
        self.reg.last_type = 'qword'
        self.tmp = self.reg.get_item_value(r'hex(b):43,ff,05,49,50,49,00,00')
        self.assertEqual(self.tmp, r'$49504905ff43')
    
    def test_get_value6(self):
        self.reg.last_type = 'multisz'
        self.tmp = self.reg.get_item_value(r'hex(7):31,00,31,00,31,00,31,00,00,00,32,00,32,00,32,00,32,00,00,00,33,\
  00,33,00,33,00,33,00,00,00,00,00')
        self.assertEqual(self.tmp, r'1111{break}2222{break}3333{break}{break}')
    
    
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
        self.tmp = self.reg.append_first_zero('3,0,3a,00,5c,00,45,00,47,00,52,00,50', debug=True)
        self.assertEqual(self.tmp, '03 00 3a 00 5c 00 45 00 47 00 52 00 50')
        
    def test_text_proc1_2(self):
        self.tmp = self.reg.append_first_zero('0,00,00,0', debug=True)
        self.assertEqual(self.tmp, '00 00 00 00')
        
    def test_text_proc1_3(self):
        self.tmp = self.reg.double_characters('00 00 00 00', debug=True)
        self.assertEqual(self.tmp, '00 00 00 00')
        
    def test_ucs_1(self):
        self.tmp = usc2utf('43,00,3a,00,5c,00,45,00,47,00,52,00,50,00,4f,00,52,00,41,00,00,00')
        self.assertEqual(self.tmp, 'C:\EGRPORA{break}')
    
    
    def test_ucs_2(self):
        self.tmp = usc2utf('31,00,31,00,31,00,31,00,00,00,32,00,32,00,32,00,32,00,00,00,33,00,33,00,33,00,33,00,00,00,00,00')
        self.assertEqual(self.tmp, '1111{break}2222{break}3333{break}{break}')
        
if __name__ == '__main__':
    unittest.main()
