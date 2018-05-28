import bpy

class WTF_scene_settings_NRM(bpy.types.Operator):
  '''Convert all scenes to NRM map rendering.'''
  bl_idname = 'scene.wtf_scene_settings_nrm'
  bl_label = 'NRM Settings'
  bl_options = {'REGISTER', 'UNDO'}

  replace_materials = bpy.props.BoolProperty(
    name = 'Replace materials',
    description = 'Replace all materials on all objects with XYZmap.',
    default = False
  )

  def execute(self, context):
    
    # apply shared settings
    bpy.ops.scene.wtf_scene_settings_shared()

    # generate material
    bpy.ops.scene.wtf_generate_material_nrm()

    # set material override on all RenderLayers
    for scene in bpy.data.scenes:
      for renderlayer in scene.render.layers:
        renderlayer.material_override = bpy.data.materials['Normalmap']
  
    # store original values of the object and mtl picker boxes
    store_mtl = bpy.context.scene.Mtl_for_mat_replace
    store_obj = bpy.context.scene.Obj_for_mat_replace
    # replace materials of all objects
    if self.replace_materials == True:
      bpy.context.scene.Mtl_for_mat_replace = 'Normalmap'
      for obj in bpy.data.objects:
        bpy.context.scene.Obj_for_mat_replace = obj.name
        bpy.ops.object.material_replace()
    # revert the obj and mtl picked boxes to their original state
    bpy.context.scene.Mtl_for_mat_replace = store_mtl
    bpy.context.scene.Obj_for_mat_replace = store_obj

    return {'FINISHED'}