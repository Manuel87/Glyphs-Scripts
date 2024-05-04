#MenuTitle: Edit Next Glyph, same layer
# encoding: utf-8

# build upon "Edit Next Glyph" by Tim Ahrens & "Next Layer in Selection" by Alex Slobzheninov


__doc__="""
Activates the next glyph in the tab for editing and also stays in the same Layer (any kind of layer, not just masters)
"""

font = Glyphs.font

direction = 0 #0 = stay within layer # -1 = previous, 1 = next
# Todo: Getting rid of all the unnecessary code, as we arent switching layers


def go_to_next_glyph():
	if font:
		tab = font.currentTab
		if tab:
			# move cursor:
			# (adopted from https://glyphsapp.com/news/glyphs-3-2-released)
			newPosition = (tab.layersCursor + 1) % (len(tab.layers))
			tab.layersCursor = newPosition
			# re-center glyph:
			vp = tab.viewPort
			vp.origin.x = tab.selectedLayerOrigin.x + 0.5 * ( font.selectedLayers[0].width * tab.scale - vp.size.width )
			if newPosition == 0:
				print()
				# ^ very strange: if we don’t do this
				#   then the glyph is not centred correctly
				#   if the text cursor is active
			
			# TODO: in case the new glyph is on a different line, also adjust y 

			# Apply Layer
			# apply_layer_to_selected_glyphs(selected_layer,selected_layer)


			switch_layers(direction) # this works great, but messes up the viewport position
			tab.viewPort = vp




def get_prev_or_next_layer(layer, direction):
	try:
		layers = layer.parent.sortedLayers()
		layer_index = layers.indexOfObject_(layer)
		layer_index += direction
		if layer_index < 0:
			layer_index = len(layers) - 1
		elif layer_index >= len(layers):
			layer_index = 0
		new_layer = layers[layer_index]
		return new_layer
	except:
		return None


def apply_layer_to_selected_glyph(new_layer):
	new_selected_layers = []
	l = layer.parent.layerForName_(new_layer.name)
	if l:
		new_selected_layers.append(l)
	else:
		new_selected_layers.append(layer)
	return new_selected_layers



def apply_layer_to_selected_glyphs(new_layer, selected_layers):

	new_selected_layers = []
	for layer in selected_layers:
		l = layer.parent.layerForName_(new_layer.name)
		if l:
			new_selected_layers.append(l)
		else:
			new_selected_layers.append(layer)
	return new_selected_layers


def set_master(font, tab, text_cursor, text_range, toggle, master_index):
	# select the layers
	tab.textCursor = text_cursor
	tab.textRange = text_range
	# set master index
	font.masterIndex = master_index + toggle
	font.masterIndex -= toggle


def set_master_layers_to_master(font, tab, master):
	# get user's selection to reset later
	current_text_cursor = tab.textCursor
	current_text_range = tab.textRange
	master_index = font.masters.index(master)
	
	# toggle master to some other master and back, otherwise it doesn't apply
	toggle = -1 if 0 < master_index else 1
	
	# select old master layers and apply master
	text_cursor = None
	text_range = 0
	for i, layer in enumerate(tab.layers):
		if layer.isMasterLayer and layer.master == master:
			if text_cursor is None:
				text_cursor = i
			text_range += 1
		else:
			if text_cursor is not None:
				set_master(font, tab, text_cursor, text_range, toggle, master_index)
			# reset selection
			text_cursor = None
			text_range = 0
	if text_cursor is not None:
		set_master(font, tab, text_cursor, text_range, toggle, master_index)

	# set original user's selection
	tab.textCursor = current_text_cursor
	tab.textRange = current_text_range


def switch_layers(direction = 1):
	font = Glyphs.font
	if not font or not font.currentTab or not font.selectedLayers:
		return
	# get initial tab layers
	tab = font.currentTab
	initial_tab_layers = copy(tab.layers)

	# get text selection
	selection_org = tab.textCursor - 1

	selection_now = tab.textCursor
	selection_end = tab.textCursor + tab.textRange
	first_layer = tab.layers[selection_org]
	try:
		new_first_layer = get_prev_or_next_layer(first_layer, direction)
	except:
		print(traceback.format_exc())
		return


	# apply the new layer to all selected glyphs; skip if not possible
	selected_layers = tab.layers[selection_now : selection_end] if tab.textRange else [font.selectedLayers[0]]
	new_selected_layers = apply_layer_to_selected_glyphs(new_first_layer, selected_layers)
	
	# apply layers to the tab
	if tab.textRange:
		new_tab_layers = initial_tab_layers[:selection_now] + new_selected_layers + initial_tab_layers[selection_end:]
	else:
		new_tab_layers = initial_tab_layers[:selection_now] + new_selected_layers + initial_tab_layers[selection_now + 1:]
	tab.layers = new_tab_layers

	set_master_layers_to_master(font, tab, font.masters[tab.masterIndex])




go_to_next_glyph()