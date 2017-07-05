#MenuTitle: Delete Layers in Current Glyph With Numeral at the End
# -*- coding: utf-8 -*-
__doc__="""
Goes through selected glyphs in ALL Masters and deletes all glyph layers with a Date / Numeral at the End.
"""

import GlyphsApp

Font = Glyphs.font
thisMaster = Glyphs.font.selectedFontMaster
masterID = thisMaster.id

selectedLayers = Font.selectedLayers
doNotDelete = [ "[]", "{}", "_" ]
doAlwaysDelete = "0,1,2,3,4,5,6,7,8,9".split(",")#[ "0","1","2","3","4","5","6","7","8","9"]
print doAlwaysDelete
print list("0123")

def process( thisGlyph ):
	count = 0

	numberOfLayers = len( thisGlyph.layers )
	for i in range( numberOfLayers )[::-1]:
		thisLayer = thisGlyph.layers[i]
		#if thisLayer.associatedMasterId == masterID and
		if thisLayer.layerId != thisLayer.associatedMasterId: # not the master layer
			thisLayerName = thisLayer.name
			thisLayerShouldBeRemoved = False
			if thisLayerName: # always delete unnamed layers
				for parentheses in doAlwaysDelete:
					closing = parentheses
					print thisLayerName, closing

					# check if ONE of them is at the END of the layer name, like:
					# Bold [160], Bold [160[, Bold ]160], Regular {120}
					if thisLayerName.endswith(closing):
						print True
						thisLayerShouldBeRemoved = True

			else:
				print thisLayerName
				thisLayerShouldBeRemoved = True

			print thisLayerName

			if thisLayerShouldBeRemoved:
				count += 1
				del thisGlyph.layers[i]

	return count

Font.disableUpdateInterface()

for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent

	thisGlyph.beginUndo()
	print "%s layers deleted in %s." % ( process( thisGlyph ), thisGlyph.name )
	thisGlyph.endUndo()

Font.enableUpdateInterface()
