#!/usr/bin/env python
# -*- coding:utf-8 -*-

from glob import glob
from regparser import regparser


files_list = glob('regs/*.reg')

files_list = ['regs/37.reg',]

# конструктору объекта передаём список из имён файлов
reg = regparser(files_list)

print('[Registry]')
reg.innosetup() # печать ключей реестра в формате  InnoSetup

