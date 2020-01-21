#!/usr/bin/env python

import os
import subprocess

source_locale = 'en-US'
locales_dir = os.fspath('locales')

source_locale_path = os.path.join(locales_dir, source_locale)

locales = list(filter(lambda x: os.path.isdir(os.path.join(locales_dir,x)) and (x != source_locale), os.listdir(locales_dir)))
pots = []

for root,dirs,files in os.walk(source_locale_path):
	pots += list(filter(lambda x : x.endswith('.pot'), (os.path.join(root, name) for name in files)))


for pot in pots:
	for locale in locales:
		target_po = os.path.join(locales_dir, locale, os.path.splitext(os.path.relpath(pot, source_locale_path))[0]+'.po')
		if os.path.isfile(target_po):
			print('Updating '+target_po+' from "'+pot+':')
			subprocess.call(['msgmerge', '--update', '--backup=none', '--no-wrap', '--width=200', target_po, pot])
		else:
			print('Creating '+target_po+' from "'+pot+':')
			target_po_tmp = target_po+'.tmp'
			os.makedirs(os.path.split(target_po)[0],exist_ok=True)
			subprocess.call(['msginit', '--input='+pot, '--locale='+locale+'.utf-8', '--output='+target_po_tmp])
			target_po_file = open(target_po, 'wb')
			subprocess.call(['msgconv', '--to-code=utf-8', target_po_tmp], stdout=target_po_file)
			target_po_file.close()
			os.remove(target_po_tmp)

