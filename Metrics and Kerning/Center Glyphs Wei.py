#MenuTitle: Center Glyphs Wei Huang
# -*- coding: utf-8 -*-
"""Center selected Glzphs."""
# https://github.com/mekkablue/Glyphs-Scripts/issues/287#issuecomment-1433953956


import vanilla
import GlyphsApp

def process( thisLayer ):
	LSB = thisLayer.LSB
	RSB = thisLayer.RSB
	width = thisLayer.width

	halfSB = (LSB + RSB)/2
	thisLayer.LSB = int(halfSB)
	thisLayer.RSB = int(halfSB)
	thisLayer.width = width

thisFont.disableUpdateInterface() # suppresses UI updates in Font View

for thisLayer in listOfSelectedLayers:
	thisGlyph = thisLayer.parent
	numberOfLayers = len( thisGlyph.layers )
	for i in range( numberOfLayers )[::-1]:
		thisOtherLayer = thisGlyph.layers[i]
		print "Processing", thisGlyph.name
		thisGlyph.beginUndo() # begin undo grouping
		process( thisOtherLayer )
		thisGlyph.endUndo()   # end undo grouping

thisFont.enableUpdateInterface() # re-enables UI updates in Font View
