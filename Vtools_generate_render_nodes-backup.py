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
      ('front', 'front',''),
      ('back', 'back','')
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
    description = 'Select where in the RenderLayer name is the AO identifier.',
    items = [
      ('front', 'front',''),
      ('back', 'back','')
    ]
  )
  shadow_identifier = bpy.props.StringProperty(
    name = 'Shadow Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Shadow.',
    default = 'shadow'
  )

  def execute(self, context):
    # ------------------------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------------------------

    remove_existing_compositor_nodes = True

    screen_name = 'Default'
    render_layers_from_scene = bpy.context.scene.name
    render_nodes_to_scene = bpy.context.scene.name

    appendix_AO =     self.AO_identifier #'main'
    appendix_shadow = self.shadow_identifier #'shadow' 

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    # make all scenes use compositor nodes
    bpy.data.screens[screen_name].scene = bpy.data.scenes[render_layers_from_scene]
    bpy.context.scene.use_nodes = True
    bpy.data.screens[screen_name].scene = bpy.data.scenes[render_nodes_to_scene]
    bpy.context.scene.use_nodes = True


    # read Render Layers
    # switch scene to source
    bpy.data.screens[screen_name].scene = bpy.data.scenes[render_layers_from_scene]
    # go through render layers and add them to a list
    render_layer_list = []
    print('Reading render layers:')
    for render_layer in bpy.context.scene.render.layers:
      print(render_layer.name)
      render_layer_list.append(render_layer.name)

    # make sure AO render layers have AO on, and shadow render layers have shadow on
    appendix_AO_char_count = len(appendix_AO)
    appendix_shadow_char_count = len(appendix_shadow)

    for render_layer in bpy.context.scene.render.layers:
      render_layer_name = render_layer.name
      render_layer_appendix_AO = render_layer_name[-appendix_AO_char_count:]
      render_layer_appendix_shadow = render_layer_name[-appendix_shadow_char_count:]
      
      if render_layer_appendix_AO == appendix_AO:
        print('AO appendix detected')
        if render_layer.use_pass_ambient_occlusion == False:
          print(str(render_layer_name) + ' has appendix "' + appendix_AO + '" but does not have AO pass activated. Activating AO pass...')
          render_layer.use_pass_ambient_occlusion = True
      
      if render_layer_appendix_shadow == appendix_shadow:
        print('shadow appendix detected')
        if render_layer.use_pass_shadow == False:
          print(str(render_layer_name) + ' has appendix "' + appendix_shadow + '" but does not have shadow pass activated. Activating shadow pass...')
          render_layer.use_pass_shadow = True



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
      output_node.location = (400,0)

      subtract_node = shadow_shitter.nodes.new(type="CompositorNodeMixRGB")
      subtract_node.name = 'ShadowShitter-subtract-node'
      subtract_node.label = 'ShadowShitter-subtract-node'
      subtract_node.location = (0,0)
      subtract_node.blend_type = 'SUBTRACT'

      set_alpha_node = shadow_shitter.nodes.new(type="CompositorNodeSetAlpha")
      set_alpha_node.name = 'ShadowShitter-set-alpha-node'
      set_alpha_node.label = 'ShadowShitter-set-alpha-node'
      set_alpha_node.location = (200,0)

      shadow_shitter.links.new(input_node.outputs[0], subtract_node.inputs[2])
      shadow_shitter.links.new(subtract_node.outputs[0], set_alpha_node.inputs[1])
      shadow_shitter.links.new(set_alpha_node.outputs[0], output_node.inputs[0])
      print('ShadowShitter successfully created!')



    # switch scene to destination and make sure nodes are allowed
    bpy.data.screens[screen_name].scene = bpy.data.scenes[render_nodes_to_scene]
    bpy.context.scene.use_nodes = True

    # clear all current composite nodes (mainly for debug)
    if remove_existing_compositor_nodes == True:
      for node in bpy.context.scene.node_tree.nodes:
        print('Removing ' + node.name)
        bpy.context.scene.node_tree.nodes.remove(node)

    nodes = bpy.context.scene.node_tree.nodes
    x_count = 0
    y_count = 0
    x_multiplier = 200
    y_multiplier = -400

    for render_layer_name in render_layer_list:
      
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

      output_node.base_path = "//OUTPUT\\" + bpy.context.scene.name + '\\' + bpy.context.scene.name + '_' + render_layer_name

      # put x pack to normal for next row, and add y for next row
      x_count -= 1
      y_count += 1

      # remove output node default input socket
      output_node.file_slots.remove(output_node.inputs[0])
      # add output node input socket
      output_node.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '_')

      # exception to change to shadow pass
      appendix_shadow_char_count = len(appendix_shadow)
      node_appendix_shadow = render_layer_name[-appendix_shadow_char_count:]
      if node_appendix_shadow == appendix_shadow:
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
      appendix_AO_char_count = len(appendix_AO)
      node_appendix_AO = render_layer_name[-appendix_AO_char_count:]
      if node_appendix_AO == appendix_AO:
        print(node_appendix_AO)
        bpy.context.scene.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])
        
        # add extra output node socket for AO
        output_node.file_slots.new(bpy.context.scene.name + '_' + render_layer_name + '-AO' + '_')

        index_AO = input_node.outputs.find('AO')

        bpy.context.scene.node_tree.links.new(input_node.outputs[index_AO], output_node.inputs[1])
        continue
      
      # link the nodes
      bpy.context.scene.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])

      print(render_layer_name)
    return {'FINISHED'}






