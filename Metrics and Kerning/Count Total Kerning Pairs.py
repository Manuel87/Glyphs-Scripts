# MenuTitle: Count total kerning pairs + efficiency
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Shows total amount of kerning pairs of each possible glyph-to-glyph pair combinaition actually in effect -vs- regular kerning count were class-to-class pairs are only counted as one pair + calculates the efficiency that results out of the two.
"""


import time
from GlyphsApp import Glyphs


thisFont = Glyphs.font
thisFont.disableUpdateInterface()
start_time = time.time()
Glyphs.showMacroWindow()


KerningClasses_L = {}
KerningClasses_R = {}

for glyph in thisFont.glyphs: # writing a dictionary with all classes that are actually used by exporting glyphs
	if glyph.export != 0: # not counting non-exporting glyphs / not adding it to this kerning class dictionary
	    leftSideKerningClass = glyph.rightKerningGroup # left side of a kerning pair = right side of the glyph on the left and vice versa
	    rightSideKerningClass = glyph.leftKerningGroup
	    if leftSideKerningClass:
	    	leftSideKerningClass = "L_" + glyph.rightKerningGroup
	    	if leftSideKerningClass in KerningClasses_L:
	    		KerningClasses_L[leftSideKerningClass] = KerningClasses_L[leftSideKerningClass] + 1
	    	else:
	    		KerningClasses_L[leftSideKerningClass] = 1
	    if rightSideKerningClass:
	    	rightSideKerningClass = "R_" + glyph.leftKerningGroup
	    	if rightSideKerningClass in KerningClasses_R:
	    		KerningClasses_R[rightSideKerningClass] = KerningClasses_R[rightSideKerningClass] + 1
	    	else:
	    		KerningClasses_R[rightSideKerningClass] = 1

#print(f"\nKerningClasses_L: \n{KerningClasses_L}")
#print(f"\nKerningClasses_R: \n{KerningClasses_R}")

for this_master in thisFont.masters:
	print(f"\n--------------------\n{this_master.name}")
	kn = 0
	kn2 = 0
	kt = 0
	count_L = 0	
	count_R = 0
	count_L_R = 0
	master_id = this_master.id
	KernDict = dict( thisFont.kerning[master_id] ) #converting to proper dict
	for leftSide in KernDict:
		KernDict[leftSide] = dict(KernDict[leftSide]) #converting to proper dict second level too

	for leftSide in KernDict:
		glyphLeftClass = False
		glyphRightClass = False
		count_L_R = 0 
		if str(leftSide)[0]=='@':
			kerningClass_L = "L_" + leftSide.split('_L_')[-1]
			if kerningClass_L in KerningClasses_L:  # check if class is used by any glyph (filtering out non-exporting)
				count_L = KerningClasses_L[kerningClass_L]
			else:
				count_L = 0
		else:
			glyphOnLeft = thisFont.glyphForId_(leftSide)
			if glyphOnLeft.export != 0: # check if this glyph-to-glyph kerning is used by any glyph (filtering out non-exporting)
				if thisFont.glyphForId_(leftSide).rightKerningGroup:
					glyphLeftClass = True
				else:
					glyphLeftClass = False
				count_L = 1
			else:
				count_L = 0
		
		for rightSide in KernDict[leftSide]:
			if str(rightSide)[0]=='@':		
				kerningClass_R = "R_" + rightSide.split('_R_')[-1]
				if kerningClass_R in KerningClasses_R: # check if class is used by any glyph (filtering out non-exporting)
					count_R = KerningClasses_R[kerningClass_R]
				else:
					count_R = 0
			else:
				glyphOnRight = thisFont.glyphForId_(rightSide)
				if glyphOnRight.export != 0: # check if this glyph-to-glyph kerning is used by any glyph (filtering out non-exporting)
					if glyphOnRight.leftKerningGroup:
						glyphRightClass = True
					else:
						glyphRightClass = False
					count_R = 1
				else:
					count_R = 0
			if count_L == 0 and count_R == 0:
				kn2 = kn2 # not counting non-exporting glyphs
			elif count_L == 0 or count_R == 0:
				kn2 = kn2 # not counting non-exporting glyphs
			else:
				kn2 = kn2 + 1 
			kn = kn + 1
			if glyphLeftClass == True and glyphRightClass == True: # remove glyph_glyph pairs from counting if they have classes, as they are already counted via the classes
				kt = kt # do not count as it is already counted via the kerning classes
			else:
				count_L_R = count_L * count_R
				kt = kt + count_L_R

	print(f"--------------------\n{kn} Normal kerning pairs")
	print(f"--------------------\n{kn2} Normal kerning pairs, excluding non-exporting glyphs") 
	print(f"--------------------\n{kt} Total kerning pairs, excluding non-exporting glyphs")
	print(f"--------------------\n{round(kt/kn2, 2)} Efficiency (the larger the better)")


print(f"\n\n-------------------------------------------------------\nNormal kerning pair count = each kerning group pair counts only as one entry, same as each glyph-to-glyph pair")
print(f"-------------------------------------------------------\nTotal kerning pair count = counting also all possible pair combinations of each glyph within kerning groups")
#print(f"-------------------------------------------------------\nNon-exporting glyphs: their pairs are removed\n-------------------------------------------------------")
print(f"-------------------------------------------------------\nExecution time: {round(time.time() - start_time, 4)} seconds\n-------------------------------------------------------\n\n" )


thisFont.enableUpdateInterface()

	 