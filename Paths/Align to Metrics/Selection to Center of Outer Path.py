#MenuTitle: Align Selection to Horizontal Object Center
# -*- coding: utf-8 -*-
__doc__="""
Align selected paths (and parts of paths) in the frontmost layer to the Horizontal Center of the drawn paths.
"""

import GlyphsApp
import math

Font = Glyphs.font
Doc = Glyphs.currentDocument
selectedLayer = Font.selectedLayers[0]
layerCenter = selectedLayer.width // 2
selectedComponent = selectedLayer.selection[0]

thisLSB = selectedLayer.LSB
thisRSB = selectedLayer.RSB
ObjectWidth = selectedLayer.width - thisLSB - thisRSB
ObjectCenter = (ObjectWidth // 2) + thisLSB
xheightCenter = Font.selectedFontMaster.xHeight // 2

def italicSkew(x, y, angle=Layer.master.italicAngle):
	"""Skews x/y along the x axis and returns skewed x value."""
	new_angle = (angle / 180.0) * math.pi
	return x + y * math.tan(new_angle)

try:
	try:
		# until v2.1:
		selection = selectedLayer.selection()
	except:
		# since v2.2:
		selection = selectedLayer.selection
	
	selectionYList = [ n.y for n in selection ]
	topMostY = max( selectionYList )
	bottomMostY = min( selectionYList )

	try: #works if it is an compoment
		selectionCenterY = selectedComponent.bounds.origin.y + selectedComponent.bounds.size.height // 2
	except:
		selectionCenterY = ( topMostY + bottomMostY ) // 2


	selectionXList = [ n.x for n in selection ]
	leftMostX = min( selectionXList )
	rightMostX = max( selectionXList )


	try:
		selectionCenter = selectedComponent.bounds.origin.x + selectedComponent.bounds.size.width // 2
		print(selectedComponent.bounds.origin.x)
	except:
		selectionCenter = ( leftMostX + rightMostX ) // 2



	layerCenterItalic = italicSkew(layerCenter, selectionCenterY-xheightCenter)
	ObjectCenterItalic = italicSkew(ObjectCenter, selectionCenterY-xheightCenter)
	centerOffset = float( ObjectCenterItalic - selectionCenter )





	Font.disableUpdateInterface()

	for thisNode in selection:
		thisNode.x += centerOffset

	Font.enableUpdateInterface()
	
except Exception as e:
	print("Error: Nothing selected in frontmost layer?")
	print(e)

