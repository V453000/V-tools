import bpy
import math

class XYZ_render(bpy.types.Operator):
  '''Renders every frame with all the XYZ map rotations, adjusting the scene name and auto-generating output nodes.'''
  bl_idname = 'scene.xyz_render'
  bl_label = 'XYZ Render'
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

    # set render settings
    bpy.ops.scene.xyz_convert_scene()

    # put cursor to zero
    bpy.context.scene.cursor_location = (0,0,0)
    
    # get camera
    camera_obj = bpy.context.scene.camera
    
    # deselect everything
    bpy.ops.object.select_all(action='DESELECT')
    camera_obj.select = True
    bpy.context.scene.objects.active = camera_obj

    # save scene name before starting to change it
    original_scene_name = bpy.context.scene.name
    # iterate through XYZ views
    for i in range(0, 13):
      print(i)
      i_2d = format(i,'02d')
      # change scene name with i
      new_scene_name = original_scene_name + '_XYZ-' + str(i_2d)
      bpy.context.scene.name = new_scene_name
      # generate new render nodes
      bpy.ops.nodes.generate_render_nodes()
      # rotate camera
      rot_x = 0
      rot_y = 0
      rot_z = i*math.pi/4
      if i >= 8:
        rot_x = math.pi/16*3
        rot_z = i*math.pi/2
      if i == 12:
        rot_x = -math.pi/4
        rot_z = 0

      bpy.data.objects['Camera-Parent'].rotation_euler = (rot_x,rot_y,rot_z)

      # change cache path
      bpy.context.scene.render.filepath = '//cache\\' + 'cache_' + new_scene_name + '\\' + 'cache_' + new_scene_name + '_'
      # render      
      bpy.ops.render.render(animation=True)
      print('View', i_2d, 'finished...')  

    # revert the original scene back as if nothing happened
    bpy.context.scene.name = original_scene_name
    bpy.data.objects['Camera-Parent'].rotation_euler = (0,0,0)
    return {'FINISHED'}