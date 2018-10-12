import bpy

class WTF_scene_settings_XYZ(bpy.types.Operator):
  '''Convert all scenes to XYZ map rendering.'''
  bl_idname = 'scene.wtf_scene_settings_xyz'
  bl_label = 'XYZ Settings'
  bl_options = {'REGISTER', 'UNDO'}

  replace_materials = bpy.props.BoolProperty(
    name = 'Replace materials',
    description = 'Replace all materials on all objects with XYZmap.',
    default = False
  )

  XYZ_wtfscale = bpy.props.FloatProperty(
  name = 'Scale',
  default = 128
  )
  XYZ_groundheight = bpy.props.FloatProperty(
  name = 'Ground Height',
  default = 0
  )
  XYZ_groundheight_from_selected = bpy.props.BoolProperty(
  name = 'Active object sets Ground Height',
  default = False
  )

  def execute(self, context):

    # apply shared settings
    bpy.ops.scene.wtf_scene_settings_shared()

    # output & cache & placeholder settings
    for scene in bpy.data.scenes:
      scene.render.filepath = '//cache\\\\' + scene.name + '/' + scene.name + '-cache_'
      scene.render.use_overwrite = False
      scene.render.use_placeholder = True

    if bpy.data.node_groups.get('XYZ-settings') is None:
      settings_group = bpy.data.node_groups.new(name = 'XYZ-settings', type = 'ShaderNodeTree')
    else:
      settings_group = bpy.data.node_groups['XYZ-settings']
    
    if settings_group.nodes.get('XYZ-settings-scale') is None:
      settings_scale_node = settings_group.nodes.new('ShaderNodeValue')
      settings_scale_node.name =  'XYZ-settings-scale'
      settings_scale_node.label = 'XYZ-settings-scale'
      settings_scale_node.outputs[0].default_value = 128
    else:
      settings_scale_node = settings_group.nodes['XYZ-settings-scale']

    settings_scale = settings_scale_node.outputs[0].default_value

    # generate material
    bpy.ops.scene.wtf_generate_material_xyz(XYZ_wtfscale = settings_scale, XYZ_groundheight = self.XYZ_groundheight, XYZ_groundheight_from_selected = self.XYZ_groundheight_from_selected)

    # set material override on all RenderLayers
    for scene in bpy.data.scenes:
      for renderlayer in scene.render.layers:
        renderlayer.material_override = bpy.data.materials['XYZmap']
        renderlayer.cycles.use_denoising = False
        #'''
        #Disabled because every material is getting the node group.
        #''' not disabled atm
        #renderlayer.material_override = None
        

    # store original values of the object and mtl picker boxes
    store_mtl = bpy.context.scene.Mtl_for_mat_replace
    store_obj = bpy.context.scene.Obj_for_mat_replace
    # replace materials of all objects
    if self.replace_materials == True:
      bpy.context.scene.Mtl_for_mat_replace = 'XYZmap'
      for obj in bpy.data.objects:
        bpy.context.scene.Obj_for_mat_replace = obj.name
        bpy.ops.object.material_replace()
    # revert the obj and mtl picked boxes to their original state
    bpy.context.scene.Mtl_for_mat_replace = store_mtl
    bpy.context.scene.Obj_for_mat_replace = store_obj

    # add Track To constraint to camera
    for scene in bpy.data.scenes:
      # make sure the scene actually has a camera
      if scene.camera is not None:
        camera_obj = scene.camera
        # find top parent
        camera_boss_object = camera_obj
        print('A',camera_boss_object)
        while(camera_boss_object.parent is not None):
          print('X',camera_boss_object)
          print('Y',camera_boss_object.parent)
          camera_boss_object = camera_boss_object.parent
        
        
        
        if camera_obj.constraints.get('XYZ_TRACK_TO') is None:
          track_to_constraint = camera_obj.constraints.new('TRACK_TO')
        else:
          track_to_constraint = camera_obj.constraints['XYZ_TRACK_TO']
        track_to_constraint.name       = 'XYZ_TRACK_TO'
        track_to_constraint.target     = camera_boss_object
        track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_to_constraint.up_axis    = 'UP_Y'
    
    bpy.ops.scene.wtf_generate_material_nrm()
    # duplicate all remaining render layers and add -XYZ-Normalmap instead of -copy
    for scene in bpy.data.scenes:
      # create a list of render layers (otherwise it iterates over new ones too)
      renderlayer_list = []
      for renderlayer in scene.render.layers:
        renderlayer_list.append(renderlayer.name)
      for renderlayer_name in renderlayer_list:
        render_layer = scene.render.layers[renderlayer_name]
        bpy.ops.scene.duplicate_render_layer(set_appendix = '-Normalmap', set_source_render_layer = render_layer.name, set_source_scene = scene.name, set_target_scene = scene.name)
        print(scene.name, 'is XJXJFJIFY SCENE NAME')
        scene.render.layers[renderlayer_name+'-Normalmap'].material_override = bpy.data.materials['Normalmap']


    return {'FINISHED'}
