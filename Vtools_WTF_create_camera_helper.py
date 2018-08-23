import bpy

class WTF_create_camera_helper(bpy.types.Operator):
  '''Creates camera alignment helper for XYZ rendering.'''
  bl_idname = 'scene.wtf_create_camera_helper'
  bl_label = 'Cam Helper'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    line_verts = [
      [ 0, 0, 0], #0
      [ 0, 0, -1], #1

      [-1, 1, 1], #2
      [ 1, 1, 1], #3
      [-1,-1, 1], #4
      [ 1,-1, 1], #5

    ] 
    line_edges = [
      (0,1), #main line

      (0,2), #lines behind camera
      (0,3), #lines behind camera
      (0,4), #lines behind camera
      (0,5), #lines behind camera

      (2,3), #lines behind camera
      (2,4), #lines behind camera
      (3,5), #lines behind camera
      (4,5), #lines behind camera
    ]
    line_faces = []
  
    camera_line_name = 'Camera-line'

    if bpy.data.meshes.get(camera_line_name) is None:
      print(camera_line_name, 'not found, generating...')
      bpy.data.meshes.new(camera_line_name).from_pydata(line_verts, line_edges, line_faces)
      line_mesh = bpy.data.meshes[camera_line_name]
      print('line_mesh is: ', line_mesh)
      camera_line_obj = bpy.data.objects.new(camera_line_name, line_mesh)
    else:
      print(camera_line_name, 'already exists, proceeding...')
    
    if bpy.context.scene.camera is not None:
      print('Scene has camera, adding', camera_line_name)
      camera_children = []
      for child in bpy.context.scene.camera.children:
        camera_children.append(child.name)
      if camera_line_name in camera_children:
        print(camera_line_name, 'is already a child of camera, skipping...')
      else:
        scene_camera_line_obj = bpy.context.scene.objects.link(camera_line_obj)
        scene_camera_line_obj_name = scene_camera_line_obj.object.name
        bpy.context.scene.objects[scene_camera_line_obj_name].parent = bpy.context.scene.camera
    else:
      print('Scene has no camera, skipping...')

    


    return {'FINISHED'}
