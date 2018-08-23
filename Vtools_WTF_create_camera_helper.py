import bpy

class WTF_create_camera_helper(bpy.types.Operator):
  '''Creates camera alignment helper for XYZ rendering.'''
  bl_idname = 'scene.wtf_create_camera_helper'
  bl_label = 'Cam Helper'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    line_verts = [
      [0,0,0],
      [0,1,0]
    ] 
    line_edges = []
    line_faces = []
  
    #line_mesh = bpy.data.meshes.new('Camera-line').from_pydata(line_verts, line_edges line_faces)


    return {'FINISHED'}
