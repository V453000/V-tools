import bpy

class generate_render_nodes_with_resize(bpy.types.Operator):
  '''Generate Render Nodes from RenderLayers, with automatically downscaled outputs.'''
  bl_idname = 'nodes.generate_render_nodes_with_resize'
  bl_label = 'Generate render nodes with automatic output resizing (mainly for icons)'
  bl_options = {'REGISTER', 'UNDO'}
  
  
  resizer_use = bpy.props.EnumProperty(
    name = 'Resizer',
    description = 'Choose whether ResizeShitter automatically downscales the outputs.',
    items = [
      #identifier   #name       #desc  #icon             #ID
      ('OFF'      , 'OFF'       ,'' , 'PANEL_CLOSE'     , 0),
      ('50%'      , '50%'       ,'' , 'SCENE'           , 1),
      ('50% & 25%', '50% & 25%' ,'' , 'CAMERA_STEREO'   , 2)
    ],
   default = '50% & 25%'
  )
  previewer_use = bpy.props.EnumProperty(
    name = 'Use Previewer',
    description = 'Choose whether PreviewShitter attempts to combine render passes into a render preview.',
    items = [
      #identifier   #name       #desc  #icon             #ID
      ('OFF'      , 'OFF'      ,'' , 'VISIBLE_IPO_ON'  , 0),
      ('ON'       , 'ON'       ,'' , 'VISIBLE_IPO_OFF' , 1)
    ],
    default = 'ON'
  )

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
    description = 'Delete the nodes in current SHADOW Shitter and create new ones.',
    default = False
  )  
  regenerate_preview_shitter = bpy.props.BoolProperty(
    name = 'Regenerate Preview Shitter',
    description = 'Delete the nodes in current PREVIEW Shitter and create new ones.',
    default = False
  )
  regenerate_resize_shitter = bpy.props.BoolProperty(
    name = 'Regenerate Resize Shitter',
    description = 'Delete the nodes in current RESIZE Shitter and create new ones.',
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
    bpy.ops.nodes.generate_render_nodes(
      resizer_use = self.resizer_use,
      previewer_use = self.previewer_use,
      AO_identifier_use = self.AO_identifier_use,
      AO_identifier_position = self.AO_identifier_position,
      AO_identifier = self.AO_identifier,
      shadow_identifier_use = self.shadow_identifier_use,
      shadow_identifier_position = self.shadow_identifier_position,
      shadow_identifier = self.shadow_identifier,
      height_identifier_use = self.height_identifier_use,
      height_identifier_position = self.height_identifier_position,
      height_identifier = self.height_identifier,
      normal_identifier_use = self.height_identifier_use,
      normal_identifier_position = self.normal_identifier_position,
      normal_identifier = self.normal_identifier,
      remove_existing_nodes = self.remove_existing_nodes,
      regenerate_shadow_shitter = self.regenerate_shadow_shitter,
      regenerate_preview_shitter = self.regenerate_preview_shitter,
      regenerate_resize_shitter = self.regenerate_resize_shitter,
      regenerate_height_material = self.regenerate_height_material,
      regenerate_normal_material = self.regenerate_normal_material
      )

    return {'FINISHED'}
