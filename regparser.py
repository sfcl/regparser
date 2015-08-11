#!/usr/bin/env python
# -*- config:utf-8 -*-
"""
    Класс реализует синтаксический парсер текстовых файлов в формате
    Windows Registry Editor Version 5.00. А также с последующей конвертацией в секцию [Registry] InnoSetup.
    https://en.wikipedia.org/wiki/Windows_Registry
"""

import re
import configparser

class registry_item(object):
    # класс контейнер для хранения одной единицы вложенного элемента реестра
    def __init__(self):
        self.name  = ''
        self.type  = ''
        self.value = ''

class registry_block(object):
    # класс контейнер для хранения вложенного блока реестра
    def __init__(self):
        self.root       = ''
        self.subkey     = ''
        self.list_items = []
            
class regparser(object):
    def __init__(self, fn):
        # fn - список из строк-имён файлов
        self.big_registry_list = []
        self.files_names = fn

        # отключаем ругательство на стартовую строку Windows Registry Editor Version 5.00
        # это хак!
        self.config = configparser.ConfigParser(comment_prefixes = ('#', ';', 'Windows', ))

        # включаем режим правильных регистров букв в именах ключей
        # это тоже хак!
        self.config.optionxform = str
        
        for file_name in self.files_names: 
            self.config.read(file_name, encoding='utf-16',)
            self.blks = self.config.sections()
            # наполняем список big_registry_list данными
            for hive in self.blks:
                regb = registry_block()
                regb.root = self.get_root(self.config[hive].name)
                regb.subkey = self.reg_subkey(self.config[hive].name)
                for itm in self.config[hive]:
                    regi = registry_item()
                    regi.name = itm[1:-1] # убираем кавычки слева и справа 
                    tmp_var = self.config[hive][itm]
                    regi.type = self.get_item_type(tmp_var)
                    regi.value = self.get_item_value(tmp_var)
                    regb.list_items.append(regi)
                
                self.big_registry_list.append(regb)

            # освобождаем память
            regi = ''
            regb = ''

    def prepare_value(self, prepare_string):
        # превращает данные в формат InnoSetup, преобразует данные
        # 43,00,3a,00,5c,00,45,00,47,00,52,00,50,00,4f,00,52,00,41,00,\
        # 5c,00,46,00,4f,00,52,00,4d,00,53,00,36,00,30,00,00,00
        # в формат 
        # 43,00,3a,00,5c,00,45,00,47,00,52,00,50,00,4f,00,52,00,41,00, 5c,00,46,00,4f,00,52,00,4d,00,53,00,36,00,30,00,00,00
        prepare_string = prepare_string.replace('\n', '') # Убираем переводы строк
        prepare_string = prepare_string.replace('\\', '') # Убираем обратные слеши
        return prepare_string
        
    def get_root(self, prepare_string):
        """
        Из строки вида HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\ORACLE\HOME0
        получаем HKLM
        """
        tmp_root = re.split('\\\\', prepare_string)
        tmp_root = tmp_root[0]
        if tmp_root == 'HKEY_LOCAL_MACHINE':
            return 'HKLM'
        
        elif tmp_root == 'HKEY_CURRENT_CONFIG':
            return 'HKCC'
        
        elif tmp_root == 'HKEY_CLASSES_ROOT':
            return 'HKCR'
            
        elif tmp_root == 'HKEY_CURRENT_USER':
            return 'HKCU'
            
        elif tmp_root == 'HKEY_USERS':    
            return 'HKU'
            
    def reg_subkey(self, prepare_string):
        """
        Из строки вида HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\ORACLE\HOME0
        получаем SOFTWARE\Wow6432Node\ORACLE\HOME0
        """
        tmp_subkey = re.split('\\\\', prepare_string)
        tmp_subkey = tmp_subkey[1:]
        return '\\'.join(tmp_subkey)
        
    def get_item_type(self, prepare_string):
        """
        На основе строки формата hex:09,39,40,30,43,48,94,89,32,49
        возвращаем тип binary InnoSetup
        """
        
        tmp_list = re.split(':', prepare_string)
        
        if len(tmp_list) == 1:
            return 'string'
        
        elif len(tmp_list) == 2:
            if tmp_list[0] == 'hex(2)':
                return 'expandsz'
            
            elif tmp_list[0] == 'hex':
                return 'binary'
                
            elif tmp_list[0] == 'dword':
                return 'dword'
                
            elif tmp_list[0] == 'hex(b)':
                return 'qword'
                
            elif tmp_list[0] == 'hex(7)':
                return 'multisz'
            
            else:
                return 'none'
        
    def get_item_value(self, prepare_string):
        """
        На основе строки формата hex:09,39,40,30,43,48,94,89,32,49
        возвращаем 09,39,40,30,43,48,94,89,32,49
        """
        tmp_list = re.split(':', prepare_string)
        if len(tmp_list) == 1:
            return tmp_list[0][1:-1]
        elif len(tmp_list) == 2:
            return tmp_list[1]
    
    def innosetup(self):
        print('[Registry]')
        for hive in self.big_registry_list:
            #print(hive.root, '|', hive.subkey)
            for itms in hive.list_items:
                tmp_str = ''
                tmp_str += 'Root: ' + hive.root + ';'
                tmp_str += ' Subkey: ' + hive.subkey + ';'
                tmp_str += ' ValueType: ' + itms.type + ';'
                tmp_str += ' ValueName: ' + itms.name + ';'
                tmp_str += ' ValueData: ' + itms.value              
                print(tmp_str)
  