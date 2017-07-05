#MenuTitle: Reset entry and exit anchors to x=LSB/RSB
# -*- coding: utf-8 -*-
__doc__="""
Resets entry and exit anchors to x=LSB/RSB in any selected Glyph.
"""

import GlyphsApp

Glyphs.clearLog()
Glyphs.showMacroWindow()

Font = Glyphs.font
selectedLayers = Font.selectedLayers

def findOncurveAtRSB( thisLayer ):
	layerWidth = thisLayer.width
	myRSBnodes = []

	for thisPath in thisLayer.paths:
		for thisNode in thisPath.nodes:
			if thisNode.type != GSOFFCURVE and abs( thisNode.x - layerWidth ) < 1.0:
				myRSBnodes.append( thisNode )

	if len( myRSBnodes ) == 1:
		return myRSBnodes[0]
	else:
		#print "%s: %s potential entry points" % ( thisLayer.parent.name, len( myRSBnodes ) )
		return None

def deleteEntryExitAnchors( thisLayer ):
	CoordY = {}
	anchorsToBeDeleted = [ a for a in thisLayer.anchors if a.name.startswith("exit_") or a.name.startswith("entry_") or a.name in ("exit", "entry") ]
	if anchorsToBeDeleted:
		print "  Deleting: %s" % ( ", ".join([a.name for a in anchorsToBeDeleted]) )
		for thisAnchor in anchorsToBeDeleted:
			print "..", thisAnchor.name, thisAnchor.y
			CoordY[str(thisAnchor.name)] = thisAnchor.y
			thisLayer.removeAnchor_(thisAnchor)
		return CoordY
	else:
		CoordY["entry"] = 0.0
		CoordY["exit"] = 0.0
		return CoordY

def process( thisLayer ):
	listOfAnchorNames = [ a.name for a in thisLayer.anchors ]
	glyphName = thisLayer.parent.name
	CoordY = deleteEntryExitAnchors( thisLayer )
	print CoordY



	# add exit at 0,0:
	#if ".init" in glyphName or ".medi" in glyphName:
	#if len( thisLayer.paths ) > 0:
	# if "exit" not in listOfAnchorNames:
	myExit = GSAnchor( "exit", NSPoint( 0.0, CoordY["exit"] ) )
	thisLayer.addAnchor_( myExit )
	#print "%s: exit" % glyphName


	# add entry at RSB:
	#if ".medi" in glyphName or ".fina" in glyphName:
	# if "entry" not in listOfAnchorNames:
	#myEntryPoint = findOncurveAtRSB( thisLayer )
	#if myEntryPoint != None:
	#	#myEntry = GSAnchor( "entry", NSPoint( myEntryPoint.x, myEntryPoint.y ) )
	#else:
	myEntry = GSAnchor( "entry", NSPoint( thisLayer.width, CoordY["entry"] ) )

	thisLayer.addAnchor_( myEntry )
	#print "%s: entry" % glyphName
	print "Entry/Exit reset to LSB/RSB, 0.0"

Font.disableUpdateInterface()

for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo()
	process( thisLayer )
	thisGlyph.endUndo()

Font.enableUpdateInterface()
