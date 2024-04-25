#MenuTitle: Algin Center / Unify Bounds / Multiple Comp.
# -*- coding: utf-8 -*-
"""Make selected glyphs monospaced."""

import vanilla
import GlyphsApp
print("mystart");

def UnifyBounds():
	try:
		print("try")
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers

		# newWidth = float( self.w.changeValue.get() )

		
		for thisLayer in selectedLayers:
			LSB_RSB_Total = thisLayer.LSB + thisLayer.RSB
			
			changeValue = round(LSB_RSB_Total / 2)
			
			thisLayer.LSB = changeValue
			thisLayer.RSB = changeValue


	except Exception as e:
		raise e

UnifyBounds();