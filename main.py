#!/usr/bin/env python
# -*- coding:utf-8 -*-

from glob import glob
from regparser import regparser


files_list = glob('regs_32/*.reg')
#files_list = ['37.reg',]


reg = regparser()
reg.read_files_list(files_list)

print('[Registry]')
reg.innosetup() # печать ключей реестра в формате  InnoSetup
