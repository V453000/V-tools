import bpy

class generate_render_nodes(bpy.types.Operator):
  '''Generate Render Nodes from RenderLayers.'''
  bl_idname = 'nodes.generate_render_nodes'
  bl_label = 'Generate Render Nodes'
  bl_options = {'REGISTER', 'UNDO'}



  AO_identifier_use = bpy.props.BoolProperty(
    name = 'Use AO',
    description = 'Save AO pass from specified RenderLayers to individual folder.',
    default = True
  )
  AO_identifier_position = bpy.props.EnumProperty(
    name = 'AO Identifier position',
    description = 'Select where in the RenderLayer name is the AO identifier.',
    items = [
      ('back', 'back',''),
      ('front', 'front','')
    ]
  )
  AO_identifier = bpy.props.StringProperty(
    name = 'AO Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering AO.',
    default = 'main'
  )


  shadow_identifier_use = bpy.props.BoolProperty(
    name = 'Use Shadow',
    description = 'Save Shadow pass from specified RenderLayers to individual folder.',
    default = True
  )
  shadow_identifier_position = bpy.props.EnumProperty(
    name = 'Shadow Identifier position',
    description = 'Select where in the RenderLayer name is the Shadow identifier.',
    items = [
      ('back', 'back',''),
      ('front', 'front','')
    ]
  )
  shadow_identifier = bpy.props.StringProperty(
    name = 'Shadow Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Shadow.',
    default = 'shadow'
  )
  

  height_identifier_use = bpy.props.BoolProperty(
    name = 'Use Height',
    description = 'Save Height pass from specified RenderLayers to individual folder.',
    default = True
  )
  height_identifier_position = bpy.props.EnumProperty(
    name = 'Height Identifier position',
    description = 'Select where in the RenderLayer name is the Height identifier.',
    items = [
      ('back', 'back',''),
      ('front', 'front','')
    ]
  )
  height_identifier = bpy.props.StringProperty(
    name = 'Height Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Height.',
    default = 'height'
  )

  normal_identifier_use = bpy.props.BoolProperty(
    name = 'Use Z-Normal',
    description = 'Save Z-Normal pass from specified RenderLayers to individual folder.',
    default = True
  )
  normal_identifier_position = bpy.props.EnumProperty(
    name = 'Z-Normal Identifier position',
    description = 'Select where in the RenderLayer name is the Z-Normal identifier.',
    items = [
      ('back', 'back',''),
      ('front', 'front','')
    ]
  )
  normal_identifier = bpy.props.StringProperty(
    name = 'Z-Normal Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Z-Normal.',
    default = 'Z-normal'
  )

  remove_existing_nodes = bpy.props.BoolProperty(
    name = 'Remove Existing Nodes',
    description = 'Choose whether the function should remove existing nodes, or only add new.',
    default = True
  )
  regenerate_shadow_shitter = bpy.props.BoolProperty(
    name = 'Regenerate Shadow Shitter',
    description = 'Delete the nodes in current Shadow Shitter and create new ones.',
    default = False
  )  
  regenerate_preview_shitter = bpy.props.BoolProperty(
    name = 'Regenerate Preview Shitter',
    description = 'Delete the nodes in current preview Shitter and create new ones.',
    default = False
  )
  regenerate_height_material = bpy.props.BoolProperty(
    name = 'Regenerate HEIGHT material',
    description = 'Delete the nodes in current HEIGHT material and create new ones.',
    default = False
  )  
  regenerate_normal_material = bpy.props.BoolProperty(
    name = 'Regenerate Z-NORMAL',
    description = 'Delete the nodes in current Z-NORMAL material and create new ones.',
    default = False
  )  

  def execute(self, context):
    # ------------------------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------------------------

    render_layers_from_scene = bpy.context.scene.name   
    render_nodes_to_scene = bpy.context.scene.name

    output_folder = "//OUTPUT\\"
    appendix_AO =     self.AO_identifier #'main'
    appendix_shadow = self.shadow_identifier #'shadow' 
    appendix_height = self.height_identifier #'height' 
    appendix_normal = self.normal_identifier #'Z-normal' 

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    # make all scenes use compositor nodes
    bpy.data.scenes[render_layers_from_scene].use_nodes = True
    bpy.data.scenes[render_nodes_to_scene].use_nodes = True

    # read Render Layers
    # switch scene to source
    bpy.context.screen.scene = bpy.data.scenes[render_layers_from_scene]
    # go through render layers and add them to a list
    render_layer_list = []
    print('Reading render layers:')
    for render_layer in bpy.context.scene.render.layers:
      print(render_layer.name)
      render_layer_list.append(render_layer.name)








    if bpy.data.materials.get('HEIGHT') is None:
      height_material_existed = False
    else:
      height_material_existed = True
    # check if HEIGHT material exists, if not, create it
    if bpy.data.materials.get('HEIGHT') is None:
      # create new HEIGHT material
      print('HEIGHT material does not exist, creating...')
      height_mtl = bpy.data.materials.new('HEIGHT')
      height_mtl.use_nodes = True
      height_nodes = height_mtl.node_tree.nodes
    if self.regenerate_height_material == True or height_material_existed == False:
      # remove all nodes first
      for node in height_nodes:
        height_nodes.remove(node)
      
      # create new nodes
      geometry_node = height_nodes.new(type = 'ShaderNodeNewGeometry')
      geometry_node.name = 'HEIGHT-Geometry'
      geometry_node.label = geometry_node.name
      geometry_node.location = (-400,0)
      
      mapping_node = height_nodes.new(type = 'ShaderNodeMapping')
      mapping_node.name = 'HEIGHT-Mapping'
      mapping_node.label = mapping_node.name
      mapping_node.location = (-200,0)
      mapping_node.scale[2] = 0.1

      separateXYZ_node = height_nodes.new(type = 'ShaderNodeSeparateXYZ')
      separateXYZ_node.name = 'HEIGHT-SeparateXYZ'
      separateXYZ_node.label = separateXYZ_node.name
      separateXYZ_node.location = (180,0)

      emission_node = height_nodes.new(type = 'ShaderNodeEmission')
      emission_node.name = 'HEIGHT-Emission'
      emission_node.label = emission_node.name
      emission_node.location = (380,0)

      material_output = height_nodes.new(type = 'ShaderNodeOutputMaterial')
      material_output.name = 'HEIGHT-MaterialOutput'
      material_output.label = material_output.name
      material_output.location = (580,0)

      height_mtl.node_tree.links.new(geometry_node.outputs[0], mapping_node.inputs[0])
      height_mtl.node_tree.links.new(mapping_node.outputs[0], separateXYZ_node.inputs[0])
      height_mtl.node_tree.links.new(separateXYZ_node.outputs[2], emission_node.inputs[0])
      height_mtl.node_tree.links.new(emission_node.outputs[0], material_output.inputs[0])
    
    if bpy.data.materials.get('Z-NORMAL') is None:
      normal_material_existed = False
    else:
      normal_material_existed = True
    # check if Z-NORMAL material exists, if not, create it
    if bpy.data.materials.get('Z-NORMAL') is None:
      normal_mtl = bpy.data.materials.new('Z-NORMAL')
      normal_mtl.use_nodes = True
      normal_nodes = normal_mtl.node_tree.nodes
    # generate nodes for Z-NORMAL material
    if self.regenerate_normal_material == True or normal_material_existed == False:
      # remove all nodes first
      for node in normal_nodes:
        normal_nodes.remove(node)
      # create new nodes
      geometry_node = normal_nodes.new(type = 'ShaderNodeNewGeometry')
      geometry_node.name = 'Z-NORMAL-Geometry'
      geometry_node.label = geometry_node.name
      geometry_node.location = (-400, 0)

      separateXYZ_node = normal_nodes.new(type = 'ShaderNodeSeparateXYZ')
      separateXYZ_node.name = 'Z-NORMAL-SeparateXYZ'
      separateXYZ_node.label = separateXYZ_node.name
      separateXYZ_node.location = (-200, 0)

      emission_node = normal_nodes.new(type = 'ShaderNodeEmission')
      emission_node.name = 'Z-NORMAL-Emission'
      emission_node.label = emission_node.name
      emission_node.location = (0, 0)

      material_output = normal_nodes.new(type = 'ShaderNodeOutputMaterial')
      material_output.name = 'Z-NORMAL-MaterialOutput'
      material_output.label = material_output.name
      material_output.location = (200, 0)

      normal_mtl.node_tree.links.new(geometry_node.outputs[1], separateXYZ_node.inputs[0])
      normal_mtl.node_tree.links.new(separateXYZ_node.outputs[2], emission_node.inputs[0])
      normal_mtl.node_tree.links.new(emission_node.outputs[0], material_output.inputs[0])
    








    # make sure AO render layers have AO on, and shadow render layers have shadow on and height layers have height material override
    appendix_AO_char_count = len(appendix_AO)
    appendix_shadow_char_count = len(appendix_shadow)
    appendix_height_char_count = len(appendix_height)
    appendix_normal_char_count = len(appendix_normal)

    for render_layer in bpy.context.scene.render.layers:
      render_layer_name = render_layer.name
      
      if self.AO_identifier_position == 'back':
        render_layer_appendix_AO = render_layer_name[-appendix_AO_char_count:]
      if self.AO_identifier_position == 'front':
        render_layer_appendix_AO = render_layer_name[:appendix_AO_char_count]

      if self.shadow_identifier_position == 'back':
        render_layer_appendix_shadow = render_layer_name[-appendix_shadow_char_count:]
      if self.shadow_identifier_position == 'front':
        render_layer_appendix_shadow = render_layer_name[:appendix_shadow_char_count]

      if self.height_identifier_position == 'back':
        render_layer_appendix_height = render_layer_name[-appendix_height_char_count:]
      if self.height_identifier_position == 'front':
        render_layer_appendix_height = render_layer_name[:appendix_height_char_count]
      
      if self.normal_identifier_position == 'back':
        render_layer_appendix_normal = render_layer_name[-appendix_normal_char_count:]
      if self.normal_identifier_position == 'front':
        render_layer_appendix_normal = render_layer_name[:appendix_normal_char_count]


      if render_layer_appendix_AO == appendix_AO:
        print('AO appendix detected')
        if render_layer.use_pass_ambient_occlusion == False:
          print(str(render_layer_name) + ' has appendix "' + appendix_AO + '" but does not have AO pass activated. Activating...')
          render_layer.use_pass_ambient_occlusion = True
      
      if render_layer_appendix_shadow == appendix_shadow:
        print('shadow appendix detected')
        if render_layer.use_pass_shadow == False:
          print(str(render_layer_name) + ' has appendix "' + appendix_shadow + '" but does not have shadow pass activated. Activating...')
          render_layer.use_pass_shadow = True
      
      if render_layer_appendix_height == appendix_height:
        print('height appendix detected')
        if render_layer.material_override != bpy.data.materials['HEIGHT']:
          print(str(render_layer_name) + ' has appendix "' + appendix_height + '" but does not have HEIGHT material override activated. Activating...')
          render_layer.material_override = bpy.data.materials['HEIGHT']
      
      if render_layer_appendix_normal == appendix_normal:
        print('normal appendix detected')
        if render_layer.material_override != bpy.data.materials['Z-NORMAL']:
          print(str(render_layer_name) + ' has appendix "' + appendix_normal + '" but does not have Z-NORMAL material override activated. Activating...')
          render_layer.material_override = bpy.data.materials['Z-NORMAL']


    # destroy shadow shitter if desired by settings
    if self.regenerate_shadow_shitter == True:
      if bpy.data.node_groups.get('ShadowShitter') is not None:
        bpy.data.node_groups.remove(bpy.data.node_groups['ShadowShitter'])
    # check if ShadowShitter exists, if not, create it
    nodes = bpy.context.scene.node_tree.nodes
    if bpy.data.node_groups.get('ShadowShitter') is None:
      print('ShadowShitter does not exist, creating...')
      shadow_shitter = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = 'ShadowShitter')

      shadow_shitter.inputs.new('NodeSocketFloat', 'Shadow Pass')
      input_node = shadow_shitter.nodes.new('NodeGroupInput')
      input_node.location = (-200,0)

      shadow_shitter.outputs.new('NodeSocketFloat', 'Shadow')
      output_node = shadow_shitter.nodes.new('NodeGroupOutput')
      output_node.location = (600,0)

      #subtract_node = shadow_shitter.nodes.new(type="CompositorNodeMixRGB")
      #subtract_node.name = 'ShadowShitter-subtract-node'
      #subtract_node.label = 'ShadowShitter-subtract-node'
      #subtract_node.location = (0,0)
      #subtract_node.blend_type = 'SUBTRACT'

      alpha_over_node = shadow_shitter.nodes.new(type="CompositorNodeAlphaOver")
      alpha_over_node.name = 'ShadowShitter-alpha-over-node'
      alpha_over_node.label = 'ShadowShitter-alpha-over-node'
      alpha_over_node.location = (0,0)

      invert_node = shadow_shitter.nodes.new(type="CompositorNodeInvert")
      invert_node.name = 'ShadowShitter-invert-node'
      invert_node.label = 'ShadowShitter-invert-node'
      invert_node.location = (200,0)

      set_alpha_node = shadow_shitter.nodes.new(type="CompositorNodeSetAlpha")
      set_alpha_node.name = 'ShadowShitter-set-alpha-node'
      set_alpha_node.label = 'ShadowShitter-set-alpha-node'
      set_alpha_node.location = (400,0)

      shadow_shitter.links.new(input_node.outputs[0], alpha_over_node.inputs[2])
      shadow_shitter.links.new(alpha_over_node.outputs[0], invert_node.inputs[1])
      shadow_shitter.links.new(invert_node.outputs[0], set_alpha_node.inputs[1])
      shadow_shitter.links.new(set_alpha_node.outputs[0], output_node.inputs[0])
      print('ShadowShitter successfully created!')



    # destroy preview shitter if desired by settings
    if self.regenerate_preview_shitter == True:
      if bpy.data.node_groups.get('PreviewShitter') is not None:
        bpy.data.node_groups.remove(bpy.data.node_groups['PreviewShitter'])
    # check if preview shitter exists, if not, create it
    nodes = bpy.context.scene.node_tree.nodes
    if bpy.data.node_groups.get('PreviewShitter') is None:
      preview_shitter = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = 'PreviewShitter')

      preview_shitter.inputs.new('NodeSocketFloat', 'Image')
      input_node = preview_shitter.nodes.new('NodeGroupInput')
      input_node.name = 'PreviewShitter-Input'
      input_node.label = input_node.name
      input_node.location = (-200, 0)

      preview_shitter.outputs.new('NodeSocketFloat', 'Preview')
      '''
      preview_shitter.outputs.new('NodeSocketFloat', 'Full size')
      preview_shitter.outputs.new('NodeSocketFloat', '50% size')
      preview_shitter.outputs.new('NodeSocketFloat', '25% size')
      '''

      output_node = preview_shitter.nodes.new('NodeGroupOutput')
      output_node.name = 'PreviewShitter-Output'
      output_node.label = output_node.name
      output_node.location = (200,0)
      '''
      transform_node_1 = preview_shitter.nodes.new('CompositorNodeTransform')
      transform_node_1.filter_type = 'BILINEAR'
      transform_node_1.inputs[4].default_value = 0.5
      transform_node_1.name = 'PreviewShitter-Transform-1'
      transform_node_1.label = transform_node_1.name
      transform_node_1.location = (0, -50)
      
      transform_node_2 = preview_shitter.nodes.new('CompositorNodeTransform')
      transform_node_2.filter_type = 'BILINEAR'
      transform_node_2.inputs[4].default_value = 0.25
      transform_node_2.name = 'PreviewShitter-Transform-2'
      transform_node_2.label = transform_node_1.name
      transform_node_2.location = (0, -250)

      #link the nodes
      preview_shitter.links.new(input_node.outputs[0], output_node.inputs[0])
      preview_shitter.links.new(input_node.outputs[0], transform_node_1.inputs[0])
      preview_shitter.links.new(input_node.outputs[0], transform_node_2.inputs[0])
      preview_shitter.links.new(transform_node_1.outputs[0], output_node.inputs[1])
      preview_shitter.links.new(transform_node_2.outputs[0], output_node.inputs[2])
      '''

    # switch scene to destination and make sure nodes are allowed
    bpy.context.screen.scene = bpy.data.scenes[render_nodes_to_scene]
    bpy.context.scene.use_nodes = True

    # clear all current composite nodes (mainly for debug)
    if self.remove_existing_nodes == True:
      for node in bpy.context.scene.node_tree.nodes:
        print('Removing ' + node.name)
        bpy.context.scene.node_tree.nodes.remove(node)

    nodes = bpy.context.scene.node_tree.nodes
    x_count = 0
    y_count = 0
    x_multiplier = 200
    y_multiplier = -400

    for render_layer_name in render_layer_list:
      
      render_layer_is_AO = False
      render_layer_is_shadow = False
      render_layer_is_normal = False


      # shadow appendix or suffix
      appendix_or_suffix_shadow = -1 # -1 for appendix, 1 for suffix
      if self.shadow_identifier_position == 'front':
        appendix_or_suffix_shadow = 1
      if self.shadow_identifier_position == 'back':
        appendix_or_suffix_shadow = -1

      # filter AO identifier
      appendix_AO_char_count = len(appendix_AO)
      if self.AO_identifier_position == 'back':
        node_appendix_AO = render_layer_name[-appendix_AO_char_count:]
      if self.AO_identifier_position == 'front':
        node_appendix_AO = render_layer_name[:appendix_AO_char_count]

      if node_appendix_AO == appendix_AO:
        render_layer_is_AO = True

      # filter shadow identifier
      appendix_shadow_char_count = len(appendix_shadow)
      if self.shadow_identifier_position == 'back':
        node_appendix_shadow = render_layer_name[-appendix_shadow_char_count:]
      if self.shadow_identifier_position == 'front':
        node_appendix_shadow = render_layer_name[:appendix_shadow_char_count]

      if node_appendix_shadow == appendix_shadow:
        render_layer_is_shadow = True

      # filter normal identifier
      appendix_normal_char_count = len(appendix_normal)
      if self.normal_identifier_position == 'back':
        node_appendix_normal = render_layer_name[-appendix_normal_char_count:]
      if self.normal_identifier_position == 'front':
        node_appendix_normal = render_layer_name[:appendix_normal_char_count]

      if node_appendix_normal == appendix_normal:
        render_layer_is_normal = True



      # create input node
      input_node = nodes.new('CompositorNodeRLayers')
      input_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      input_node.name = 'render-layer-' + render_layer_name
      input_node.label = 'render-layer-' + render_layer_name
      input_node.scene = bpy.data.scenes[render_layers_from_scene]
      input_node.layer = render_layer_name
      
      # add x for next node
      x_count += 1

      # create output node
      output_node = nodes.new('CompositorNodeOutputFile')
      output_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      output_node.name = 'file-output-' + render_layer_name
      output_node.label = 'file-output-' + render_layer_name

      output_node.base_path = output_folder + bpy.context.scene.name + '\\' + bpy.context.scene.name + '_' + render_layer_name

      # create extra output node for AO
      if render_layer_is_AO == True and self.AO_identifier_use == True:
        output_node_AO = nodes.new('CompositorNodeOutputFile')
        output_node_AO.location = (x_count*x_multiplier, y_count*y_multiplier - 140)
        output_node_AO.name = 'file-output-' + render_layer_name + '-AO'
        output_node_AO.label = 'file-output-' + render_layer_name + '-AO'

        output_node_AO.file_slots.remove(output_node_AO.inputs[0])
        output_node_AO.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '-AO' + '_')

        output_node_AO.base_path = output_folder + bpy.context.scene.name + '\\' + bpy.context.scene.name + '_' + render_layer_name + '-AO'

      # put x pack to normal for next row, and add y for next row
      x_count -= 1
      y_count += 1
      # remove output node default input socket
      output_node.file_slots.remove(output_node.inputs[0])
            # add output node input socket
      output_node.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '_')

      # exception to change to shadow pass
      if render_layer_is_shadow == True and self.shadow_identifier_use == True:
        print(node_appendix_shadow)
        shadow_shitter = nodes.new('CompositorNodeGroup')
        shadow_shitter.node_tree = bpy.data.node_groups['ShadowShitter']
        #bpy.context.scene.node_tree.links.new(input_node.outputs[3], output_node.inputs[0])
        x_count += 1
        y_count -= 0.5
        shadow_shitter.location = (x_count*x_multiplier, y_count*y_multiplier)
        x_count -= 1
        y_count += 0.5

        index_shadow = input_node.outputs.find('Shadow')
        
        bpy.context.scene.node_tree.links.new(input_node.outputs[index_shadow], shadow_shitter.inputs[0])
        bpy.context.scene.node_tree.links.new(shadow_shitter.outputs[0], output_node.inputs[0])

        continue

      # exception to add AO pass
      if render_layer_is_AO == True and self.AO_identifier_use == True:
        print(node_appendix_AO)
        bpy.context.scene.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])
        
        # connect to output_node_AO
        #output_node.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '-AO' + '_')
        index_AO = input_node.outputs.find('AO')
        bpy.context.scene.node_tree.links.new(input_node.outputs[index_AO], output_node_AO.inputs[0])
        continue







      
      # link the nodes
      bpy.context.screen.scene.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])

      print(render_layer_name)

    return {'FINISHED'}






