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

    # generate material
    bpy.ops.scene.wtf_generate_material_xyz(XYZ_wtfscale = self.XYZ_wtfscale, XYZ_groundheight = self.XYZ_groundheight, XYZ_groundheight_from_selected = self.XYZ_groundheight_from_selected)

    # set material override on all RenderLayers
    for scene in bpy.data.scenes:
      for renderlayer in scene.render.layers:
        renderlayer.material_override = bpy.data.materials['XYZmap']
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
      camera_obj = scene.camera
      # find top parent
      camera_boss_object = camera_obj
      while(camera_boss_object.parent is not None):
        camera_boss_object = camera_boss_object.parent
      
      if camera_obj.constraints.get('XYZ_TRACK_TO') is None:
        track_to_constraint = camera_obj.constraints.new('TRACK_TO')
        track_to_constraint.name       = 'XYZ_TRACK_TO'
        track_to_constraint.target     = camera_boss_object
        track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_to_constraint.up_axis    = 'UP_Y'




    return {'FINISHED'}
