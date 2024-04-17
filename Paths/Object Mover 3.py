#MenuTitle: Object Mover 3.0 ...
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Batch-process path positions in selected glyphs (GUI).
ToDo: clean up print commands
ToDo: also move anchors along
ToDo: Only move slected path(s) within a single glyph (especially be careful for italics as currently positioning is solved by LSB/RSB and not italic angle directly as there was some error with that, but its in the code and if applied right it should work ... also check my Selection to Center.py for that)

"""
# based on Anchor Mover 2.0 by mekkablue

import vanilla, math
from Foundation import NSPoint
from AppKit import NSAffineTransform, NSAffineTransformStruct

def transform(shiftX=0.0, shiftY=0.0, rotate=0.0, skew=0.0, scale=1.0):
	"""
	Returns an NSAffineTransform object for transforming layers.
	Apply an NSAffineTransform t object like this:
		Layer.transform_checkForSelection_doComponents_(t,False,True)
	Access its transformation matrix like this:
		tMatrix = t.transformStruct() # returns the 6-float tuple
	Apply the matrix tuple like this:
		Layer.applyTransform(tMatrix)
		Component.applyTransform(tMatrix)
		Path.applyTransform(tMatrix)
	Chain multiple NSAffineTransform objects t1, t2 like this:
		t1.appendTransform_(t2)
	"""
	myTransform = NSAffineTransform.transform()
	if rotate:
		myTransform.rotateByDegrees_(rotate)
	if scale != 1.0:
		myTransform.scaleBy_(scale)
	if not (shiftX == 0.0 and shiftY == 0.0):
		myTransform.translateXBy_yBy_(shiftX, shiftY)
	if skew:
		skewStruct = NSAffineTransformStruct()
		skewStruct.m11 = 1.0
		skewStruct.m22 = 1.0
		skewStruct.m21 = math.tan(math.radians(skew))
		skewTransform = NSAffineTransform.transform()
		skewTransform.setTransformStruct_(skewStruct)
		myTransform.appendTransform_(skewTransform)
	return myTransform

def italicize(thisPoint, italicAngle=0.0, pivotalY=0.0):
	"""
	Returns the italicized position of an NSPoint 'thisPoint'
	for a given angle 'italicAngle' and the pivotal height 'pivotalY',
	around which the italic slanting is executed, usually half x-height.
	Usage: myPoint = italicize(myPoint,10,xHeight*0.5)
	"""
	x = thisPoint.x
	yOffset = thisPoint.y - pivotalY # calculate vertical offset
	italicAngle = math.radians(italicAngle) # convert to radians
	tangens = math.tan(italicAngle) # math.tan needs radians
	horizontalDeviance = tangens * yOffset # vertical distance from pivotal point
	x += horizontalDeviance # x of point that is yOffset from pivotal point
	return NSPoint(x, thisPoint.y)

def highestNodeInLayer(layer):
	highest = None
	for p in layer.paths:
		for n in p.nodes:
			if n.type != GSOFFCURVE:
				if highest is None or highest.y < n.y:
					highest = n
	return highest

def lowestNodeInLayer(layer):
	lowest = None
	for p in layer.paths:
		for n in p.nodes:
			if n.type != GSOFFCURVE:
				if lowest is None or lowest.y > n.y:
					lowest = n
	return lowest

def rightmostNodeInLayer(layer):
	rightmost = None
	for p in layer.paths:
		for n in p.nodes:
			if n.type != GSOFFCURVE:
				if rightmost is None or rightmost.x < n.x:
					rightmost = n
	return rightmost

def leftmostNodeInLayer(layer):
	leftmost = None
	for p in layer.paths:
		for n in p.nodes:
			if n.type != GSOFFCURVE:
				if leftmost is None or leftmost.x > n.x:
					leftmost = n
	return leftmost

listType = (
	("Everything", "0"),
	("Paths only", "1"),
	("Copmonents only", "2")
	)

listHorizontal = (
	("current position", "copyPathX"),
	("align center @ center (half of total width)", "copyLayer.width // 2.0"),
	("align left @ LSB", "0.0 + copyPathWidth // 2"),
	("align right @ RSB", "copyLayer.width - copyPathWidth // 2"),
	#("bbox left edge", "0.0 + copyPathWidth // 2"),
	#("bbox center", "copyLayer.bounds.origin.x + copyLayer.width // 2.0"),
	#("bbox right edge", "copyLayer.bounds.origin.x + copyLayer.bounds.size.width"),
	#("highest node", "highestNodeInLayer(copyLayer).x"),
	#("lowest node", "lowestNodeInLayer(copyLayer).x"),

	# ("bbox left edge", "copyLayer.bounds.origin.x"),
	# ("bbox center", "copyLayer.bounds.origin.x + copyLayer.bounds.size.width // 2.0"),
	# ("bbox right edge", "copyLayer.bounds.origin.x + copyLayer.bounds.size.width"),
	# ("highest node", "highestNodeInLayer(copyLayer).x"),
	# ("lowest node", "lowestNodeInLayer(copyLayer).x"),
	)

listVertical = (
	("current position", "copyPathY"),
	("align center, exaclty at -------------->", "0.0"),
	("align center @ half cap height", "selectedCapheight // 2.0"),
	("align center @ half mix -> 0.45:0.05 (UC:LC)", "selectedCapheight * 0.45 + selectedXheight * 0.05"),
	("align center @ half mix -> 0.40:0.10 (UC:LC)", "selectedCapheight * 0.40 + selectedXheight * 0.10"),
	("align center @ half mix -> 0.35:0.15 (UC:LC)", "selectedCapheight * 0.35 + selectedXheight * 0.15"),
	("align center @ half mix -> 0.30:0.20 (UC:LC)", "selectedCapheight * 0.30 + selectedXheight * 0.20"),
	("align center @ half mix -> 0.27:0.23 (UC:LC)", "selectedCapheight * 0.27 + selectedXheight * 0.23"),
	("align center @ half mix -> 0.25:0.25 (UC:LC)", "selectedCapheight * 0.25 + selectedXheight * 0.25"),
	("align center @ half mix -> 0.20:0.30 (UC:LC)", "selectedCapheight * 0.20 + selectedXheight * 0.30"),
	("align center @ half mix -> 0.15:0.35 (UC:LC)", "selectedCapheight * 0.15 + selectedXheight * 0.35"),
	("align center @ half mix -> 0.10:0.40 (UC:LC)", "selectedCapheight * 0.10 + selectedXheight * 0.40"),
	("align center @ half mix -> 0.05:0.45 (UC:LC)", "selectedCapheight * 0.05 + selectedXheight * 0.45"),
	("align center @ half x-height", "selectedXheight // 2.0"),
	("align center @ half smallcap height", "originalMaster.customParameters['smallCapHeight']/2"),
	("align center @ half ascender", "selectedAscender // 2.0"),
	("align top, exaclty at --------------", "0.0 - copyPathHeight // 2"),
	("align top @ ascender", "selectedAscender - copyPathHeight // 2"),
	("align top @ cap height", "selectedCapheight - copyPathHeight // 2"),
	("align top @ smallcap height", "originalMaster.customParameters['smallCapHeight']- copyPathHeight // 2"),
	("align top @ x-height", "selectedXheight - copyPathHeight // 2"),
	("align bottom, exaclty at -------------->", "0.0 + copyPathHeight // 2"),
	("align bottom @ baseline", "0.0 + copyPathHeight // 2"),
	("align bottom @ descender", "selectedDescender + copyPathHeight // 2"),
	# ("bbox top", "copyLayer.bounds.origin.y + copyLayer.bounds.size.height"),
	# ("bbox center", "copyLayer.bounds.origin.y + ( copyLayer.bounds.size.height // 2.0 )"),
	# ("bbox bottom", "copyLayer.bounds.origin.y"),
	# ("leftmost node", "leftmostNodeInLayer(copyLayer).y"),
	# ("rightmost node", "rightmostNodeInLayer(copyLayer).y"),
	)

def italicSkew(x, y, angle=10.0):
	"""Skews x/y along the x axis and returns skewed x value."""
	new_angle = (angle / 180.0) * math.pi
	return x + y * math.tan(new_angle)

class ObjectMover3(object):
	prefID = "com.manuel_87.ObjectMover3"

	def __init__(self):
		linePos, inset, lineHeight = 12, 15, 22

		self.w = vanilla.FloatingWindow((500, 175), "Object Mover 3.0", minSize=(350, 175), maxSize=(1000, 175), autosaveName=self.pref("mainwindow"))

		#self.w.text_1 = vanilla.TextBox((inset, linePos + 2, inset + 60, 14), "Move Object", sizeStyle='small')
		#self.w.object_type = vanilla.ComboBox((inset + 75, linePos - 1, -110 - inset - 25, 19), [t[0] for t in listType], sizeStyle='small', callback=self.SavePreferences)
			#self.w.type_name = vanilla.ComboBox((inset + 75, linePos - 1, -110 - inset - 25, 19), self.GetAnchorNames(), sizeStyle='small', callback=self.SavePreferences)
		#self.w.button = vanilla.SquareButton((-110 - inset - 20, linePos, -110 - inset, 18), u"↺", sizeStyle='small', callback=self.SetAnchorNames)
		#self.w.text_2 = vanilla.TextBox((-105 - 15, linePos + 2, -inset, 14), "in selected glyphs:", sizeStyle='small')
		#linePos += lineHeight

		self.w.hText_1 = vanilla.TextBox((inset - 2, linePos, 20, 14), u"↔", sizeStyle='regular')
		self.w.hText_2 = vanilla.TextBox((inset + 20, linePos + 2, 20, 14), "to", sizeStyle='small')
		self.w.hTarget = vanilla.PopUpButton((inset + 40, linePos, -50 - 15 - 15 - inset, 17), [x[0] for x in listHorizontal], sizeStyle='small', callback=self.SavePreferences)
		self.w.hText_3 = vanilla.TextBox((-60 - 15 - 15, linePos + 2, -50 - inset, 14), "+", sizeStyle='small')
		self.w.hChange = vanilla.EditText((-60 - 15, linePos, -inset, 19), "0.0", sizeStyle='small', callback=self.SavePreferences)
		linePos += lineHeight

		self.w.vText_1 = vanilla.TextBox((inset, linePos, 20, 14), u"↕", sizeStyle='regular')
		self.w.vText_2 = vanilla.TextBox((inset + 20, linePos + 2, 20, 14), "to", sizeStyle='small')
		self.w.vTarget = vanilla.PopUpButton((inset + 40, linePos, -50 - 15 - 15 - inset, 17), [y[0] for y in listVertical], sizeStyle='small', callback=self.SavePreferences)
		self.w.vText_3 = vanilla.TextBox((-60 - 15 - 15, linePos + 2, -50 - inset, 14), "+", sizeStyle='small')
		self.w.vChange = vanilla.EditText((-60 - 15, linePos, -inset, 19), "0.0", sizeStyle='small', callback=self.SavePreferences)
		linePos += lineHeight

		self.w.italic = vanilla.CheckBox((inset, linePos, -inset, 18), "Respect italic angle", value=True, sizeStyle='small', callback=self.SavePreferences)
		linePos += lineHeight

		self.w.allMasters = vanilla.CheckBox(
			(inset, linePos, -inset, 20), u"All masters and special layers (otherwise only current masters)", value=False, callback=self.SavePreferences, sizeStyle='small'
			)
		linePos += lineHeight

		self.w.moveButton = vanilla.Button((-80 - 15, -20 - 15, -15, -15), "Move", sizeStyle='regular', callback=self.MoveCallback)
		self.w.setDefaultButton(self.w.moveButton)

		if not self.LoadPreferences():
			print("Error: Could not load preferences. Will resort to defaults.")

		self.w.open()
		self.w.makeKey()

	def domain(self, prefName):
		prefName = prefName.strip().strip(".")
		return self.prefID + "." + prefName.strip()

	def pref(self, prefName):
		prefDomain = self.domain(prefName)
		return Glyphs.defaults[prefDomain]

	def SavePreferences(self, sender=None):
		try:
			# write current settings into prefs:
			#Glyphs.defaults[self.domain("type_name")] = self.w.type_name.get()
			Glyphs.defaults[self.domain("hTarget")] = self.w.hTarget.get()
			Glyphs.defaults[self.domain("hChange")] = self.w.hChange.get()
			Glyphs.defaults[self.domain("vTarget")] = self.w.vTarget.get()
			Glyphs.defaults[self.domain("vChange")] = self.w.vChange.get()
			Glyphs.defaults[self.domain("italic")] = self.w.italic.get()
			Glyphs.defaults[self.domain("allMasters")] = self.w.allMasters.get()
			return True
		except:
			import traceback
			print(traceback.format_exc())
			return False

	def LoadPreferences(self):
		try:
			# register defaults:
			#Glyphs.registerDefault(self.domain("type_name"), "")
			Glyphs.registerDefault(self.domain("hTarget"), 0.0)
			Glyphs.registerDefault(self.domain("hChange"), 0.0)
			Glyphs.registerDefault(self.domain("vTarget"), 0.0)
			Glyphs.registerDefault(self.domain("vChange"), 0.0)
			Glyphs.registerDefault(self.domain("italic"), True)
			Glyphs.registerDefault(self.domain("allMasters"), False)

			# load previously written prefs:
			#self.w.type_name.set(self.pref("type_name"))
			self.w.hTarget.set(self.pref("hTarget"))
			self.w.hChange.set(self.pref("hChange"))
			self.w.vTarget.set(self.pref("vTarget"))
			self.w.vChange.set(self.pref("vChange"))
			self.w.italic.set(self.pref("italic"))
			self.w.allMasters.set(self.pref("allMasters"))
			return True
		except:
			import traceback
			print(traceback.format_exc())
			return False

	def prefAsFloat(self, pref):
		try:
			preference = self.pref(pref)
			return float(preference)
		except:
			Glyphs.defaults[self.domain(pref)] = 0.0
			self.LoadPreferences()
			return 0.0

	def MoveCallback(self, sender):
		# brings macro window to front and clears its log:
		Glyphs.clearLog()

		thisFont = Glyphs.font
		selectedLayers = thisFont.selectedLayers
		#type_name = self.pref("type_name")
		horizontal_index = self.pref("hTarget")
		horizontal_change = self.prefAsFloat("hChange")
		vertical_index = self.pref("vTarget")
		vertical_change = self.prefAsFloat("vChange")
		allMasters = self.pref("allMasters")
		respectItalic = self.pref("italic")

		# print(horizontal_index)
		# print(listHorizontal[horizontal_index])
		# print(listHorizontal[horizontal_index][1])
		evalCodeH = listHorizontal[horizontal_index][1]
		evalCodeV = listVertical[vertical_index][1]

		if not selectedLayers:
			print("No glyphs selected.")
			Message(title="No Glyphs Selected", message="Could not move objects. No glyphs were selected.", OKButton=None)
		else:
			print("Processing %i glyph%s..." % (
				len(selectedLayers),
				"" if len(selectedLayers) == 1 else "s",
				))
			thisFont.disableUpdateInterface()
			try:
				for selectedLayer in selectedLayers:
					selectedGlyph = selectedLayer.glyph()
					if selectedGlyph:
						print("\n🔠 %s" % selectedGlyph.name)
						if allMasters:
							originalLayers = tuple([l for l in selectedGlyph.layers if l.isMasterLayer or l.isSpecialLayer])
						else:
							originalLayers = (selectedLayer, )

						for originalLayer in originalLayers:
							originalMaster = originalLayer.master
							selectedAscender = originalMaster.ascender
							selectedCapheight = originalMaster.capHeight
							selectedDescender = originalMaster.descender
							selectedXheight = originalMaster.xHeight
							halfXHeight = selectedXheight * 0.5
							italicAngle = originalMaster.italicAngle

							# print(originalLayer.components)
							if len(originalLayer.paths) == 0 and len(originalLayer.components) == 0:
								print("⚠️ no paths nor components on layer %s." % originalLayer.name)
							else:
								thisGlyph = originalLayer.parent

								# create a layer copy that can be slanted backwards if necessary
								copyLayer = originalLayer.copyDecomposedLayer()
								#print("decompose copy")
								#copyLayer = originalLayer.copyDecomposedLayer()
								#copyLayer.decomposeCorners()
								# thisGlyph.beginUndo() # undo grouping causes crashes

								try:
									if italicAngle and respectItalic:
										# slant the layer copy backwards
										moveDown = transform(shiftY=-halfXHeight).transformStruct()
										skewBack = transform(skew=-italicAngle).transformStruct()
										moveUp = transform(shiftY=halfXHeight).transformStruct()
										copyLayer.applyTransform(moveDown)
										copyLayer.applyTransform(skewBack)
										copyLayer.applyTransform(moveUp)

									#bottomMinY = False;
									#topMostY = False;
									copyPathHeight = 0
									copyAllHeight = 0
									copyAllWidth = 0
									copyAllTopMost = -1000
									copyAllBottomMin = 1000
									copyAllLeftMin = +1000
									copyAllRightMost = -1000


									for copyPath in copyLayer.paths:
										#if copyPath.name == type_name:


										#NEW CODE


										if len(copyLayer.paths) > 0:

											print("Copy is PATH")
											copy = copyPath.nodes

										if len(copyLayer.components) > 0:

											print("Copy is COMPONENT")
											for component in copyLayer.components:
												component.selected = True
											#copyLayer.components[0].selected = True
											copyComponentLayer = copyLayer
											copy = copyLayer.selection


										# Get X-Cordinate of Path
										copyXList = [ n.x for n in copy ]


										# leftMostX = min( copyXList )
										# rightMostX = max( copyXList )

										# copyPathWidth = rightMostX-leftMostX

										# # X-Coordinate of the Center of Selected Path
										# if len(copyLayer.paths) > 0:
										# 	copyPathX = ( leftMostX + rightMostX ) // 2
										# if len(copyLayer.components) > 0:
										# 	copyPathX = copyComponentLayer.bounds.origin.x + copyComponentLayer.bounds.size.width // 2




										if copyAllRightMost < max( copyXList ):
											copyAllRightMost = max( copyXList )

										if copyAllLeftMin > min( copyXList ):
											copyAllLeftMin = min( copyXList)

										copyAllWidth = copyAllRightMost - copyAllLeftMin

										leftMinX = min( copyXList )
										rightMostX = max( copyXList )
										copyPathWidth = max( copyXList )-min( copyXList )

										copyPathWidth = copyAllWidth #rightMostX-leftMinX
										copyPathX = (copyAllRightMost + copyAllLeftMin) // 2
										rightMostX = copyAllRightMost
										leftMinX = copyAllLeftMin




										# Get Y-Cordinate of Path
										copyYList = [ n.y for n in copy ]
										# try:
										# 	if min( copyYList ) < bottomMinY:
										# 		bottomMinY = min( copyYList )
										# 	if topMostY < max( copyXList ):
										# 		topMostY = max( copyYList )
										# except:

										print("copyAllHeight")

										if copyAllTopMost < max( copyYList ):
											copyAllTopMost = max( copyYList )

										if copyAllBottomMin > min( copyYList ):
											copyAllBottomMin = min( copyYList)

										copyAllHeight = copyAllTopMost - copyAllBottomMin

										bottomMinY = min( copyYList )
										topMostY = max( copyYList )
										copyPathHeight = max( copyYList )-min( copyYList )

										copyPathHeight = copyAllHeight #topMostY-bottomMinY
										copyPathY = (copyAllTopMost + copyAllBottomMin) // 2
										topMostY = copyAllTopMost
										bottomMinY = copyAllBottomMin

										# Y-Coordinate of the Center of Selected Path
										#if len(copyLayer.paths) > 0:
										#	copyPathY = ( topMostY + bottomMinY ) // 2

										#if len(copyLayer.components) > 0:
										#	copyPathY = copyComponentLayer.bounds.origin.y + copyComponentLayer.bounds.size.height // 2

										old_path_x = copyPathX
										old_path_y = copyPathY

										#print("copyLayer")
										#print(copyLayer)
										#print(copyLayer.bounds.size.width)

										# print("center")
										# print(copyLayer.bounds.origin.x + copyLayer.bounds.size.width // 2.0)
										old_path_LSB = copyLayer.LSB
										old_path_RSB = copyLayer.RSB

										# old_path_x = copyPath.x
										# old_path_y = copyPath.y


										xMove = eval(evalCodeH) + horizontal_change
										yMove = eval(evalCodeV) + vertical_change

										print("xMove = eval(evalCodeH) + horizontal_change")
										print(evalCodeH)
										print(" " + str(xMove) + " = " + str(eval(evalCodeH)) + " + " + str(horizontal_change))

										print("yMove = eval(evalCodeV) + vertical_change")
										print(evalCodeV)
										print(" " + str(yMove) + " = " + str(eval(evalCodeV)) + " + " + str(vertical_change))

										# Ignore moves relative to bbox if there are no paths:
										# if not copyLayer.paths:
										# 	if "bounds" in evalCodeH:
										# 		xMove = old_path_x

										# 	if "bounds" in evalCodeV:
										# 		yMove = old_path_y

										# Move Nodes / Objects

									if len(originalLayer.paths) > 0:
										print("MOVE MOVE MOVE MOVE MOVE MOVE MOVE")
										print("Original is PATH")
										for path in originalLayer.paths:
											originalPath = path.nodes

											xOffset = xMove - old_path_x
											yOffset = yMove - old_path_y

											print("yOffset = yMove - old_path_y")
											print( str(yMove) + "+" + str(old_path_y))


											for thisNode in originalPath:
												thisNode.x += xOffset

											for thisNode in originalPath:
												thisNode.y += yOffset


											if evalCodeH == "copyPathX":
												originalLayer.LSB = old_path_LSB + horizontal_change
												originalLayer.RSB = old_path_RSB - horizontal_change



									if len(originalLayer.components) > 0:
										print("MOVE MOVE MOVE MOVE MOVE MOVE MOVE")
										print("Original is Component")
										# originalLayer.components[0].selected = True
										for component in originalLayer.components:
											component.selected = True
										originalComponentLayer = originalLayer
										originalPath = originalLayer.selection


										xOffset = xMove - old_path_x
										yOffset = yMove - old_path_y
										print("yOffset = yMove - old_path_y")
										print( str(yMove) + "+" + str(old_path_y))


										for thisNode in originalPath:
											thisNode.x += xOffset

										for thisNode in originalPath:
											thisNode.y += yOffset

										if evalCodeH == "copyPathX":
											originalLayer.LSB = old_path_LSB + horizontal_change
											originalLayer.RSB = old_path_RSB - horizontal_change

										#originalPath = originalLayer.paths[type_name]
										#originalPath.position = NSPoint(xMove, yMove)


										# Only move if the calculated position differs from the original one:
										# originalPath = originalLayer.paths[type_name]
										# if int(old_path_x) != int(xMove) or int(old_path_y) != int(yMove):
										# 	if italicAngle and respectItalic:
										# 		# skew back
										# 		originalPath.position = italicize(NSPoint(xMove, yMove), italicAngle, halfXHeight)
										# 	else:
										# 		originalPath.position = NSPoint(xMove, yMove)
										# 	print("⚓️ %s → %i, %i in layer: %s." % (type_name, originalPath.x, originalPath.y, originalLayer.name))
										# else:
										# 	print("⚓️ %s path unchanged in %s." % (type_name, originalLayer.name))

								except Exception as e:
									print("ERROR: Failed to move path in %s." % thisGlyph.name)
									print(e)
									import traceback
									print(traceback.format_exc())

			except Exception as e:
				raise e
			finally:
				thisFont.enableUpdateInterface()
		print("Done.")

	# def GetAnchorNames(self):
	# 	myAnchorList = []
	# 	selectedLayers = Glyphs.currentDocument.Layers()
	# 	try:
	# 		for thisLayer in selectedLayers:
	# 			AnchorNames = list(thisLayer.paths.keys()) # hack to avoid traceback
	# 			for thisAnchorName in AnchorNames:
	# 				if thisAnchorName not in myAnchorList:
	# 					myAnchorList.append(thisAnchorName)
	# 	except:
	# 		print("Error: Cannot collect path names from the current copy.")

	# 	return sorted(myAnchorList)

	# def SetAnchorNames(self, sender):
	# 	pathList = self.GetAnchorNames()
	# 	self.w.type_name.setItems(pathList)

ObjectMover3()
