#MenuTitle: Show Next Master
# -*- coding: utf-8 -*-
__doc__="""
Jumps to next Master.
"""

import GlyphsApp
from Foundation import NSApplication

Font = Glyphs.font
Font.parent.windowController().setMasterIndex_(Font.masterIndex + 1)
