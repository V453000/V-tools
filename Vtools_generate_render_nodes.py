import bpy
import os
import collections

LinkList = collections.namedtuple('LinkList', ['from_node', 'to_node', 'from_socket', 'to_socket'])

class generate_render_nodes(bpy.types.Operator):
  '''Generate Render Nodes from RenderLayers.'''
  bl_idname = 'nodes.generate_render_nodes'
  bl_label = 'Generate Render Nodes'
  bl_options = {'REGISTER', 'UNDO'}



  resizer_use = bpy.props.EnumProperty(
    name = 'Resizer',
    description = 'Choose whether ResizeShitter automatically downscales the outputs.',
    items = [
      #identifier     #name             #desc  #icon             #ID
      ('OFF'         , 'OFF'           ,'' , 'PANEL_CLOSE'     , 0),
      ('ONLY PREVIEW', 'ONLY PREVIEW'  ,'' , 'FILE_TICK'       , 1),
      ('ALL OUTPUTS' , 'ALL OUTPUTS'   ,'' , 'SCENE'           , 2)
    ],
    default = 'OFF'
  )
  previewer_use = bpy.props.EnumProperty(
    name = 'Use Previewer',
    description = 'Choose whether PreviewShitter attempts to combine render passes into a render preview.',
    items = [
      #identifier   #name       #desc  #icon             #ID
      ('OFF'      , 'OFF'      ,'' , 'PANEL_CLOSE'     , 0),
      ('ON'       , 'ON'       ,'' , 'VISIBLE_IPO_ON'  , 1)
    ],
    default = 'OFF'
  )


  remove_existing_nodes = bpy.props.EnumProperty(
    name = 'Remove Existing Nodes',
    description = 'Choose whether the function should remove existing nodes, or only add new.',
    items = [
      #identifier   #name         #desc  #icon        #ID
      ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
      ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Regenerate'
  )
  regenerate_shadow_shitter = bpy.props.EnumProperty(
    name = 'Regenerate Shadow Shitter',
    description = 'Delete the nodes in current SHADOW Shitter and create new ones.',
    items = [
      #identifier   #name         #desc  #icon        #ID
      ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
      ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Keep'
  )
  regenerate_preview_shitter = bpy.props.EnumProperty(
    name = 'Regenerate Preview Shitter',
    description = 'Delete the nodes in current PREVIEW Shitter and create new ones.',
    items = [
      #identifier   #name         #desc  #icon        #ID
      ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
      ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Keep'
  )
  regenerate_resize_shitter = bpy.props.EnumProperty(
    name = 'Regenerate Resize Shitter',
    description = 'Delete the nodes in current RESIZE Shitter and create new ones.',
    items = [
      #identifier   #name         #desc  #icon        #ID
      ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
      ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Keep'
  )
  regenerate_height_material = bpy.props.EnumProperty(
    name = 'Regenerate HEIGHT material',
    description = 'Delete the nodes in current HEIGHT material and create new ones.',
    items = [
      #identifier   #name         #desc  #icon        #ID
      ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
      ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Keep'
  )
  regenerate_normal_material = bpy.props.EnumProperty(
    name = 'Regenerate Z-NORMAL',
    description = 'Delete the nodes in current Z-NORMAL material and create new ones.',
    items = [
      #identifier   #name         #desc  #icon        #ID
      ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
      ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Keep'
  )

  AO_identifier_use = bpy.props.EnumProperty(
    name = 'Use AO',
    description = 'Save AO pass from specified RenderLayers to individual folder.',
    items = [
      #identifier   #name       #desc  #icon             #ID
      ('OFF'      , 'OFF'       ,'' , 'PANEL_CLOSE'     , 0),
      ('Back'     , 'Back'      ,'' , 'FORWARD'         , 1),
      ('Front'    , 'Front'     ,'' , 'BACK'            , 2)
    ],
   default = 'Back'
  )
  AO_identifier = bpy.props.StringProperty(
    name = 'AO Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering AO.',
    default = 'main'
  )
  shadow_identifier_use = bpy.props.EnumProperty(
    name = 'Use Shadow',
    description = 'Save Shadow pass from specified RenderLayers to individual folder.',
    items = [
      #identifier   #name       #desc  #icon             #ID
      ('OFF'      , 'OFF'       ,'' , 'PANEL_CLOSE'     , 0),
      ('Back'     , 'Back'      ,'' , 'FORWARD'         , 1),
      ('Front'    , 'Front'     ,'' , 'BACK'            , 2)
    ],
   default = 'Back'
  )
  shadow_identifier = bpy.props.StringProperty(
    name = 'Shadow Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Shadow.',
    default = 'shadow'
  )
  height_identifier_use = bpy.props.EnumProperty(
    name = 'Use Height',
    description = 'Save Height pass from specified RenderLayers to individual folder.',
    items = [
      #identifier   #name       #desc  #icon             #ID
      ('OFF'      , 'OFF'       ,'' , 'PANEL_CLOSE'     , 0),
      ('Back'     , 'Back'      ,'' , 'FORWARD'         , 1),
      ('Front'    , 'Front'     ,'' , 'BACK'            , 2)
    ],
   default = 'Back'
  )
  height_identifier = bpy.props.StringProperty(
    name = 'Height Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Height.',
    default = 'height'
  )
  normal_identifier_use = bpy.props.EnumProperty(
    name = 'Use Z-Normal',
    description = 'Save Z-Normal pass from specified RenderLayers to individual folder.',
    items = [
      #identifier   #name       #desc  #icon             #ID
      ('OFF'      , 'OFF'       ,'' , 'PANEL_CLOSE'     , 0),
      ('Back'     , 'Back'      ,'' , 'FORWARD'         , 1),
      ('Front'    , 'Front'     ,'' , 'BACK'            , 2)
    ],
   default = 'Back'
  )
  normal_identifier = bpy.props.StringProperty(
    name = 'Z-Normal Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Z-Normal.',
    default = 'Z-normal'
  )
  def execute(self, context):
    
    #log_filename = 'C:/Users/GFX-V/Desktop/log.txt'
    # erase log file first
    #with open(log_filename, 'w'): pass
    
    def log(text):
      # write into log file
      ''' Logging only for debug usage.
      if bpy.path.abspath('//') != '':
        full_filename = bpy.path.basename(bpy.context.blend_data.filepath)
        folder_name = '//' + os.path.dirname(full_filename)
        log_path = os.path.join(folder_name, log_filename)
        with open(log_filename, 'a') as file:
          file.write(text)
          file.write('\n')
      else:
        self.report({'ERROR'}, 'Save the .blend file first before outputting to a log.')
      '''
      print(text)

    def insert_resizer(output_node, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, resizer_use):
      link_list = []
      for link in output_node.inputs[0].links:
        link_list.append(LinkList(link.from_node, link.to_node, link.from_socket, link.to_socket))
      for link in link_list:
        if link.from_node.name[-14:] == 'PreviewShitter' and resizer_use != 'OFF' or resizer_use == 'ALL OUTPUTS':
          average_node_location = ( link.from_node.location + link.to_node.location ) /2
          resizer_node = bpy.context.scene.node_tree.nodes.new('CompositorNodeGroup')
          resizer_node.node_tree = bpy.data.node_groups['ResizeShitter']
          resizer_node.name = output_node.name + '-ResizeShitter'
          resizer_node.label = resizer_node.name
          if render_layer_is_shadow == False and render_layer_is_height == False and render_layer_is_normal == False:
            resizer_node.location = average_node_location
          else:
            resizer_node.location = (link.from_node.location[0], average_node_location[1])
          resizer_node.width = node_width

          bpy.context.scene.node_tree.links.new(link.from_socket, resizer_node.inputs[0])
          bpy.context.scene.node_tree.links.new(resizer_node.outputs[0], link.to_socket)

          # resizer outputs
          full_resolution =    str(int(bpy.context.scene.render.resolution_x * bpy.context.scene.render.resolution_percentage)/1/100)[:-2]
          half_resolution =    str(int(bpy.context.scene.render.resolution_x * bpy.context.scene.render.resolution_percentage)/2/100)[:-2]
          quarter_resolution = str(int(bpy.context.scene.render.resolution_x * bpy.context.scene.render.resolution_percentage)/4/100)[:-2]
          to_half_res    = full_resolution + 'to' + half_resolution
          to_quarter_res = full_resolution + 'to' + quarter_resolution

          # find the output path for the node
          output_base_path = output_node.base_path
          output_base_path_first_half = output_base_path.split('\\')[0]
          output_base_path_second_half = ''
          i = 0
          for segment_count in output_base_path.split('\\'):
            i+=1
          if i > 1:
            output_base_path_second_half = '\\' + output_base_path.split('\\')[1]

          #--------------------------------------------------------------------------------------------------------

          # handle AO
          output_render_layer_name = render_layer_name
          log('input socket name is...' + link.from_socket.name)
          if link.from_socket.name == 'AO':
            log('INPUT SOCKET IS AOOOOOOO')
            output_render_layer_name = output_render_layer_name + '-AO'

          # handle PreviewShitter outputs for FOLDER (base_path)
          if link.from_node.name[-14:] == 'PreviewShitter':
            resizer_output_base_path_half    = '//OUTPUT_PREVIEW'
            resizer_output_base_path_quarter = '//OUTPUT_PREVIEW'
          else:
            resizer_output_base_path_half    = output_base_path_first_half + '_' + to_half_res    + output_base_path_second_half + '/' + bpy.context.scene.name + '_' +  output_render_layer_name
            resizer_output_base_path_quarter = output_base_path_first_half + '_' + to_quarter_res + output_base_path_second_half + '/' + bpy.context.scene.name + '_' +  output_render_layer_name

          # handle PreviewShitter outputs for FILENAME (file_slot)
          if link.from_node.name[-14:] == 'PreviewShitter':
            output_filename_half    = preview_group_name + 'PREVIEW' + '_' + to_half_res    + '_'
            output_filename_quarter = preview_group_name + 'PREVIEW' + '_' + to_quarter_res + '_'
          else:
            output_filename_half    = bpy.context.scene.name + '_' + output_render_layer_name + '_' + to_half_res    + '_'
            output_filename_quarter = bpy.context.scene.name + '_' + output_render_layer_name + '_' + to_quarter_res + '_'
          

          #--------------------------------------------------------------------------------------------------------

          # add 50% node
          #if resizer_use == '50%' or resizer_use == '50% & 25%':
          # create basic half_output node
          half_output_node = bpy.context.scene.node_tree.nodes.new('CompositorNodeOutputFile')
          half_output_node.name = output_node.name + '-50%-output'
          half_output_node.label = half_output_node.name
          half_output_node.file_slots.remove(half_output_node.inputs[0])
          half_output_node.location = (output_node.location[0], output_node.location[1]-100)
          half_output_node.width = x_multiplier-30+150
          half_output_node.base_path = resizer_output_base_path_half
          half_output_node.file_slots.new( output_filename_half )
          # link it
          bpy.context.scene.node_tree.links.new(resizer_node.outputs[1], half_output_node.inputs[0])
          
          # add 25% node
          #if resizer_use == '50% & 25%':
          quarter_output_node = bpy.context.scene.node_tree.nodes.new('CompositorNodeOutputFile')
          quarter_output_node.name = output_node.name + '-25%-output'
          quarter_output_node.label = quarter_output_node.name
          quarter_output_node.file_slots.remove(quarter_output_node.inputs[0])
          quarter_output_node.location = (half_output_node.location[0], half_output_node.location[1]-100)
          quarter_output_node.width = x_multiplier-30+150
          quarter_output_node.base_path = resizer_output_base_path_quarter
          quarter_output_node.file_slots.new( output_filename_quarter )
          # link it
          bpy.context.scene.node_tree.links.new(resizer_node.outputs[2], quarter_output_node.inputs[0])

          #if link.from_node.name[-14:] == 'PreviewShitter':
          #  quarter_output_node.base_path = output_node.base_path + '_' + full_resolution + 'to' + quarter_resolution
          #  quarter_output_node.file_slots.new(preview_group_name + 'PREVIEW' + '_' + full_resolution + 'to' + quarter_resolution + '_')
          #else:
          #  if render_layer_is_AO == False:
          #    quarter_output_node.base_path = output_base_path_first_half + '_' + full_resolution + 'to' + quarter_resolution + output_base_path_second_half + '\\' + bpy.context.scene.name + '_' + render_layer_name
          #    quarter_output_node.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '_' + full_resolution + 'to' + quarter_resolution + '_')
          #  if render_layer_is_AO == True:
          #    quarter_output_node.base_path = output_base_path_first_half + '_' + full_resolution + 'to' + quarter_resolution + output_base_path_second_half + '\\' + bpy.context.scene.name + '_' + render_layer_name + '-AO'
          #    quarter_output_node.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '-AO' + '_' + full_resolution + 'to' + quarter_resolution + '_')

          # link the resizer to the output nodes

    log('----------------------------------------------')
    log('   G E N E R A T E   R E N D E R    N O D E S ')
    log('----------------------------------------------')

    # ------------------------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------------------------

    render_layers_from_scene = bpy.context.scene.name   
    render_nodes_to_scene = bpy.context.scene.name

    output_folder      = '//OUTPUT\\'
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
    
    for render_layer in bpy.context.scene.render.layers:
      render_layer_list.append(render_layer.name)

    log('Detected RenderLayers:')
    for render_layer_name in render_layer_list:
      log('  ' + render_layer_name)








    if bpy.data.materials.get('HEIGHT') is None:
      height_material_existed = False
    else:
      height_material_existed = True
    # check if HEIGHT material exists, if not, create it
    if bpy.data.materials.get('HEIGHT') is None:
      # create new HEIGHT material
      log('HEIGHT material does not exist, creating...')
      height_mtl = bpy.data.materials.new('HEIGHT')
      height_mtl.use_nodes = True
      height_nodes = height_mtl.node_tree.nodes
    if self.regenerate_height_material == 'Regenerate' or height_material_existed == False:
      height_mtl = bpy.data.materials['HEIGHT']
      height_mtl.use_nodes = True
      height_nodes = height_mtl.node_tree.nodes
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
    if self.regenerate_normal_material == 'Regenerate' or normal_material_existed == False:
      normal_mtl = bpy.data.materials['Z-NORMAL']
      normal_mtl.use_nodes = True
      normal_nodes = normal_mtl.node_tree.nodes
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
      
      if self.AO_identifier_use == 'Back':
        render_layer_appendix_AO = render_layer_name[-appendix_AO_char_count:]
      if self.AO_identifier_use == 'Front':
        render_layer_appendix_AO = render_layer_name[:appendix_AO_char_count]

      if self.shadow_identifier_use == 'Back':
        render_layer_appendix_shadow = render_layer_name[-appendix_shadow_char_count:]
      if self.shadow_identifier_use == 'Front':
        render_layer_appendix_shadow = render_layer_name[:appendix_shadow_char_count]

      if self.height_identifier_use == 'Back':
        render_layer_appendix_height = render_layer_name[-appendix_height_char_count:]
      if self.height_identifier_use == 'Front':
        render_layer_appendix_height = render_layer_name[:appendix_height_char_count]
      
      if self.normal_identifier_use == 'Back':
        render_layer_appendix_normal = render_layer_name[-appendix_normal_char_count:]
      if self.normal_identifier_use == 'Front':
        render_layer_appendix_normal = render_layer_name[:appendix_normal_char_count]


      if render_layer_appendix_AO == appendix_AO:
        if render_layer.use_pass_ambient_occlusion == False:
          render_layer.use_pass_ambient_occlusion = True
      
      if render_layer_appendix_shadow == appendix_shadow:
        if render_layer.use_pass_shadow == False:
          render_layer.use_pass_shadow = True
      
      if render_layer_appendix_height == appendix_height:
        if render_layer.material_override != bpy.data.materials['HEIGHT']:
          render_layer.material_override = bpy.data.materials['HEIGHT']
      
      if render_layer_appendix_normal == appendix_normal:
        if render_layer.material_override != bpy.data.materials['Z-NORMAL']:
          render_layer.material_override = bpy.data.materials['Z-NORMAL']


    # destroy shadow shitter if desired by settings
    if self.regenerate_shadow_shitter == 'Regenerate':
      if bpy.data.node_groups.get('ShadowShitter') is not None:
        bpy.data.node_groups.remove(bpy.data.node_groups['ShadowShitter'])
    # check if ShadowShitter exists, if not, create it
    nodes = bpy.context.scene.node_tree.nodes
    if bpy.data.node_groups.get('ShadowShitter') is None:
      log('ShadowShitter does not exist, creating...')
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



    # destroy PREVIEW shitter if desired by settings
    if self.regenerate_preview_shitter == 'Regenerate':
      if bpy.data.node_groups.get('PreviewShitter') is not None:
        bpy.data.node_groups.remove(bpy.data.node_groups['PreviewShitter'])
    # check if preview shitter exists, if not, create it
    nodes = bpy.context.scene.node_tree.nodes

    x_count = 0
    y_count = 0
    x_multiplier = 320
    y_multiplier = -200
    node_width = 270

    if bpy.data.node_groups.get('PreviewShitter') is None:
      log('PreviewShitter does not exist, creating...')
      preview_shitter = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = 'PreviewShitter')

      preview_shitter.inputs.new('NodeSocketFloat', 'main')
      preview_shitter.inputs.new('NodeSocketFloat', 'main-AO')
      preview_shitter.inputs.new('NodeSocketFloat', 'height')
      preview_shitter.inputs.new('NodeSocketFloat', 'Z-normal')
      preview_shitter.inputs.new('NodeSocketFloat', 'shadow')
      preview_shitter.inputs['main'].default_value     = 0.5
      preview_shitter.inputs['main-AO'].default_value  = 1
      preview_shitter.inputs['height'].default_value   = 0
      preview_shitter.inputs['Z-normal'].default_value = 0
      preview_shitter.inputs['shadow'].default_value   = 1
      
      input_node = preview_shitter.nodes.new(type = 'NodeGroupInput')
      input_node.name = 'PreviewShitter-Input'
      input_node.label = input_node.name
      input_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      x_count+=1

      AO_invert_node = preview_shitter.nodes.new(type = 'CompositorNodeInvert')
      AO_invert_node.name = 'PreviewShitter-AO-Invert'
      AO_invert_node.label = AO_invert_node.name
      AO_invert_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      AO_invert_node.width            = node_width
      AO_invert_node.use_custom_color = True
      AO_invert_node.color            = (1, 0.873463, 0.603827)
      x_count+=1
      
      AO_set_alpha_node = preview_shitter.nodes.new(type = 'CompositorNodeSetAlpha')
      AO_set_alpha_node.name = 'PreviewShitter-AO-SetAlpha'
      AO_set_alpha_node.label = AO_set_alpha_node.name
      AO_set_alpha_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      AO_set_alpha_node.width            = node_width
      AO_set_alpha_node.use_custom_color = True
      AO_set_alpha_node.color            = (1, 0.873463, 0.603827)
      x_count+=1
      
      AO_multiply_node = preview_shitter.nodes.new(type = 'CompositorNodeMixRGB')
      AO_multiply_node.name = 'PreviewShitter-AO-Multiply'
      AO_multiply_node.label = AO_multiply_node.name
      AO_multiply_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      AO_multiply_node.width = node_width
      AO_multiply_node.use_custom_color = True
      AO_multiply_node.color = (1, 0.873463, 0.603827)
      AO_multiply_node.blend_type = 'MULTIPLY'
      AO_multiply_node.use_alpha = True
      y_count+=1
      
      height_set_alpha_node = preview_shitter.nodes.new(type = 'CompositorNodeSetAlpha')
      height_set_alpha_node.name = 'PreviewShitter-Height-SetAlpha'
      height_set_alpha_node.label = height_set_alpha_node.name
      height_set_alpha_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      height_set_alpha_node.width = node_width
      height_set_alpha_node.use_custom_color = True
      height_set_alpha_node.color = (0.890884, 1, 0.787412)
      x_count+=1
      
      height_add_node = preview_shitter.nodes.new(type = 'CompositorNodeMixRGB')
      height_add_node.name = 'PreviewShitter-Height-Add'
      height_add_node.label = height_add_node.name
      height_add_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      height_add_node.width = node_width
      height_add_node.use_custom_color = True
      height_add_node.color = (0.890884, 1, 0.787412)
      height_add_node.blend_type = 'ADD'
      height_add_node.use_alpha = True
      y_count+=1
      
      normal_set_alpha_node = preview_shitter.nodes.new(type = 'CompositorNodeSetAlpha')
      normal_set_alpha_node.name = 'PreviewShitter-Normal-SetAlpha'
      normal_set_alpha_node.label = normal_set_alpha_node.name
      normal_set_alpha_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      normal_set_alpha_node.width = node_width
      normal_set_alpha_node.use_custom_color = True
      normal_set_alpha_node.color = (0.787412, 0.971302, 1)
      x_count+=1
      
      normal_add_node = preview_shitter.nodes.new(type = 'CompositorNodeMixRGB')
      normal_add_node.name = 'PreviewShitter-Normal-Add'
      normal_add_node.label = normal_add_node.name
      normal_add_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      normal_add_node.width = node_width
      normal_add_node.use_custom_color = True
      normal_add_node.color = (0.787412, 0.971302, 1)
      normal_add_node.blend_type = 'ADD'
      normal_add_node.use_alpha = True
      y_count+=1

      shadow_invert_node = preview_shitter.nodes.new(type = 'CompositorNodeInvert')
      shadow_invert_node.name = 'PreviewShitter-Shadow-Invert'
      shadow_invert_node.label = shadow_invert_node.name
      shadow_invert_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      shadow_invert_node.width = node_width
      shadow_invert_node.use_custom_color = True
      shadow_invert_node.color = (0.550994, 0.615665, 0.698193)
      x_count+=1
      
      shadow_opacity_multiply_node = preview_shitter.nodes.new(type = 'CompositorNodeMath')
      shadow_opacity_multiply_node.name = 'PreviewShitter-Shadow-Opacity-Multiply'
      shadow_opacity_multiply_node.label = shadow_opacity_multiply_node.name
      shadow_opacity_multiply_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      shadow_opacity_multiply_node.width = node_width
      shadow_opacity_multiply_node.use_custom_color = True
      shadow_opacity_multiply_node.color = (0.550994, 0.615665, 0.698193)
      shadow_opacity_multiply_node.operation = 'MULTIPLY'
      x_count+=1
      
      shadow_set_alpha_node = preview_shitter.nodes.new(type = 'CompositorNodeSetAlpha')
      shadow_set_alpha_node.name = 'PreviewShitter-Shadow-SetAlpha'
      shadow_set_alpha_node.label = shadow_set_alpha_node.name
      shadow_set_alpha_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      shadow_set_alpha_node.width = node_width
      shadow_set_alpha_node.use_custom_color = True
      shadow_set_alpha_node.color = (0.550994, 0.615665, 0.698193)
      x_count+=1
      
      shadow_alpha_over_node = preview_shitter.nodes.new(type = 'CompositorNodeAlphaOver')
      shadow_alpha_over_node.name = 'PreviewShitter-Shadow-AlphaOver'
      shadow_alpha_over_node.label = shadow_alpha_over_node.name
      shadow_alpha_over_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      shadow_alpha_over_node.width = node_width
      shadow_alpha_over_node.use_custom_color = True
      shadow_alpha_over_node.color = (0.550994, 0.615665, 0.698193)
      y_count+=1

      x_count=1
      settings_separateRGBA_node = preview_shitter.nodes.new(type = 'CompositorNodeSepRGBA')
      settings_separateRGBA_node.name = 'PreviewShitter-Settings-SeparateRGBA'
      settings_separateRGBA_node.label = settings_separateRGBA_node.name
      settings_separateRGBA_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_separateRGBA_node.width = node_width
      x_count+=1

      settings_AO_multiply_node = preview_shitter.nodes.new(type = 'CompositorNodeMath')
      settings_AO_multiply_node.name = 'PreviewShitter-Settings-AO-Multiply'
      settings_AO_multiply_node.label = settings_AO_multiply_node.name
      settings_AO_multiply_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_AO_multiply_node.width = node_width
      settings_AO_multiply_node.operation = 'MULTIPLY'
      x_count+=1

      settings_height_multiply_node = preview_shitter.nodes.new(type = 'CompositorNodeMath')
      settings_height_multiply_node.name = 'PreviewShitter-Settings-Height-Multiply'
      settings_height_multiply_node.label = settings_height_multiply_node.name
      settings_height_multiply_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_height_multiply_node.width = node_width
      settings_height_multiply_node.operation = 'MULTIPLY'
      x_count+=1

      settings_normal_multiply_node = preview_shitter.nodes.new(type = 'CompositorNodeMath')
      settings_normal_multiply_node.name = 'PreviewShitter-Settings-Normal-Multiply'
      settings_normal_multiply_node.label = settings_normal_multiply_node.name
      settings_normal_multiply_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_normal_multiply_node.width = node_width
      settings_normal_multiply_node.operation = 'MULTIPLY'
      y_count+=1

      x_count=1.1
      settings_AO_value_node = preview_shitter.nodes.new(type = 'CompositorNodeValue')
      settings_AO_value_node.name = 'PreviewShitter-Settings-AO-Value'
      settings_AO_value_node.label = settings_AO_value_node.name
      settings_AO_value_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_AO_value_node.width = node_width
      settings_AO_value_node.use_custom_color = True
      settings_AO_value_node.color = (1, 0.552123, 0.2033105)
      settings_AO_value_node.outputs[0].default_value = 1
      x_count+=1
      settings_height_value_node = preview_shitter.nodes.new(type = 'CompositorNodeValue')
      settings_height_value_node.name = 'PreviewShitter-Settings-Height-Value'
      settings_height_value_node.label = settings_height_value_node.name
      settings_height_value_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_height_value_node.width = node_width
      settings_height_value_node.use_custom_color = True
      settings_height_value_node.color = (0.606634, 1, 0.318547)
      settings_height_value_node.outputs[0].default_value = 0.3
      x_count+=1
      settings_normal_value_node = preview_shitter.nodes.new(type = 'CompositorNodeValue')
      settings_normal_value_node.name = 'PreviewShitter-Settings-Normal-Value'
      settings_normal_value_node.label = settings_normal_value_node.name
      settings_normal_value_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_normal_value_node.width = node_width
      settings_normal_value_node.use_custom_color = True
      settings_normal_value_node.color = (0.318547, 0.888118, 1)
      settings_normal_value_node.outputs[0].default_value = 0.2
      x_count+=1
      settings_shadow_value_node = preview_shitter.nodes.new(type = 'CompositorNodeValue')
      settings_shadow_value_node.name = 'PreviewShitter-Settings-Shadow-Value'
      settings_shadow_value_node.label = settings_shadow_value_node.name
      settings_shadow_value_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      settings_shadow_value_node.width = node_width
      settings_shadow_value_node.use_custom_color = True
      settings_shadow_value_node.color = (0.315438, 0.468448, 0.698193)
      settings_shadow_value_node.outputs[0].default_value = 0.5
      
      x_count=9
      output_node = preview_shitter.nodes.new(type = 'NodeGroupOutput')
      output_node.name = 'PreviewShitter-Output'
      output_node.label = output_node.name
      output_node.location = (x_count*x_multiplier, y_count*y_multiplier)

      preview_shitter.outputs.new('NodeSocketFloat', 'Preview')

      # LINKS
      # for AO_invert_node
      preview_shitter.links.new(input_node.outputs['main-AO'], AO_invert_node.inputs[1])
      # for AO_set_alpha_node
      preview_shitter.links.new(input_node.outputs['main'], AO_set_alpha_node.inputs[0])
      preview_shitter.links.new(AO_invert_node.outputs[0],  AO_set_alpha_node.inputs[1])
      # for AO_multiply_node
      preview_shitter.links.new(settings_AO_multiply_node.outputs[0], AO_multiply_node.inputs[0])
      preview_shitter.links.new(input_node.outputs['main'],           AO_multiply_node.inputs[1])
      preview_shitter.links.new(AO_set_alpha_node.outputs[0],         AO_multiply_node.inputs[2])
      # for height_set_alpha_node
      preview_shitter.links.new(input_node.outputs['main'],   height_set_alpha_node.inputs[0])
      preview_shitter.links.new(input_node.outputs['height'], height_set_alpha_node.inputs[1])
      # for height_add_node
      preview_shitter.links.new(settings_height_multiply_node.outputs[0], height_add_node.inputs[0])
      preview_shitter.links.new(AO_multiply_node.outputs[0],              height_add_node.inputs[1])
      preview_shitter.links.new(height_set_alpha_node.outputs[0],         height_add_node.inputs[2])
      # for normal_set_alpha_node
      preview_shitter.links.new(input_node.outputs['main'],     normal_set_alpha_node.inputs[0])
      preview_shitter.links.new(input_node.outputs['Z-normal'], normal_set_alpha_node.inputs[1])
      # for normal_add_node
      preview_shitter.links.new(settings_normal_multiply_node.outputs[0], normal_add_node.inputs[0])
      preview_shitter.links.new(height_add_node.outputs[0],               normal_add_node.inputs[1])
      preview_shitter.links.new(normal_set_alpha_node.outputs[0],         normal_add_node.inputs[2])
      # for shadow_invert_node
      preview_shitter.links.new(input_node.outputs['shadow'],       shadow_invert_node.inputs[1])
      # for shadow_opacity_multiply_node
      preview_shitter.links.new(settings_shadow_value_node.outputs[0], shadow_opacity_multiply_node.inputs[0])
      preview_shitter.links.new(shadow_invert_node.outputs[0],         shadow_opacity_multiply_node.inputs[1])
      # for shadow_set_alpha_node
      preview_shitter.links.new(shadow_opacity_multiply_node.outputs[0], shadow_set_alpha_node.inputs[1])
      # for shadow_alpha_over_node
      preview_shitter.links.new(shadow_set_alpha_node.outputs[0], shadow_alpha_over_node.inputs[1])
      preview_shitter.links.new(normal_add_node.outputs[0],       shadow_alpha_over_node.inputs[2])
      # for settings_separateRGBA_node
      preview_shitter.links.new(input_node.outputs['main'], settings_separateRGBA_node.inputs[0])
      # for settings_AO_multiply_node
      preview_shitter.links.new(settings_AO_value_node.outputs[0],     settings_AO_multiply_node.inputs[0])
      preview_shitter.links.new(settings_separateRGBA_node.outputs[3], settings_AO_multiply_node.inputs[1])
      # for settings_height_multiply_node
      preview_shitter.links.new(settings_height_value_node.outputs[0], settings_height_multiply_node.inputs[0])
      preview_shitter.links.new(settings_separateRGBA_node.outputs[3], settings_height_multiply_node.inputs[1])
      # for settings_normal_multiply_node
      preview_shitter.links.new(settings_normal_value_node.outputs[0], settings_normal_multiply_node.inputs[0])
      preview_shitter.links.new(settings_separateRGBA_node.outputs[3], settings_normal_multiply_node.inputs[1])
      # for output_node
      preview_shitter.links.new(shadow_alpha_over_node.outputs[0], output_node.inputs[0])



    # destroy RESIZE shitter if desired by settings
    if self.regenerate_resize_shitter == 'Regenerate':
      if bpy.data.node_groups.get('ResizeShitter') is not None:
        bpy.data.node_groups.remove(bpy.data.node_groups['ResizeShitter'])
    # check if preview shitter exists, if not, create it
    nodes = bpy.context.scene.node_tree.nodes
    if bpy.data.node_groups.get('ResizeShitter') is None:
      resize_shitter = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = 'ResizeShitter')

      resize_shitter.inputs.new('NodeSocketFloat', 'Image')
      input_node = resize_shitter.nodes.new('NodeGroupInput')
      input_node.name = 'ResizeShitter-Input'
      input_node.label = input_node.name
      input_node.location = (-200, 0)

      resize_shitter.outputs.new('NodeSocketFloat', 'Full size')
      resize_shitter.outputs.new('NodeSocketFloat', '50% size')
      resize_shitter.outputs.new('NodeSocketFloat', '25% size')
    
      output_node = resize_shitter.nodes.new('NodeGroupOutput')
      output_node.name = 'ResizeShitter-Output'
      output_node.label = output_node.name
      output_node.location = (400,0)
      
      transform_node_1 = resize_shitter.nodes.new('CompositorNodeTransform')
      transform_node_1.filter_type = 'BILINEAR'
      transform_node_1.inputs[4].default_value = 0.5
      transform_node_1.name = 'ResizeShitter-Transform-1'
      transform_node_1.label = transform_node_1.name
      transform_node_1.location = (0, -50)
      
      crop_node_1 = resize_shitter.nodes.new('CompositorNodeCrop')
      crop_node_1.relative = True
      crop_node_1.name = 'ResizeShitter-Crop-1'
      crop_node_1.rel_min_x = 0.25
      crop_node_1.rel_max_x = 0.74
      crop_node_1.rel_min_y = 0.25
      crop_node_1.rel_max_y = 0.74
      crop_node_1.label = crop_node_1.name
      crop_node_1.location = (200, -50)
      
      transform_node_2 = resize_shitter.nodes.new('CompositorNodeTransform')
      transform_node_2.filter_type = 'BILINEAR'
      transform_node_2.inputs[4].default_value = 0.25
      transform_node_2.name = 'ResizeShitter-Transform-2'
      transform_node_2.label = transform_node_1.name
      transform_node_2.location = (0, -300)

      crop_node_2 = resize_shitter.nodes.new('CompositorNodeCrop')
      crop_node_2.relative = True
      crop_node_2.name = 'ResizeShitter-Crop-2'
      crop_node_2.rel_min_x = 0.375
      crop_node_2.rel_max_x = 0.62
      crop_node_2.rel_min_y = 0.375
      crop_node_2.rel_max_y = 0.62
      crop_node_2.label = crop_node_2.name
      crop_node_2.location = (200, -300)

      #link the nodes
      resize_shitter.links.new(input_node.outputs[0], output_node.inputs[0])
      resize_shitter.links.new(input_node.outputs[0], transform_node_1.inputs[0])
      resize_shitter.links.new(input_node.outputs[0], transform_node_2.inputs[0])
      resize_shitter.links.new(transform_node_1.outputs[0], crop_node_1.inputs[0])
      resize_shitter.links.new(transform_node_2.outputs[0], crop_node_2.inputs[0])
      resize_shitter.links.new(crop_node_1.outputs[0], output_node.inputs[1])
      resize_shitter.links.new(crop_node_2.outputs[0], output_node.inputs[2])
      

    # switch scene to destination and make sure nodes are allowed
    bpy.context.screen.scene = bpy.data.scenes[render_nodes_to_scene]
    bpy.context.scene.use_nodes = True

    # clear all current composite nodes
    if self.remove_existing_nodes == 'Regenerate':
      for node in bpy.context.scene.node_tree.nodes:
        bpy.context.scene.node_tree.nodes.remove(node)



    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------  FFFFFFF      U       U         CCCCC       K      K     --------------
    # -----------------------  F            U       U        C     C      K    K       --------------
    # -----------------------  F            U       U       C             K  K         --------------
    # -----------------------  FFFFF        U       U       C             K K K        --------------
    # -----------------------  F             U     U         C     C      K     K      --------------
    # -----------------------  F              UUUU            CCCCC       K       K    --------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------


    nodes = bpy.context.scene.node_tree.nodes
    x_multiplier = 300
    y_multiplier = -680
    y_count = 0
    for render_layer_name in render_layer_list:
      x_count = 0

      render_layer_is_AO = False
      render_layer_is_shadow = False
      render_layer_is_normal = False
      render_layer_is_height = False
      render_layer_is_main = False

      # filter AO identifier
      appendix_AO_char_count = len(appendix_AO)
      if self.AO_identifier_use == 'Back':
        node_appendix_AO = render_layer_name[-appendix_AO_char_count:]
      if self.AO_identifier_use == 'Front':
        node_appendix_AO = render_layer_name[:appendix_AO_char_count]

      if node_appendix_AO == appendix_AO:
        render_layer_is_AO = True

      # filter shadow identifier
      appendix_shadow_char_count = len(appendix_shadow)
      if self.shadow_identifier_use == 'Back':
        node_appendix_shadow = render_layer_name[-appendix_shadow_char_count:]
      if self.shadow_identifier_use == 'Front':
        node_appendix_shadow = render_layer_name[:appendix_shadow_char_count]

      if node_appendix_shadow == appendix_shadow:
        render_layer_is_shadow = True

      # filter normal identifier
      appendix_normal_char_count = len(appendix_normal)
      if self.normal_identifier_use == 'Back':
        node_appendix_normal = render_layer_name[-appendix_normal_char_count:]
      if self.normal_identifier_use == 'Front':
        node_appendix_normal = render_layer_name[:appendix_normal_char_count]

      if node_appendix_normal == appendix_normal:
        render_layer_is_normal = True

      # filter height identifier
      appendix_height_char_count = len(appendix_height)
      if self.height_identifier_use == 'Back':
        node_appendix_height = render_layer_name[-appendix_height_char_count:]
      if self.height_identifier_use == 'Front':
        node_appendix_height = render_layer_name[:appendix_height_char_count]

      if node_appendix_height == appendix_height:
        render_layer_is_height = True


      # create input node
      input_node = nodes.new('CompositorNodeRLayers')
      input_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      input_node.name = 'render-layer-' + render_layer_name
      input_node.label = 'render-layer-' + render_layer_name
      input_node.scene = bpy.data.scenes[render_layers_from_scene]
      input_node.layer = render_layer_name
      input_node.width = x_multiplier-30
      
      # add x for next node
      x_count += 4




      # read if render layer is shadow/AO/height/normal/...
      log('Processing: ' + render_layer_name)
      # remove the shadow/AO/height/normal/... identifier and  get a base_name (add scene name)
      preview_group_name = bpy.context.scene.name + '_' + render_layer_name
      if render_layer_is_shadow == True:
        if self.shadow_identifier_use == 'Back':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[:-appendix_shadow_char_count]
        elif self.shadow_identifier_use == 'Front':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[appendix_shadow_char_count:]
        log('...layer identified as shadow')

      elif render_layer_is_AO == True:
        if self.AO_identifier_use == 'Back':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[:-appendix_AO_char_count]
        elif self.AO_identifier_use == 'Front':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[appendix_AO_char_count:]
        log('...layer identified as AO')
      elif render_layer_is_height == True:
        if self.height_identifier_use == 'Back':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[:-appendix_height_char_count]
        elif self.height_identifier_use == 'Front':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[appendix_height_char_count:]
        log('...layer identified as height')
      elif render_layer_is_normal == True:
        if self.normal_identifier_use == 'Back':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[:-appendix_normal_char_count]
        elif self.normal_identifier_use == 'Front':
          preview_group_name = bpy.context.scene.name + '_' + render_layer_name[appendix_normal_char_count:]
        log('...layer identified as normal')

      # create a Preview shitter group for base_name if it does not yet exist
      preview_shitter_node_name = preview_group_name+'PreviewShitter'
      if nodes.get(preview_shitter_node_name) is not None:
        preview_shitter_node = nodes[preview_shitter_node_name]
      elif nodes.get(preview_shitter_node_name) is None and self.previewer_use == 'ON':
        log('Adding ' + preview_shitter_node_name)
        preview_shitter_node = nodes.new('CompositorNodeGroup')
        preview_shitter_node.node_tree = bpy.data.node_groups['PreviewShitter']
        preview_shitter_node.name = preview_shitter_node_name
        preview_shitter_node.label = preview_shitter_node.name
        preview_shitter_node.location = (x_count*x_multiplier, y_count*y_multiplier)
        preview_shitter_node.width = x_multiplier-30
        x_count += 2
        preview_shitter_output_node = nodes.new('CompositorNodeOutputFile')
        preview_shitter_output_node.location = (x_count*x_multiplier, y_count*y_multiplier)
        preview_shitter_output_node.name = 'file-output-' + render_layer_name + '-PREVIEW'
        preview_shitter_output_node.label = preview_shitter_output_node.name
        preview_shitter_output_node.width = x_multiplier-30+150

        preview_shitter_output_node.base_path = output_folder[:-1] + '_PREVIEW'
        # remove output node default input socket
        preview_shitter_output_node.file_slots.remove(preview_shitter_output_node.inputs[0])
        # add output node input socket
        preview_shitter_output_node.file_slots.new(preview_group_name + 'PREVIEW' + '_')

        bpy.context.scene.node_tree.links.new(preview_shitter_node.outputs[0], preview_shitter_output_node.inputs[0])
        # add resizer
        if self.resizer_use != 'OFF':
          insert_resizer(preview_shitter_output_node, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, self.resizer_use)

        x_count +=-2
      else:
        if self.previewer_use == 'ON':
          if nodes.get(preview_group_name) is not None:
            preview_shitter_node = nodes[preview_group_name]



      # connect renderlayer output to preview shitter input

      # add x for next node
      x_count += -2

      # create output node
      output_node = nodes.new('CompositorNodeOutputFile')
      output_node.location = (x_count*x_multiplier, y_count*y_multiplier)
      output_node.name = 'file-output-' + render_layer_name
      output_node.label = 'file-output-' + render_layer_name
      output_node.width = x_multiplier-30+150

      output_node.base_path = output_folder + bpy.context.scene.name + '\\' + bpy.context.scene.name + '_' + render_layer_name

      # create extra output node for AO
      if render_layer_is_AO == True and self.AO_identifier_use != 'OFF':
        output_node_AO = nodes.new('CompositorNodeOutputFile')
        output_node_AO.location = (x_count*x_multiplier, y_count*y_multiplier - 140 - 180)
        output_node_AO.name = 'file-output-' + render_layer_name + '-AO'
        output_node_AO.label = 'file-output-' + render_layer_name + '-AO'
        output_node_AO.width = x_multiplier-30+150

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


      if self.previewer_use == 'ON':
        if render_layer_is_AO:
          bpy.context.scene.node_tree.links.new(input_node.outputs[0], preview_shitter_node.inputs['main'])
          index_AO = input_node.outputs.find('AO')
          bpy.context.scene.node_tree.links.new(input_node.outputs[index_AO], preview_shitter_node.inputs['main-AO'])
        elif render_layer_is_height:
          bpy.context.scene.node_tree.links.new(input_node.outputs[0], preview_shitter_node.inputs['height'])
        elif render_layer_is_normal:
          bpy.context.scene.node_tree.links.new(input_node.outputs[0], preview_shitter_node.inputs['Z-normal'])
        elif render_layer_is_shadow:
          index_shadow = input_node.outputs.find('Shadow')
          bpy.context.scene.node_tree.links.new(input_node.outputs[index_shadow], preview_shitter_node.inputs['shadow'])
        else:
          bpy.context.scene.node_tree.links.new(input_node.outputs[0], preview_shitter_node.inputs['main'])

      # exception to change to shadow pass
      if render_layer_is_shadow == True and self.shadow_identifier_use != 'OFF':
        shadow_shitter = nodes.new('CompositorNodeGroup')
        shadow_shitter.node_tree = bpy.data.node_groups['ShadowShitter']
        shadow_shitter.name = render_layer_name + '-ShadowShitter'
        shadow_shitter.label = shadow_shitter.name
        #bpy.context.scene.node_tree.links.new(input_node.outputs[3], output_node.inputs[0])
        x_count += 1
        y_count -= 0.50
        shadow_shitter.location = (x_count*x_multiplier-300, y_count*y_multiplier+16)
        shadow_shitter.width = x_multiplier-30
        x_count -= 1
        y_count += 0.50

        index_shadow = input_node.outputs.find('Shadow')
        
        bpy.context.scene.node_tree.links.new(input_node.outputs[index_shadow], shadow_shitter.inputs[0])
        bpy.context.scene.node_tree.links.new(shadow_shitter.outputs[0], output_node.inputs[0])
        # add resizer
        if self.resizer_use != 'OFF':
          insert_resizer(output_node, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, self.resizer_use)
        log('-> Finished processing ' + render_layer_name)
        log('---------------------------------------------')
        continue

      # exception to add AO pass
      if render_layer_is_AO == True and self.AO_identifier_use != 'OFF':
        bpy.context.scene.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])
        # add resizer
        if self.resizer_use != 'OFF':
          insert_resizer(output_node, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, self.resizer_use)

        # connect to output_node_AO
        #output_node.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '-AO' + '_')
        index_AO = input_node.outputs.find('AO')
        bpy.context.scene.node_tree.links.new(input_node.outputs[index_AO], output_node_AO.inputs[0])
        # add resizer
        if self.resizer_use != 'OFF':
          insert_resizer(output_node_AO, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, self.resizer_use)
        log('-> Finished processing ' + render_layer_name)
        log('---------------------------------------------')
        continue
      
      if render_layer_is_height and self.height_identifier_use != 'OFF':
        height_alpha_over_black_node = bpy.context.scene.node_tree.nodes.new('CompositorNodeAlphaOver')
        height_alpha_over_black_node.name = render_layer_name + '-Alpha-Over-Black'
        height_alpha_over_black_node.label = height_alpha_over_black_node.name
        height_alpha_over_black_node.location = ( input_node.location[0] + x_multiplier, input_node.location[1] -262 )
        height_alpha_over_black_node.width = x_multiplier - 30
        height_alpha_over_black_node.inputs[1].default_value = (0, 0, 0, 1)

        bpy.context.scene.node_tree.links.new(input_node.outputs[0], height_alpha_over_black_node.inputs[2])
        bpy.context.scene.node_tree.links.new(height_alpha_over_black_node.outputs[0], output_node.inputs[0])

        if self.resizer_use != 'OFF':
          insert_resizer(output_node, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, self.resizer_use)
        log('-> Finished processing ' + render_layer_name)
        log('---------------------------------------------')
        continue

      if render_layer_is_normal and self.normal_identifier_use != 'OFF':
        normal_alpha_over_black_node = bpy.context.scene.node_tree.nodes.new('CompositorNodeAlphaOver')
        normal_alpha_over_black_node.name = render_layer_name + '-Alpha-Over-Black'
        normal_alpha_over_black_node.label = normal_alpha_over_black_node.name
        normal_alpha_over_black_node.location = ( input_node.location[0] + x_multiplier, input_node.location[1] -262 )
        normal_alpha_over_black_node.width = x_multiplier - 30
        normal_alpha_over_black_node.inputs[1].default_value = (0, 0, 0, 1)

        bpy.context.scene.node_tree.links.new(input_node.outputs[0], normal_alpha_over_black_node.inputs[2])
        bpy.context.scene.node_tree.links.new(normal_alpha_over_black_node.outputs[0], output_node.inputs[0])

        if self.resizer_use != 'OFF':
          insert_resizer(output_node, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, self.resizer_use)
        log('-> Finished processing ' + render_layer_name)
        log('---------------------------------------------')
        continue

      # link the nodes
      bpy.context.screen.scene.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])
     
      # add resizer
      if self.resizer_use != 'OFF':
        insert_resizer(output_node, x_multiplier, output_folder, render_layer_name, preview_group_name, render_layer_is_shadow, self.resizer_use)

      log('-> Finished processing ' + render_layer_name)
      log('---------------------------------------------')
    
    return {'FINISHED'}






