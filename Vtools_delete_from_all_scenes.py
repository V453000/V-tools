import bpy

class delete_from_all_scenes(bpy.types.Operator):
  '''Delete selected objects from all scenes.'''
  bl_idname = 'object.delete_from_all_scenes'
  bl_label = 'Delete selected Objects from all Scenes'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):

    starting_scene_name = bpy.context.scene.name

    object_list = []
    for obj in bpy.context.selected_objects:
      object_list.append(obj.name)
    bpy.ops.object.select_all(action='DESELECT')
    
    for s in bpy.data.scenes:
      for obj_name in object_list:
        #bpy.context.screen.scene = s
        #bpy.context.scene.objects.active = obj
        #bpy.ops.object.delete()
        
        # unlink method - leaves materials and mesh data in scene :/
        #bpy.data.scenes[s.name].objects.unlink(bpy.data.scenes[s.name].objects[obj.name])
        
        bpy.context.screen.scene = s
        if bpy.context.scene.objects.get(obj_name) is not None:
          bpy.context.scene.objects[obj_name].select = True
      
      bpy.ops.object.delete()

    # revert back to the scene from which the command was launched
    
    bpy.context.screen.scene = bpy.data.scenes[starting_scene_name]

        

        
    return {'FINISHED'}