#MenuTitle: Generate Instances into one .glyphs file
# -*- coding: utf-8 -*-
__doc__="""
Generate all active Instances into a single .glyphs file, while keeping all inactive instances intact – e.g. to reset the weight of the current 'Regular' Master.

Notes
- CAUTION: not sure what happens to brace and bracket layers with this
"""
# Author: Manuel von Gebhardi

import GlyphsApp

original_font = Glyphs.fonts[0]
instances_as_fonts = []
all_original_instances = []

for instance in original_font.instances:
	if (instance.active):
		instance_font = instance.interpolatedFont

		# Current workaround to avoid the not-so-clever automatic naming
		# General suggestion to Georg: disable the automatic naming and instead add a separate name-field for master!
		instance_font.masters[0].weight = "Regular" #instance.weight # avoiding strange namings
		instance_font.masters[0].width = "Regular" #instance.width # avoiding strange namings
		instance_font.masters[0].italicAngle = 0 #solving naming issue with "italic italic"//original value needs to be manually entered after the script :/	#temp_angle = instance_font.masters[0].italicAngle #

		# Copy Interpolation Values
		instance_font.masters[0].weightValue = instance.weightValue
		instance_font.masters[0].widthValue = instance.widthValue
		instance_font.masters[0].customValue = instance.customValue

		# Name
		instance_font.masters[0].customName = instance.name
		print instance_font.masters[0].customName
		print instance_font.masters[0].weightValue

		instances_as_fonts.append(instance_font)

	all_original_instances.append(instance)


# Create new Glyphs File
Glyphs.fonts.append(instances_as_fonts[0])
new_font = Glyphs.fonts[0]

# Add new Masters, except first (already there)
for i in range(1,len(instances_as_fonts)): # 1 instead of 0, hence adding all except the first one
	new_font.addFontAsNewMaster_(instances_as_fonts[i].masters[0])


# Add all original instances
new_font.instances = () # empty Instances first
for instance in all_original_instances:
	new_font.instances.append(instance.copy())


