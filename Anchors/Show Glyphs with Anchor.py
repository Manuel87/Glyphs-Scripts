#MenuTitle: Show Glyphs with this Anchor
# -*- coding: utf-8 -*-
__doc__="""
New Tab with all Glyphs that have the selected anchor.
"""

thisFont = Glyphs.font # frontmost font
selectedLayer = thisFont.selectedLayers[0]
selection = selectedLayer.selection

editString = ""

for anchor in selection:
	if type(anchor) == GSAnchor:
		anchorName = anchor.name
		for glyph in thisFont.glyphs:
			thisLayer = glyph.layers[selectedLayer.associatedMasterId]
			if anchorName in thisLayer.anchors.keys():
				editString += "/" + glyph.name
if len(editString) > 0:
	thisFont.newTab(editString) ### Open Tab with all Characters
