import bpy

class WTF_scene_settings_XYZ(bpy.types.Operator):
  '''Convert all scenes to XYZ map rendering.'''
  bl_idname = 'scene.wtf_scene_settings_xyz'
  bl_label = 'XYZ Settings'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
    # apply shared settings
    bpy.ops.scene.wtf_scene_settings_shared()
    
    # generate material
    bpy.ops.scene.wtf_generate_material_xyz()

    # set material override on all RenderLayers
    for scene in bpy.data.scenes:
      for renderlayer in scene.render.layers:
        renderlayer.material_override = bpy.data.materials['XYZmap']

    return {'FINISHED'}