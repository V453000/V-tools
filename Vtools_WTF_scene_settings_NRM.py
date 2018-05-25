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

    # replace materials of all objects
    if self.replace_materials == True:
      bpy.context.scene.Mtl_for_mat_replace = 'Normalmap'
      for obj in bpy.data.objects:
        bpy.context.scene.Obj_for_mat_replace = obj.name
        bpy.ops.object.material_replace()

    return {'FINISHED'}