#!/usr/bin/env python
# -*- coding:utf-8 -*-

from regparser import regparser

# конструктору объекта передаём список из имён файлов, которые нужно конвертировать

reg = regparser(['22.reg',])

reg.innosetup() # печать ключей реестра в формате  InnoSetup

