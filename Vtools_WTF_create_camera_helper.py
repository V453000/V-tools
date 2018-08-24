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

    # check if the mesh data exist in the blend file
    if bpy.data.meshes.get(camera_line_name) is None:
      print(camera_line_name, 'not found, generating...')
      bpy.data.meshes.new(camera_line_name).from_pydata(line_verts, line_edges, line_faces)
      line_mesh = bpy.data.meshes[camera_line_name]
      print('line_mesh is: ', line_mesh)
      '''camera_line_obj = bpy.data.objects.new(camera_line_name, line_mesh)#unused'''
    # if it exists, assign it to camera_line_obj for later use
    else:
      line_mesh = bpy.data.meshes[camera_line_name]
      '''camera_line_obj = bpy.data.objects[camera_line_name]#unused'''
      print(camera_line_name, 'already exists, proceeding...')
    
    ''' old trash
    if bpy.context.scene.camera is not None:
      print('Scene has camera, adding', camera_line_name)
      camera_children = []
      for child in bpy.context.scene.camera.children:
        camera_children.append([child.name, child.data.name])
      if camera_line_name in camera_children:
        print(camera_line_name, 'is already a child of camera, skipping...')
      else:
        scene_camera_line_obj = bpy.context.scene.objects.link(camera_line_obj)
        scene_camera_line_obj_name = scene_camera_line_obj.object.name
        bpy.context.scene.objects[scene_camera_line_obj_name].parent = bpy.context.scene.camera
    else:
      print('Scene has no camera, skipping...')
    '''

    # check if the scene has a camera, if not there is no point in continuing
    if bpy.context.scene.camera is not None:
      # check if any of the children uses the line mesh data
      camera_line_found_in_children = False
      for child in bpy.context.scene.camera.children:
        #camera_children.append([child.name, child.data.name])
        if child.data.name == camera_line_name:
          camera_line_found_in_children = True
      
      # if none of the children has the line data, find line objects in the scene to avoid creating an unwanted link
      if camera_line_found_in_children == False:
        camera_line_obj_name = camera_line_name
        camera_line_obj_number = 0
        
        # while the object already exists, try a different one
        while(bpy.data.objects.get(camera_line_obj_name) is not None):
          camera_line_obj_number += 1
          camera_line_obj_name = camera_line_name + '.' + format(int(camera_line_obj_number), '03d')

        # with the found object name, create the object data and link it to the current scene
        camera_line_obj_new = bpy.data.objects.new(camera_line_obj_name, line_mesh)
        scene_camera_line_obj = bpy.context.scene.objects.link(camera_line_obj_new)

        scene_camera_line_obj_name = scene_camera_line_obj.object.name
        bpy.context.scene.objects[scene_camera_line_obj_name].parent = bpy.context.scene.camera

    


    return {'FINISHED'}
