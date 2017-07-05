#MenuTitle: Delete Paths and Zero Sidebearings
# -*- coding: utf-8 -*-
__doc__="""
Deletes all paths in visible layers of selected glyphs.
"""

import sys
import os
from GlyphsApp import *
import objc
from AppKit import *
from Foundation import *

Font = Glyphs.font
selectedLayers = Font.selectedLayers

def process( thisLayer ):
	thisLayer.parent.beginUndo()

	for i in range( len( thisLayer.paths ))[::-1]:
		del thisLayer.paths[i]

	thisLayer.parent.endUndo()

Font.disableUpdateInterface()

for thisLayer in selectedLayers:
	print "Clearing %s." % thisLayer.parent.name
	process( thisLayer )

Font.enableUpdateInterface()


def main():
	Doc = Glyphs.currentDocument
	Font = Doc.font
	for glyph in Font.glyphs:
	#SelectedLayers = Doc.selectedLayers()
	#for Layer in SelectedLayers:
		glyph.layers[0].LSB = 0
		glyph.layers[0].RSB = 0

if __name__ == '__main__':
	main()
