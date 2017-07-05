#MenuTitle: Zero Sidebearings
# encoding: utf-8
"""
Center Layers.py

Created by Georg Seifert on 2011-01-17.
Copyright (c) 2011 schriftgestaltung.de. All rights reserved.
"""

import sys
import os
from GlyphsApp import *
import objc
from AppKit import *
from Foundation import *

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

