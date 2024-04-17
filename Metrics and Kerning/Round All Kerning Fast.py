# MenuTitle: Round all kerning (fast)
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Rounds all kerning pairs of the current master (or all masters) according to a multiple (grid unit) provided. Requires vanilla. Build upon script by Harbor Type.
"""

import vanilla
import time
from Foundation import NSNumberFormatter
from GlyphsApp import Glyphs





font = Glyphs.font
currentMaster = font.selectedFontMaster.id


class RoundAllKerning(object):
    key = "com.manuel87.RoundAllKerning"
    windowHeight = 126
    padding = (10, 10, 12)
    buttonHeight = 20
    textHeight = 14
    sizeStyle = 'small'
    masterOptions = (
        "on currently selected master only",
        "on all masters",
    )

    def __init__(self):

        x, y, p = self.padding

        self.w = vanilla.FloatingWindow(
            (280, self.windowHeight),
            "Round All Kerning"
        )

        y += 8

        # UI elements:
        self.w.text_1 = vanilla.TextBox(
            (x, y, 216, self.textHeight),
            "Round all kerning pairs to multiples of",
            sizeStyle=self.sizeStyle
        )
        # y += self.textHeight

        # Multiple
        formatter = NSNumberFormatter.new()
        self.w.multiple = vanilla.EditText(
            (216, y - 3, -p, 19),
            "8",
            sizeStyle=self.sizeStyle,
            formatter=formatter,
            callback=self.SavePreferences
        )
        y += self.textHeight + p - 4

        # Which masters
        self.w.whichMasters = vanilla.RadioGroup(
            (x * 1.5, y, -p, self.buttonHeight * len(self.masterOptions)),
            self.masterOptions,
            sizeStyle=self.sizeStyle,
            callback=self.SavePreferences,
        )
        self.w.whichMasters.getNSMatrix().setToolTip_(
            "Choose which font masters shall be affected.")

        y += self.buttonHeight * len(self.masterOptions)

        # Run Button:
        self.w.runButton = vanilla.Button(
            (80, -20 - 15, -80, -15),
            "Round kerning",
            sizeStyle='regular',
            callback=self.RoundAllKerningMain
        )
        self.w.setDefaultButton(self.w.runButton)

        # Load Settings:
        if not self.LoadPreferences():
            print(
                "Note: 'Round All Kerning' could not load preferences.\
                Will resort to defaults"
            )

        # Open window and focus on it:
        self.w.open()
        self.w.makeKey()

    def SavePreferences(self, sender):
        try:
            Glyphs.defaults[self.key + ".multiple"] = self.w.multiple.get()
        except:
            return False

        return True

    def LoadPreferences(self):
        try:
            Glyphs.registerDefault(self.key + ".multiple", "8")
            Glyphs.registerDefault(self.key + ".whichMasters", 0)

            self.w.multiple.set(Glyphs.defaults[self.key + ".multiple"])
            self.w.whichMasters.set(
                bool(Glyphs.defaults[self.key + ".whichMasters"])
            )
        except:
            return False

        return True

    # def RoundKerningValue(self, kerningValue, base=10):
    #     return int(base * round(float(kerningValue) / base))

    def GetKey(self, glyph_key):
        if glyph_key.startswith("@"):
            return glyph_key
        return font.glyphForId_(glyph_key).name

    def ProcessMaster(self, this_master, master_id):
        print( "\n--------------------\n%s\n--------------------" % this_master.name)
        i=0
        KernDict = dict( font.kerning[master_id] )
        for leftSide in KernDict:
            KernDict[leftSide] = dict(KernDict[leftSide])
        for leftSide in KernDict:   
            for rightSide in KernDict[leftSide]:
                existingValue = int(KernDict[leftSide][rightSide])
                if existingValue < 0: # custom round + no extra function (faster)
                    newValue = int(((existingValue/self.multiple-0.5)*10)/10) * self.multiple 
                else:
                    newValue = int(((existingValue/self.multiple+0.5)*10)/10) * self.multiple  
                if existingValue != newValue :
                    i=i+1
                    font.kerning[master_id][leftSide][rightSide] = newValue # much much faster
                    #font.setKerningForPair( master_id, leftSideName, rightSideName, newValue) # super slow     
        if (i == 0):
            print("all pairs already rounded")
        else:
            print(i, "pair(s) rounded")

    def RoundAllKerningMain(self, sender):
        self.multiple = int(self.w.multiple.get())
        self.whichMasters = self.w.whichMasters.get()
        print("\n\n\n----------------------------------------\nRounding kerning to multiples of: ", self.multiple, "\n----------------------------------------\n")
        start_time = time.time()
        Glyphs.showMacroWindow()

        try:
            font.disableUpdateInterface()
            if self.whichMasters == 1:  # all masters
                for this_master in font.masters:
                    self.ProcessMaster(this_master, this_master.id)
            else:
                self.ProcessMaster(font.selectedFontMaster, font.selectedFontMaster.id)
        finally:
            font.enableUpdateInterface()
            print("\n\n--------------------\nExecution time\n--------------------\n%s seconds" % (time.time() - start_time))


RoundAllKerning()



