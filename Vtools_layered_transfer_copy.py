import bpy

class layered_transfer_copy(bpy.types.Operator):
  '''Process objects BEFORE COPYING them, then paste them in destination scene and run the Layered Transfer Paste.'''
  bl_idname = 'object.layered_transfer_copy'
  bl_label = 'Layred Transfer COPY'
  bl_options = {'REGISTER', 'UNDO'}

  clean_mode = bpy.props.BoolProperty(
    name = 'Clean mode',
    description = 'Revert objects back to original state after copying them.',
    default = True
  )

  def execute(self, context):
      
    def layer_preprocess(obj):
      if obj.name[:8] == '|Layers|':
        print('Layers Skipped for ' + obj.name)
      else:
        # define appendix list with first item
        appendix = ['Layers']
        # go through all layers
        for n in range(0,20):
          # if object uses a layer, append that ID to the appendix
          if obj.layers[n] == True:
            # format n to always have 2 digit layer IDs
            n_2d = format(n,'02d')
            # append it
            appendix.append(n_2d)
        # put together the added string
        string_to_add = ''
        for a in appendix:
          string_to_add = string_to_add + '|' + a
        string_to_add = string_to_add + '_'
        print('Layers Processed for ' + string_to_add + obj.name)

        obj.name = string_to_add + obj.name
    
    def layer_revert(obj):
      tested_name = obj.name[7:]
      # check if the string maches any layer ID and set layers based on that
      # only process things which start with |
      if tested_name[:1] == '|':
        #print(tested_name)
        # as long as the name starts with |, iterate
        while tested_name[:1] == '|':
          # cut out the first character - |
          tested_name = tested_name[1:]
          # get the first characters from the new string (numeric ID)
          layer_ID = tested_name[:2]
          #print(layer_ID)
          # enable layers based on the numeric ID
          #for i in range(0,20):
          #  if layer_ID == layer_list[i]:
          #    obj.layers[i] = layer_ID == layer_list[i] 
          # cut the last 2 characters from the start (numeric ID)
          tested_name = tested_name[2:]
          #print(tested_name)
        obj.name = tested_name[1:]

    # go through all objects and process layer names
    for obj in bpy.context.selected_objects:
      layer_preprocess(obj)
    # copy into buffer
    bpy.ops.view3d.copybuffer()

    # revert back to original state
    if self.clean_mode == True:
      for obj in bpy.context.selected_objects:
        layer_revert(obj)

    return {'FINISHED'}