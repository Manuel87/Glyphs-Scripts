#MenuTitle: Apply current kerning across spaces
# -*- coding: utf-8 -*-
"""ALPHA: needs special json file .. I check..."""
#plain casual python script needs the JSON file in the same folder

import json, ast
from pprint import pprint

path = "example_kerning.json"
##or use temp folder currently only Osx ->  (before ~/myterminaltemp/)
#osx_dir = str(call("echo $TMPDIR", shell=True));
#path = osx_dir + "kerning.json"

with open(path) as json_file:
	jsonObj = json.load(json_file)
	#pprint(jsonObj)

opentypestring_before = "";
opentypestring = ""

leftside = {}
value = 0
rightside = {}
for leftside in jsonObj:
	opentypestring_before += "pos " + leftside
	for rightside in jsonObj[leftside]:
		value = jsonObj[leftside][rightside]
		opentypestring += opentypestring_before + "' " + str(value) + " space " + rightside + ";\n" #jsonObj[str(leftside)][str(rightside)]
		#	print value
	opentypestring_before = ""

#opentype output
print(opentypestring)

# print jsonObj["@MMK_L_Y"]["@MMK_R_b"]
# print jsonObj[leftside][rightside]
# print jsonObj[leftside][rightside]
#print jsonObj["@MMK_L_A"]["@MMK_R_a"]
