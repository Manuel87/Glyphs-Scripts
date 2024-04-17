#MenuTitle: Default Smart Component Settings
# -*- coding: utf-8 -*-
__doc__="""
Resets/Updates Smart Component Settings to my Defaults using Layers starting with "_"
"""
searchTerm = "_" # includes Layers starting with this string
Min = 0
Max = 100

# Currently only works if you first set one property manually :/ > then execute the script
#
# -----------------------
ResetEachTime = True #if true renaming your layers can lead to that you need to readjust your settings in all glyphs which use this smart component
#if not True It wont update the Property name and only adds new ones and well this can lead to crashes apparently! # need to rewrite the code to get rid of this Thing so it checks names, ...

# ToDo -> Have One Dict with all nessessary informations as "name, propertyID/Arraynumber, layerID, min, max,..." and update or use it accordingly to set Layername/Propertyname... ->

#ToDo - Restrucutre in the following order:
# smartglyph? > already property? -> are layers assigned? -> does propertyname and layername match? -> if not update propertyname -> if no property assigned, create property


# -----------------------
import GlyphsApp
from Foundation import NSApplication

Font = Glyphs.font
thisMaster = Glyphs.font.selectedFontMaster
masterID = thisMaster.id
Doc = Glyphs.currentDocument
selectedLayers = Font.selectedLayers


print ""
print "Updating SmartComponent Default Root Settings"
print "---------------------------------------------"

def SetSmartSettingsInGlyph(smartGlyph, LayerNames, Min, Max, reset=False):
	partsSettings = None #smartGlyph.smartComponentAxes() #.partsSettings()
	print "partsSettings", partsSettings
	initSetting = False
	partsettingsNames = []

	print "//Debug// type(Glyph.partsSettings()) = ", type(partsSettings)

	#if there is something, either delete or update
	if partsSettings:
		for j in range(len(partsSettings)) :
			if reset: #delete all settings
				del partsSettings[0]
			else: #update all settings
				partsSettings[j].bottomValue = Min
				partsSettings[j].topValue = Max
				partsettingsNames += [partsSettings[j].name]
		else:
			initSetting = True
	else:
		initSetting = False
		reset = True

		print "!!!!! ERROR: No PartsSettings-Object found. Can not append a Property/GSSmartComponentAxis... Would like to but how the heck do I create one?"
		print "type(partsSetting) has to be <objective-c class __NSArrayM at 0x7fff74b275c8>"
		print ""
		#test smartGlyph.smartComponentAxis()
		#print test
		# partsSettings = []
		# partsSettings.append(GSSmartComponentAxis())
		# print partsSettings



	#recreate all Settings form Layernames
	if initSetting or reset:
		for name in LayerNames:
			tempSmartSetting = GSSmartComponentAxis()
			tempSmartSetting.name = name
			tempSmartSetting.bottomValue = Min
			tempSmartSetting.topValue = Max
			smartGlyph.smartComponentAxes.append(tempSmartSetting)
			#partsSettings.append(tempSmartSetting)
		print "- setting (re)created"



	#print partsSettings

def setPoleMapping(layer, SmartLayerNames, Min, Max):
	for SmartLayerName in SmartLayerNames:
		if layer.name == SmartLayerName:
			layer.smartComponentPoleMapping[SmartLayerName] = Max
		else:
			layer.smartComponentPoleMapping[SmartLayerName] = Min


def process( thisGlyph ):
	numberOfLayers = len( thisGlyph.layers )
	SmartLayerNames = []



	# Get Layer Names
	for thisLayer in thisGlyph.layers:
		# only in this Master
		if thisLayer.associatedMasterId == masterID:
			#setPoleMapping(thisLayer, SmartLayerNames, 0, 0) # reset
			##All Layers within this Master, except the Main Master Layer itself
			if thisLayer.layerId != thisLayer.associatedMasterId:
				if thisLayer.name.startswith(searchTerm):
					SmartLayerNames += [thisLayer.name]

	# Init/Update Setting
	if len(SmartLayerNames):
		print "Smart Layers:", ", ".join(SmartLayerNames)
		print ""
		print "ResetEachTime:", ResetEachTime, "(if False its still a bit buggy)"
		print ""
		SetSmartSettingsInGlyph(thisGlyph, SmartLayerNames, Min, Max, ResetEachTime)
	else:
		print ""
		print "nothing to process"
		print ""
		print "Either no SmartComponent (_parts.glyphname) or no SmartLayers found"
		print "(only layers with '_' are included. eg. '_WiderLayerXY' )"


	#Apply smartComponentPoleMapping
	if len(SmartLayerNames):
		for thisLayer in thisGlyph.layers:
			if thisLayer.associatedMasterId == masterID: #only in this Master
				if thisLayer.layerId == thisLayer.associatedMasterId:
					setPoleMapping(thisLayer, SmartLayerNames, 1, 1) #1 is Min / 2Max
				else: #All Layers within this Master
					if thisLayer.name.startswith(searchTerm):
						setPoleMapping(thisLayer, SmartLayerNames, 1, 2)
					#if thisLayerName.startswith(searc

		print "- mapping updated"


Font.disableUpdateInterface()


for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent

	thisGlyph.beginUndo()
	print "Glyphname:", thisGlyph.name
	process( thisGlyph )

	print "Do not create more then 12 Smart Component Layers.. as apparently Glyphs cant handle more thant that currently"
	thisGlyph.endUndo()


#SetSmartSettingsInGlyph("_part.s", 0, 100)
print ""

