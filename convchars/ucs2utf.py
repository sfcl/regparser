#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Конвертер преобразующий строку вида:
43,00,3a,00,5c,00,45,00,47,00,52,00,50,00,4f,00,52,00,41,00,00,00

в 

C:\EGRPORA

"""

import re
from convchars.ctable import convert_table
#from ctable import convert_table

def usc2utf(prep_str, expandsz=False):
    tmp_list = re.split('\,', prep_str)
    result_str = ''
    #группируем элементы массива по 2
    tmp_list2 = []
    count_elems = len(tmp_list)
    inx_list = range(0, count_elems, 2)
    for inx in inx_list:
        tmp_itm = tmp_list[inx:(inx+2)]   
        v1 = tmp_itm[0]
        v2 = tmp_itm[1]
        v21 = v2 + v1 # переставляем элементы местами
        v21 = v21.upper()
        if expandsz:
            one_char = convert_table.get(v21, '')
            one_char = one_char.replace('{break}', '')
        else:
            one_char = convert_table.get(v21, '')
        result_str+=one_char
    
    return result_str
    
if __name__ == '__main__':
    pass