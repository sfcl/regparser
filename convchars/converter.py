#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Преобразует строку вида:

[#]  0023  NUMBER SIGN

в 

{
'0023' : '#',
}


"""

import re

big_list = []

with open('table.txt', 'r', encoding='utf-8') as f:
    for fline in f:
        tmp_list = re.split('\s\s', fline)
        tmp_str = '\'' + tmp_list[1] + '\''
        tmp_str = tmp_str + ' : '
        tmp_str2 = tmp_list[0]
        tmp_str2 = tmp_str2[1:-1]
        tmp_str = tmp_str + '\'' + tmp_str2 + '\',' 
        big_list.append(tmp_str)

with open('ctable.txt', 'w', encoding='utf-8') as f:
    for item in big_list:
        f.write(item + '\n')


