#MenuTitle: Clean up Layers / Delete all unnecessary Layers in Selected Glyphs across Masters
# -*- coding: utf-8 -*-
__doc__="""
Clean Up Layers. Goes through selected glyphs and deletes all unecessary layers while offering exceptions. Caution – Please customize in the script before use otherwise it might delete just all layers except Master Layers
"""
DeleteAlways_LayerWithTimestamp = True
DeleteAlways_LayersWithSameName = True

FirstMaster_OnlyBasicCleanUp = True # if True, only deletes layers with [no name], [timestamp(if true)] or [nameduplicates(if true)]
Delete_Manually_Specific = ["Light Extended"]

Delete_NOT_IfContains = [ "[", "]", "{","}", "bubble", "_" ]
Delete_NOT_IfStartsWith = ["_"]


import GlyphsApp

Font = Glyphs.font
selectedGlyphs = [ x.parent for x in Font.selectedLayers ]
thisMaster = Glyphs.font.selectedFontMaster
masterID = thisMaster.id
FirstMasterID = Font.masters[0].id
#selectedLayers = Font.selectedLayers



def process( thisGlyph):
	count = 0
	numberOfLayers = len( thisGlyph.layers )
	keptLayerNames = []
	for i in range( numberOfLayers )[::-1]:
		thisLayerShouldBeRemoved = True
		isDate = False
		thisLayer = thisGlyph.layers[i]
		thisLayerName = thisLayer.name
		if thisLayerName: # only check named layers
			if len(thisLayerName) > 3:
				if thisLayerName[-3] == ":":
					isDate = True
			if isDate != True or DeleteAlways_LayerWithTimestamp != True: # check only if there is no timestamp
				if (thisLayerName in keptLayerNames) and DeleteAlways_LayersWithSameName:
					hisLayerShouldBeRemoved = True
				else:
					if thisLayer.associatedMasterId == FirstMasterID and FirstMaster_OnlyBasicCleanUp: #only simple clean in FirstMaster
						thisLayerShouldBeRemoved = False
					else:
						if thisLayer.layerId != thisLayer.associatedMasterId: # except master layers
							for tmpstring in Delete_NOT_IfStartsWith:
								if thisLayerName.startswith(tmpstring):
									thisLayerShouldBeRemoved = False
							for tmpstring in Delete_NOT_IfContains:
								if tmpstring in thisLayerName:
									thisLayerShouldBeRemoved = False
						else:
							thisLayerShouldBeRemoved = False #keep Master Layers
				if thisLayerName in Delete_Manually_Specific:
					thisLayerShouldBeRemoved = True


		if thisLayerShouldBeRemoved:
			count += 1
			del thisGlyph.layers[i]
		else:
			keptLayerNames += [thisLayerName]




	return count


def cleanUpLayers():
	Font.disableUpdateInterface()

	for thisGlyph in selectedGlyphs:
		print thisGlyph.name, process( thisGlyph ), "deleted"

	#for thisLayer in selectedLayers:
	#	thisGlyph = thisLayer.parent
	#
	#	thisGlyph.beginUndo()
	#	print "%s layers deleted in %s." % ( process( thisGlyph ), thisGlyph.name )
	#	thisGlyph.endUndo()

	Font.enableUpdateInterface()

cleanUpLayers()
