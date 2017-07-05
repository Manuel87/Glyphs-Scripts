#MenuTitle: Show Prev Master
# -*- coding: utf-8 -*-
__doc__="""
Jumps to previous Master.
"""

import GlyphsApp
from Foundation import NSApplication

Font = Glyphs.font
Font.parent.windowController().setMasterIndex_(Font.masterIndex - 1)
