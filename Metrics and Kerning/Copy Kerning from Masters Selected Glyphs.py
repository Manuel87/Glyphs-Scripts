#MenuTitle: Copy kerning of selected glyphs from masters 1-2 to 3-4 (customizable)
# encoding: utf-8

__doc__="""
Copies Kerning from selection or alternatively from cursor position from masters 1-2 to 3-4 (edit script to fit your needs)
"""

# Customise here
# -------------------------------
sourceMasters = [1,2] # 1 = first master
targetMasters = [3,4] 
# -------------------------------




import traceback

Glyphs.showMacroWindow()
font = Glyphs.fonts[0]
tab = font.currentTab

	
def copyKerningFromMasterToMaster(source, target):
	i = 0 #glyph index
	selectedText = []
	selectedGlyphs = [layer.parent for layer in font.selectedLayers if layer.parent.name is not None]
	for thisGlyph in selectedGlyphs:
		selectedText.append(thisGlyph)
	
	if len(selectedText) > 1:

		print("\nCopy kerning: ", source.name, "->", target.name)
		print("--------------------------------------------")

		for i in range(len(selectedText)-1):
			
			currGlyph = selectedText[i] 
			nextGlyph = selectedText[i+1] #next.parent
			
			printString = f"{selectedText[i].name}-{selectedText[i+1].name}"
			
	

			copyKerningFrom(source, target, currGlyph, nextGlyph, printString)

	else:
		type(tab.layers[tab.textCursor+1: tab.textCursor + 2][0]) is GSControlLayer
		
		type(tab.layers[tab.textCursor+1: tab.textCursor + 2][0]) is GSControlLayer
	
		
		left = tab.layers[tab.textCursor-1: tab.textCursor + 1][0]
		right = tab.layers[tab.textCursor: tab.textCursor + 2][0]
		
		leftGlyph = False
		rightGlyph = False
			
		if type(left) is not GSControlLayer:
			leftGlyph = left.parent
			
		if type(next) is not GSControlLayer:
			rightGlyph = right.parent

		if not leftGlyph or not rightGlyph:
			raise SystemExit() # stop script if there is no glyph pair found
		
		print("\nCopy kerning: ", source.name, "->", target.name)
		print("--------------------------------------------")
		printString = f"{left.parent.name}-{right.parent.name}"
			
		copyKerningFrom(source, target, leftGlyph, rightGlyph, printString)
	

		

def copyKerningFrom(source, target, left, right, printString):
		
	try:
		if left.rightKerningKey and right.leftKerningKey:
			leftKern = left.rightKerningKey
			rightKern = right.leftKerningKey

			try:
				kern = font.kerningForPair(source.id, leftKern, rightKern)
				
				print(printString, kern)

				if kern == None:
					font.removeKerningForPair(target.id, leftKern, rightKern)
					return
				else:
					#if kern > 10000:
						#font.removeKerningForPair(target.id, leftKern, rightKern)
						#return
									
					font.setKerningForPair(target.id, leftKern, rightKern, kern)
					return
			except:
				print("")
	except:
		print( traceback.format_exc())


try:

	j = 0
	for source in sourceMasters:
		copyKerningFromMasterToMaster(font.masters[sourceMasters[j]-1], font.masters[targetMasters[j]-1])
		j = j+1

except:
	print("no pair found")

print("\n\n")


		
		