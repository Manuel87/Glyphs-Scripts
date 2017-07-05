#MenuTitle: Create iColor Layers and Link Available Resolutions
# -*- coding: utf-8 -*-
__doc__="""
Make an Apple Image Font (copy iColor layers and link different resolutions)
"""
import GlyphsApp
import vanilla
import math
import os.path

font = Glyphs.font

myResolutions = ["96"]



# delete all extra layers by Tim Ahrens # https://github.com/justanotherfoundry/glyphsapp-scripts/blob/master/Remove%20Backup%20Layers.py

for glyph in font.glyphs:
	if glyph.selected:
		associated_layers = [ layer.layerId for layer in glyph.layers if layer.layerId != layer.associatedMasterId and not '[' in layer.name and not ']' in layer.name ]
		for layerId in associated_layers:
			del glyph.layers[layerId]
		print glyph.name, '-> deleting all extra layers'

print " "


# access all selected glyphs in the Font View
for glyph in font.glyphs:
	if glyph.selected:
		for resolution in myResolutions:
			mynewLayer = glyph.layers[0].copy()
			mynewLayer.name = 'iColor ' + resolution
			glyph.layers.append(mynewLayer)
			print glyph.name, '-> duplicated base layer and named:', mynewLayer.name
			##glyph.layers[0].backgroundImage.path = e

			if glyph.layers[0].backgroundImage:
				fileformat = glyph.layers[0].backgroundImage.path.split(".")[-1]

				orgPath = glyph.layers[0].backgroundImage.path
				newPath = glyph.layers[0].backgroundImage.path.split("Images/")
				newPath = newPath[0] + "Images/" + glyph.name + "-" + resolution + "." + fileformat

				if os.path.isfile(newPath):
					mynewLayer.backgroundImage.path = newPath
					print glyph.name, "->", mynewLayer.backgroundImage.path.split("Images")[-1]

		print " "
