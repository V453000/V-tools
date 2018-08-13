import bpy
import math

class WTF_render_XYZ(bpy.types.Operator):
  '''Renders every frame with all the XYZ map rotations, adjusting the scene name and auto-generating output nodes.'''
  bl_idname = 'scene.wtf_render_xyz'
  bl_label = 'Render XYZ'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):

    def get_override(area_type, region_type):
      for area in bpy.context.screen.areas: 
        if area.type == area_type:             
          for region in area.regions:                 
            if region.type == region_type:                    
              override = {'area': area, 'region': region} 
              return override
      #error message if the area or region wasn't found
      raise RuntimeError("Wasn't able to find", region_type," in area ", area_type,
                          "\n Make sure it's open while executing script.")
    
    camera_angles = [
      ( 0              ),
      ( math.pi* 4 /6 ),
      ( math.pi* 8 /6 ),

      ( math.pi* 6 /6 ),
      ( math.pi* 10/6 ),
      ( math.pi* 2 /6 ),
      
      ( math.pi/2      )
    ]
    
    # set render settings
    #bpy.ops.scene.xyz_convert_scene()

    # increase the resolution
    #bpy.context.scene.render.resolution_x = bpy.context.scene.render.resolution_x * 2
    #bpy.context.scene.render.resolution_y = bpy.context.scene.render.resolution_y * 2

    # get camera highest parent
    camera_obj = bpy.context.scene.camera
    print('Original camera location', camera_obj.matrix_world.to_translation() )

    camera_boss_object = camera_obj
    while(camera_boss_object.parent is not None):
      camera_boss_object = camera_boss_object.parent

    
    
    camera_obj.constraints['XYZ_TRACK_TO'].mute = True
    camera_original_matrix = camera_obj.matrix_world.copy()
    camera_boss_object_original_matrix = camera_boss_object.matrix_world.copy()
    camera_obj.constraints['XYZ_TRACK_TO'].mute = False

    camera_original_rotation = camera_obj.rotation_euler.copy()
    camera_boss_object_original_rotation = camera_boss_object.rotation_euler.copy()
    camera_boss_object_original_rotation_matrix = camera_boss_object.matrix_world.to_euler().copy()

    # save starting frame
    frame_start = bpy.context.scene.frame_start
    # save ending frame
    frame_end = bpy.context.scene.frame_end

    # save scene name before starting to change it
    original_scene_name = bpy.context.scene.name
    
    # read the resolution and set it to double before rendering
    resolution_multiplier = 2

    resolution_percentage = bpy.context.scene.render.resolution_percentage
    bpy.context.scene.render.resolution_percentage = resolution_percentage*resolution_multiplier
    bpy.context.scene.render.tile_x = bpy.context.scene.render.resolution_x *resolution_multiplier
    bpy.context.scene.render.tile_y = bpy.context.scene.render.resolution_y *resolution_multiplier
    
    # enable all layers
    for i in range(0,20):
      bpy.context.scene.layers[i] = True

    # iterate through frames and render each one individually
    for f in range(frame_start, frame_end+1):

      # render just the individual frame
      bpy.context.scene.frame_start = f
      bpy.context.scene.frame_end = f
      # set the correct frame so that it regenerates the materials with the correct camera position
      bpy.context.scene.frame_set(f)
      # set XYZ settings for every frame (only useful when the camera has actually moved/rotated)
      bpy.ops.scene.wtf_scene_settings_xyz()

      # iterate through XYZ view
      for i in range(0, 7):

        i_2d = format(i,'02d')
        # change scene name with i
        new_scene_name = original_scene_name + '_XYZ-' + str(i_2d)
        bpy.context.scene.name = new_scene_name
        # generate new render nodes
        bpy.ops.nodes.generate_render_nodes()
        
        # rotate boss object
        camera_boss_object.rotation_euler[2] = camera_boss_object_original_rotation_matrix[2] + camera_angles[i]
        
        # move camera in Z (rotation handled by constraint)
        if i == 3 or i == 4 or i == 5 :
          camera_obj.matrix_world.translation[2] = camera_original_matrix.translation[2] /2

        else:
          camera_obj.matrix_world.translation[2] = camera_original_matrix.translation[2]

        if i == 6:
          camera_obj.matrix_world.translation[0] = camera_boss_object.matrix_world.translation[0]
          camera_obj.matrix_world.translation[1] = camera_boss_object.matrix_world.translation[1]
          camera_obj.matrix_world.translation[2] *= 2

          # special handling for top view
          bpy.context.scene.camera.constraints['XYZ_TRACK_TO'].mute = True

          loc_camera = camera_obj.matrix_world.to_translation().copy()
          target_point = camera_boss_object.matrix_world.to_translation().copy()
          direction = target_point - loc_camera
          rot_quat = direction.to_track_quat('-Z', 'Y')
          camera_obj.rotation_euler = rot_quat.to_euler()
          camera_obj.rotation_euler[2] -= math.pi/2

        # render debug
        #bpy.context.scene.render.filepath = '//debug\\' + 'debug_' + new_scene_name + '\\' + 'debug_' + new_scene_name + '_'
        #bpy.ops.render.opengl(animation=True)

        # change cache path
        bpy.context.scene.render.filepath = '//cache\\' + 'cache_' + new_scene_name + '\\' + 'cache_' + new_scene_name + '_'
        
        '''--------------------------------------------------------'''
        '''------------------------ RENDER ------------------------'''
        # render      
        bpy.ops.render.render(animation=True)
        '''------------------------        ------------------------'''
        '''--------------------------------------------------------'''

        # revert camera transforms
        #camera_obj.rotation_euler = camera_original_rotation
        #camera_boss_object.rotation_euler = camera_boss_object_original_rotation
        #camera_obj.matrix_world.translation[0] = camera_original_x
        #camera_obj.matrix_world.translation[1] = camera_original_y
        #camera_obj.matrix_world.translation[2] = camera_original_z

        # turn TrackTo constraint back on
        bpy.context.scene.camera.constraints['XYZ_TRACK_TO'].mute = True
        camera_boss_object.matrix_world = camera_boss_object_original_matrix.copy()
        camera_obj.matrix_world = camera_original_matrix.copy()
        bpy.context.scene.camera.constraints['XYZ_TRACK_TO'].mute = False
        camera_boss_object.rotation_euler = camera_boss_object_original_rotation.copy()
        camera_obj.rotation_euler = camera_original_rotation.copy()
  
        print('View', i_2d, 'finished...')  
      
      # revert the original scene back as if nothing happened
      bpy.context.scene.name = original_scene_name
      
    # revert the resolution
    bpy.context.scene.render.resolution_percentage = resolution_percentage
    return {'FINISHED'}