#MenuTitle: Show Duplicates
# -*- coding: utf-8 -*-
"""Shows Glyphs with the same name"""

import vanilla
import GlyphsApp

names = set()
duplicates = set()
for glyph in Font.glyphs:
	name = glyph.name
	if name in names:
		duplicates.add(name)
	names.add(name)
print(duplicates)
