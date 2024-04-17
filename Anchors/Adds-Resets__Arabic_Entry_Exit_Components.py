#MenuTitle: Adds/Resets Arabic _entry_comp and _exit_comp in selected Glyphs (one Master)
# -*- coding: utf-8 -*-
__doc__="""
Adds/Resets _entry_comp and _exit_comp components. (won't add if init/medi/fina component is already present)
Developed for Arabic, but should also work in other scripts that use init/medi/fina.
"""

import GlyphsApp

Glyphs.clearLog()
#Glyphs.showMacroWindow()

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
		#print "%s: %s potential _entry_comp points" % ( thisLayer.parent.name, len( myRSBnodes ) )
		return None

def process( thisLayer ):
	listOfComponentNames = [ a.name for a in thisLayer.components ]

	glyphName = thisLayer.parent.name

	dont_add_entry = 0
	dont_add_exit = 0

	#if glyphName.endswith("medi"): #endswith
	for component in thisLayer.components:
		if "fina" in component.name:
			dont_add_entry =+1
		if "medi" in component.name:
			dont_add_entry =+1
			dont_add_exit =+1
		if "init" in component.name:
			dont_add_exit =+1

	if "medi" in glyphName:
		theseComponents = thisLayer.components
		numberOfComponents = len( theseComponents )
		if numberOfComponents > 0:
			for i in range(numberOfComponents)[::-1]:
				thisComponent = theseComponents[i]
				if "entry" in thisComponent.componentName:
					thisLayer.removeComponent_( thisComponent )
				if "exit" in thisComponent.componentName:
					thisLayer.removeComponent_( thisComponent )

		if dont_add_entry == 0:
			myEntry = GSComponent( "_entry_comp", NSPoint( thisLayer.width, 0.0 ) )
			thisLayer.addComponent_( myEntry )

		if dont_add_exit == 0:
			myExit = GSComponent( "_exit_comp", NSPoint( 0.0, 0.0 ) )
			thisLayer.addComponent_( myExit )

	if "init" in glyphName:
		theseComponents = thisLayer.components
		numberOfComponents = len( theseComponents )
		if numberOfComponents > 0:
			for i in range(numberOfComponents)[::-1]:
				thisComponent = theseComponents[i]
				if "exit" in thisComponent.componentName:
					thisLayer.removeComponent_( thisComponent )

		if dont_add_exit == 0:
			myExit = GSComponent( "_exit_comp", NSPoint( 0.0, 0.0 ) )
			thisLayer.addComponent_( myExit )

	if "fina" in glyphName:
		theseComponents = thisLayer.components
		numberOfComponents = len( theseComponents )
		if numberOfComponents > 0:
			for i in range(numberOfComponents)[::-1]:
				thisComponent = theseComponents[i]
				if "entry" in thisComponent.componentName:
					thisLayer.removeComponent_( thisComponent )
		if dont_add_entry == 0:
			myEntry = GSComponent( "_entry_comp", NSPoint( thisLayer.width, 0.0 ) )
			thisLayer.addComponent_( myEntry )


Font.disableUpdateInterface()

for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo()
	process( thisLayer )
	thisGlyph.endUndo()

Font.enableUpdateInterface()
