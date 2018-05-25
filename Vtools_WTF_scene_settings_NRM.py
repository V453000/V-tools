import bpy

class WTF_scene_settings_NRM(bpy.types.Operator):
  '''Convert all scenes to NRM map rendering.'''
  bl_idname = 'scene.wtf_scene_settings_nrm'
  bl_label = 'NRM Settings'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
    # apply shared settings
    bpy.ops.scene.wtf_scene_settings_shared()

    # generate material
    bpy.ops.scene.wtf_generate_material_nrm()

    # set material override on all RenderLayers
    for scene in bpy.data.scenes:
      for renderlayer in scene.render.layers:
        renderlayer.material_override = bpy.data.materials['Normalmap']

    return {'FINISHED'}