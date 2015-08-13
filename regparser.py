#!/usr/bin/env python
# -*- config:utf-8 -*-
"""
    Класс реализует синтаксический парсер текстовых файлов в формате
    Windows Registry Editor Version 5.00. А также с последующей конвертацией в секцию [Registry] InnoSetup.
    https://en.wikipedia.org/wiki/Windows_Registry
"""

import re
import sys
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
    def __init__(self):
        # fn - список из строк-имён файлов
        self.big_registry_list = []
        self.files_names = []

        # отключаем ругательство на стартовую строку Windows Registry Editor Version 5.00
        # это хак!
        self.config = configparser.RawConfigParser(comment_prefixes = ('#', ';', 'Windows', ))

        # включаем режим правильных регистров букв в именах ключей
        # это тоже хак!
        self.config.optionxform = str
        
        # инициализируем пустые атрибуты для последующего доступа к ним из методов
        self.last_type = ''
        
        
    def read_files_list(self,  fns):
        """
        Обработка файлов по списку
        """
        self.files_names = fns
        for file_name in self.files_names: 
            self.config.read(file_name, encoding='utf-16',)
            self.blks = self.config.sections()
            # наполняем список big_registry_list данными
            for hive in self.blks:
                self.regb = registry_block()
                self.regb.root = self.get_root(self.config[hive].name)
                self.regb.subkey = self.reg_subkey(self.config[hive].name)
                for itm in self.config[hive]:
                    self.regi = registry_item()
                    self.regi.name = itm[1:-1] # убираем кавычки слева и справа 
                    tmp_var = self.config[hive][itm]
                    self.regi.type = self.get_item_type(tmp_var)
                    self.last_type = self.get_item_type(tmp_var)
                    tmp_str = self.get_item_value(tmp_var)
                    tmp_str = self.text_proc1(tmp_str)
                    tmp_str = self.double_characters(tmp_str)
                    self.regi.value = tmp_str
                    self.regb.list_items.append(self.regi)
                
                self.big_registry_list.append(self.regb)

            
    def text_proc1(self, prepare_string, debug=False):
        """
        Преобразуем значение ключа реестра типа binar из формата 
        "0,00,00"  в формат "00 00 00"
        """
        if debug or self.regi.type == 'binary':
            tmp_list = re.split(',', prepare_string)
            count_elems = len(tmp_list)
            for elem in range(count_elems):
                if len(tmp_list[elem]) == 1:
                    tmp_list[elem] = '0' + tmp_list[elem]
             
            prepare_string = ' '.join(tmp_list)
            return prepare_string
        else:
            return prepare_string
        
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
        
        tmp_str = '\\'.join(tmp_subkey) 
        
        tmp_str = '"' + tmp_str + '"' # опять хак!
        tmp_str = self.double_characters2(tmp_str)
        return tmp_str
        
    def get_item_type(self, prepare_string):
        """
        На основе строки формата hex:09,39,40,30,43,48,94,89,32,49
        возвращаем тип binary InnoSetup
        """
        if self.is_directory(prepare_string):
            return 'string'
        
        tmp_list = re.split(':', prepare_string)
        
        if len(tmp_list) == 1:
            return 'string'
        
        elif len(tmp_list) >= 2:
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
            
            return 'string'
        
    def get_item_value(self, prepare_string):
        """
        На основе строки форамата hex:09,39,40,30,43,48,94,89,32,49
        возвращаем 09,39,40,30,43,48,94,89,32,49
        """
        if self.is_directory(prepare_string):
            # заменяем \\ на \
            # prepare_string = re.sub(r'\\', r'\', prepare_string)
            prepare_string = prepare_string.replace('\\\\','\\')
            return prepare_string
            
        tmp_list = re.split(':', prepare_string)
        if len(tmp_list) == 1:
            #tmp_str = tmp_list[0][1:-1] # убираем окружающие двойные кавычники 
            return tmp_list[0]
        elif len(tmp_list) == 2:
            tmp_str = self.prepare_value(tmp_list[1])
            #tmp_str = self.double_characters(tmp_str)
            return tmp_str
            
    def is_directory(self, prepare_string):
        """
        Проверка является ли строка кайловым каталогом 
        """
        old_re = r'^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))'
        new_re = r'^(?:[\w]\:|\\)(\\[a-z_\-\s0-9\.]+)+\.(txt|gif|pdf|doc|docx|xls|xlsx)$'
        new_re = r'^["]?[A-Z]:\\.*$'
        if re.match(new_re, prepare_string):
            # https://techtavern.wordpress.com/2009/04/06/regex-that-matches-path-filename-and-extension/
            # если найден файловый путь, с ним работаем по особому
            return True
        else:
            return False
    
    def double_characters(self, prepare_string, debug=False, type='binary'):
        """
        Замена строки {289D6FA0-2A7D-11CF-AD05-0020AF0BA9E2} на строку
        {{289D6FA0-2A7D-11CF-AD05-0020AF0BA9E2}}
        """
        if not(prepare_string):
            return ''
        
        if debug or self.last_type == 'binary':
            prepare_string = '"' + prepare_string + '"'
            return prepare_string
            
        prepare_string = prepare_string[1:-1]
        # выполняем условие если внутри строки есть двойные кавычки
        if re.search('"', prepare_string):
            prepare_string = re.sub(r'"', r'""', prepare_string)
        
        prepare_string = re.sub(r'{', r'{{', prepare_string)
        prepare_string = re.sub(r'}', r'}}', prepare_string)
            
        prepare_string = '"' + prepare_string + '"'    
        
        return prepare_string
        
    def double_characters2(self, prepare_string, debug=False, type='binary'):
        """
        Замена строки {289D6FA0-2A7D-11CF-AD05-0020AF0BA9E2} на строку
        {{289D6FA0-2A7D-11CF-AD05-0020AF0BA9E2}}
        """
        
        prepare_string = re.sub(r'{', r'{{', prepare_string)
        prepare_string = re.sub(r'}', r'}}', prepare_string)
        
        return prepare_string

    def innosetup(self):
        #print('[Registry]')
        for hive in self.big_registry_list:
            #print(hive.root, '|', hive.subkey)
            for itms in hive.list_items:
                try:
                    tmp_str = ''
                    tmp_str += 'Root: ' + hive.root + ';'
                    tmp_str += ' Subkey: ' + hive.subkey + ';'
                    tmp_str += ' ValueType: ' + itms.type + ';'
                    tmp_str += ' ValueName: ' + itms.name + ';'
                    tmp_str += ' ValueData: ' + itms.value              
                    print(tmp_str)
                except TypeError:
                    print('OOOOOOOOOx')
                    
                    #sys.exit(1)
                    