#MenuTitle: Align Selection to RSB
# -*- coding: utf-8 -*-
__doc__="""
Align selected paths (and parts of paths) in the frontmost layer to the RSB.
"""

import GlyphsApp

Font = Glyphs.font
Doc = Glyphs.currentDocument
selectedLayer = Font.selectedLayers[0]
layerWidth = selectedLayer.width

try:
	try:
		# until v2.1:
		selection = selectedLayer.selection()
	except:
		# since v2.2:
		selection = selectedLayer.selection
	
	rightMostX = max( ( n.x for n in selection ) )

	Font.disableUpdateInterface()

	for thisNode in selection:
		thisNode.x += ( layerWidth - rightMostX )

	Font.enableUpdateInterface()
	
except Exception as e:
	print("Error: Nothing selected in frontmost layer?")
	print(e)
