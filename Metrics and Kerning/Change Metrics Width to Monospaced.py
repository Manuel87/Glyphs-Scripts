#MenuTitle: Change Metrics Width to Monospaced
# -*- coding: utf-8 -*-
"""Make selected glyphs monospaced."""

import vanilla
import GlyphsApp
print("mystart");
class ChangeMetricsToMono( object ):
	def __init__( self ):
		self.w = vanilla.FloatingWindow( (430, 60), "Make Metrics of Selected Glyphs monospaced", minSize=(430, 60), maxSize=(600, 60), autosaveName="com.manuel.ChangeMetricsToMono.mainwindow" )

		self.w.text_1 = vanilla.TextBox( (15, 12+2, 200, 14), "New monospaced width:", sizeStyle='small' )
		self.w.text_3 = vanilla.TextBox( (-190, 12+2, 170, 14), "units", sizeStyle='small' )
		#self.w.LSB = vanilla.CheckBox( (15+55,    12, 40, 18), "LSB", value=True, sizeStyle='small', callback=self.SavePreferences )
		#self.w.RSB = vanilla.CheckBox( (15+55+45, 12, 40, 18), "RSB", value=True, sizeStyle='small', callback=self.SavePreferences )
		self.w.changeValue = vanilla.EditText( (180, 12, -196, 15+3), "1000.0", sizeStyle = 'small')

		self.w.runButton    = vanilla.Button((-90,    12-1, -15, 19), "Change", sizeStyle='small', callback=self.ChangeMetricsToMonoMain )
		#self.w.revertButton = vanilla.Button((-90-80, 12-1, -95, 19), "Revert", sizeStyle='small', callback=self.ChangeMetricsToMonoMain )

		#self.w.setDefaultButton( self.w.runButton )

	#	try:
	#		self.LoadPreferences( )
	#	except:
		pass

		self.w.open()

	#def SavePreferences( self, sender ):
	#	try:
			#Glyphs.defaults["com.manuel.ChangeMetricsToMono.LSB"] = self.w.LSB.get()
			#Glyphs.defaults["com.manuel.ChangeMetricsToMono.LSB"] = self.w.RSB.get()
			#Glyphs.defaults["com.manuel.ChangeMetricsToMono.changeValue"] = self.w.changeValue.get()
	#	except:
	#		return False

	#	return True

	#def LoadPreferences( self ):
	#	try:
			#self.w.LSB.set( Glyphs.defaults["com.manuel.ChangeMetricsToMono.LSB"] )
			#self.w.RSB.set( Glyphs.defaults["com.manuel.ChangeMetricsToMono.RSB"] )
			#self.w.changeValue.set( Glyphs.defaults["com.manuel.ChangeMetricsToMono.changeValue"] )
	#	except:
	#		return False

	#	return True

	def ChangeMetricsToMonoMain( self, sender ):
		try:
			print("try")
			Font = Glyphs.font
			selectedLayers = Font.selectedLayers

			newWidth = float( self.w.changeValue.get() )

			#changeLSB = self.w.LSB.get()
			#changeRSB = self.w.RSB.get()
			#print("try2")

			#changeWidth = 1.1
			#print(changeWidth)



			#change = ( 100.0 + float( self.w.changeValue.get() ) ) / 100.0

			#if sender == self.w.revertButton:
			#	change = 1.0 / change

			#if changeLSB:
			for thisLayer in selectedLayers:
				changeValue = (newWidth - thisLayer.width) / 2
				print("")
				print("changeValue")
				print(changeValue)
				if (changeValue == 0.5):
					thisLayer.LSB += 0
					thisLayer.RSB += 1
				elif (changeValue == -0.5):
					thisLayer.LSB += 0
					thisLayer.RSB += -1
				else:
					thisLayer.LSB += changeValue
					thisLayer.RSB += changeValue







				#changeWidth = thisLayer.width
				#print("try3")
				#print(changeWidth)
				#thisLayer.LSB *= change

			#if changeRSB:
			#	for thisLayer in selectedLayers:
			#		thisLayer.RSB *= change

			#if not self.SavePreferences( self ):
			#	print("Note: could not write preferences.")

			# self.w.close()
		except Exception as e:
			raise e

ChangeMetricsToMono()
