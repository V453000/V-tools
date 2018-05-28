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
  default = 32
  )

  def execute(self, context):
    
    # apply shared settings
    bpy.ops.scene.wtf_scene_settings_shared()
    
    # generate material
    bpy.ops.scene.wtf_generate_material_xyz(XYZ_wtfscale = self.XYZ_wtfscale)

    # set material override on all RenderLayers
    for scene in bpy.data.scenes:
      for renderlayer in scene.render.layers:
        renderlayer.material_override = bpy.data.materials['XYZmap']

    # replace materials of all objects
    if self.replace_materials == True:
      bpy.context.scene.Mtl_for_mat_replace = 'XYZmap'
      for obj in bpy.data.objects:
        bpy.context.scene.Obj_for_mat_replace = obj.name
        bpy.ops.object.material_replace()

    return {'FINISHED'}