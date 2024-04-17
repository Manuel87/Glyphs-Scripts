#MenuTitle: Apply current kerning across dots-ar
# -*- coding: utf-8 -*-
"""ALPHA: needs special json file ... can be copied from glyphs file directly and then converted using text edits in sublime"""
#plain casual python script needs the JSON file in the same folder

import json, ast
from pprint import pprint

path = "example_kerning-ar.json"
##or use temp folder currently only Osx ->  (before ~/myterminaltemp/)
#osx_dir = str(call("echo $TMPDIR", shell=True));
#path = osx_dir + "kerning.json"

with open(path) as json_file:
	jsonObj = json.load(json_file)
	#pprint(jsonObj)

opentypestring_before = "";
opentypestring = ""
dotglyphs = " @Dots "
#[threedots-ar.ss13 dotabove-ar.ss13 dotbelow-ar.ss13 dotcenter-ar.ss13 twodotshorizontalabove-ar.ss13 twodotshorizontalbelow-ar.ss13 threedotsupabove-ar.ss13]

leftside = {}
value = 0
rightside = {}
for leftside in jsonObj:
	opentypestring_before += "pos " + leftside
	for rightside in jsonObj[leftside]:
		value = jsonObj[leftside][rightside]
		opentypestring += opentypestring_before + "' " + str(value) + dotglyphs + rightside + ";\n" #jsonObj[str(leftside)][str(rightside)]
		#	print value
	opentypestring_before = ""

#opentype output
print opentypestring

# print jsonObj["@MMK_L_Y"]["@MMK_R_b"]
# print jsonObj[leftside][rightside]
# print jsonObj[leftside][rightside]
#print jsonObj["@MMK_L_A"]["@MMK_R_a"]
