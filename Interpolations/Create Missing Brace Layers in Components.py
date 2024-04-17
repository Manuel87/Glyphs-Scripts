#MenuTitle: Create Missing Brace Layers in Components (edit)
# -*- coding: utf-8 -*-

'''
This script goes through all component glyphs and adds missing intermediate masters (called "Brace Layers" in Glyphs)
to the component glyphs where their respective base glyphs have them. For instance, if an `e` has a brace layer, 
all glyphs based on it such as `é` etc. also need a brace layer at the same value.

This is necessary to create correct Variable Fonts in environments outside Glyphs 
(such as [googlefonts/fontmake](https://github.com/googlefonts/fontmake), and even in Glyphs itself 
as of this writing, August 2019).

Otherwise, component glyphs’ metrics get interpolated linearly between the main masters, ignoring the 
intermediate masters, while the outlines get interpolated correctly. This leads to sidebearing discrepancies 
of component glyphs with base glyphs referencing intermediate masters.
'''

from GlyphsApp import *
f = Glyphs.font

def normalizeBraceLayerName(name):
	return name.replace(' ', '').replace(',', ', ').replace('\u2009','').replace(' ','')

#isBrace = "{" in layerName and "}" in layerName and layerName.find("{") < layerName.find("}")-1
def glyphHasBraceLayer(g):
	if g:
		for l in g.layers:
			if '{' in l.name and '}' in l.name:
				return True
		return False
	return False

def glyphBraceLayerNames(thisGlyph):
	'''Return layer names and associatedMasterIds as list'''
	layerNames = []
	for l in thisGlyph.layers:
		if '{' in l.name and '}' in l.name:
			newLayerName = normalizeBraceLayerName(l.name)

			if not newLayerName in layerNames:
				layerNames.append([newLayerName, l.associatedMasterId])
	return layerNames


def glyphBraceLayerNamesOnly(thisGlyph):
	'''Return layer names and associatedMasterIds as list'''
	layerNames = []
	for l in thisGlyph.layers:
		if '{' in l.name and '}' in l.name:
			newLayerName = normalizeBraceLayerName(l.name)

			if not newLayerName in layerNames:
				layerNames.append(newLayerName)
	return layerNames




layerNames = []

def glyphBraceLayerWithAttributes(thisGlyph):
	'''Return layer names and associatedMasterIds as list'''
	#layerNames = []
	Bracelayers = []
	g = 0
	for l in thisGlyph.layers:
		if '{' in l.name and '}' in l.name:
			newLayerName = normalizeBraceLayerName(l.name)
			newLayerAttributes = l.attributes["coordinates"]

			#print(l.attributes["coordinates"])
			#print("{300,\u20091,\u20090}", normalizeBraceLayerName("{300,\u20091,\u20090}"))
			#g=+1
			#if g == 1:
			if not newLayerName in layerNames:
				print(" "," + brace layer",newLayerName)
				layerNames.append(newLayerName)
				Bracelayers.append([newLayerName, l.associatedMasterId, newLayerAttributes])

			#else:
				#print("Layer already existing")
				#if not newLayerName in layerNames:
				#layerNames.append(newLayerName)
				#Bracelayers.append([newLayerName, l.associatedMasterId, newLayerAttributes])
	#print(layerNames)
	return Bracelayers

# Go through glyphs
thisFont = Glyphs.font # frontmost font
currentMaster = thisFont.selectedFontMaster
#GlyphLayerCount = 0



# for g in f.glyphs:
# 	for l in thisGlyph.layers:


#selectedGlyphs = [ l.parent for l in thisFont.selectedLayers if l.parent.name is not None ]
#for thisGlyph in selectedGlyphs:
for layer in thisFont.selectedLayers:
	thisGlyph = layer.parent
	for thisLayer in thisGlyph.layers:
		print("🔠 Processing %s" % thisGlyph.name)
		if thisLayer.components:
			#print("has component:",thisLayer.components)
			for c in thisLayer.components:
				if glyphHasBraceLayer(c.component):
					print("  component:",c.component.name,"(brace layer)")
					#print("has brace layer")
					# Remove duplicates already present in component glyph
					#createBraceLayerNames = glyphBraceLayerNames(c.component)
					createBraceLayerWithAttributes = glyphBraceLayerWithAttributes(c.component) #NEW

					# for layerName, associatedMasterId in glyphBraceLayerNames(thisGlyph):
					# 	if [createBraceLayerNames(layerName), associatedMasterId] in createBraceLayerNames:
					# 		createBraceLayerNames.remove([normalizeBraceLayerName(layerName), associatedMasterId])


					#newLayer = thisGlyph.layers[currentMaster.id].copy()
					# Insert new brace layers
					for layerName,associatedMasterId,attributes in createBraceLayerWithAttributes:
						if not layerName in glyphBraceLayerNamesOnly(thisGlyph):
							newLayer = GSLayer()
							axes = Font.axes
							newLayer.attributes["coordinates"] = attributes
							newLayer.associatedMasterId = associatedMasterId
							newLayer.name = layerName
							thisGlyph.layers.append(newLayer)
							newLayer.reinterpolate()
							newLayer.syncMetrics()

						#print('Added layer %s to %s' % (layerName, thisGlyph))
				#else:
				#	print('(no brace layer)')
