#MenuTitle: Import images into glyphs by filename
# -*- coding: utf-8 -*-
__doc__="""
Creates glyphs from image filenames and imports those images into a coresponding Glyph and currently selected Master.
"""

import os
import GlyphsApp
from vanilla import *

class EditTextDemo(object):
	# interface
	def __init__(self):
		self.w = Window((800, 200), title="Import Many Images")
		self.w.box = Box((10, 45, -210, 60))
		self.w.box2 = Box((600, 45, -10, 60))
		self.w.instruction = TextBox((10, 10, -10, 22), text="Please specify file naming scheme, file extension, path to images.")
		self.w.line2 = HorizontalLine((10, 35, -10, 1))
		self.w.box2.extensiontext = TextBox((10, 0, -10, 22), text="Extension")
		self.w.box2.extension = EditText((10, 20, 130, 22), placeholder=".jpeg")
		self.w.path = TextBox((10, 115, -10, 22))
		self.w.pickPath = Button((10, 140, -10, 20), "Choose Path to Images", callback=self.pickPath) # Choose Path Button
		self.w.testButton = Button((220, 170, -10, 20), "Place Images", callback=self.placeImages) # Place Images Button
		self.w.createGlyphs = Button((10, 170, 200, 20), "Create Glyphs", callback=self.createGlyphs) # Create Glyphs Button
		self.w.box.method = RadioGroup((10, 5, -10, 40),
                                ["By Unicode Code Point [00E4]", "By Glyph Name [adieresis]"])

		self.w.box.method.set(1)
		self.w.open()
    # function for Choose Path button
	def pickPath(self, sender):
		pickpath = GetFolder("Please choose a folder with images") + '/'
		self.w.path.set(pickpath)
	# function for Create Glyphs button
	def createGlyphs(self, sender):
		pickpath = self.w.path.get()
		pickmethod = self.w.box.method.get()
		pickextension = self.w.box2.extension.get()
		if pickextension == "":
			pickextension = self.w.box2.extension.getPlaceholder()
		for file in os.listdir(pickpath):
			if file.endswith(pickextension):
				rfile = file.replace(pickextension, "")
				if pickmethod == 0:
					Glyphs.font.glyphs.append(GSGlyph("uni" + rfile))
				if pickmethod == 1:
					Glyphs.font.glyphs.append(GSGlyph(rfile))
	# function for Place Images button
	def placeImages(self, sender):
		pickpath = self.w.path.get()
		pickmethod = self.w.box.method.get()
		pickextension = self.w.box2.extension.get()
		if pickextension == "":
			pickextension = self.w.box2.extension.getPlaceholder()

		masterID = Glyphs.font.masters[Glyphs.font.masterIndex].id
		for glyph in Glyphs.font.glyphs:
			if pickmethod == 0:
				if glyph.unicode:
					layer = glyph.layers[masterID]
					layer.backgroundImage = GSBackgroundImage(pickpath + glyph.unicode + pickextension)
			if pickmethod == 1:
				if glyph.name:
					layer = glyph.layers[masterID]
					layer.backgroundImage = GSBackgroundImage(pickpath + glyph.name + pickextension)

EditTextDemo()
