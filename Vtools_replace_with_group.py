import bpy

class replace_with_group(bpy.types.Operator):
  '''Replace selected objects with group instances.'''
  bl_idname = 'object.replace_with_group'
  bl_label = 'Replace selected objects with group instances.'
  bl_options = {'REGISTER', 'UNDO'}

  target_group = bpy.props.StringProperty(
    name = 'Group',
    description = 'Group to replace with.',
    default = ''
  )

  def execute(self, context):

    object_list = []
    for obj in bpy.context.selected_objects:
      object_list.append(obj.name)
    
    for obj_name in object_list:
      if self.target_group is not '':
        if bpy.data.groups[self.target_group] is not None:
          new_group = bpy.data.objects.new('New thing', None)
          new_group.dupli_type = 'GROUP'
          new_group.dupli_group = bpy.data.groups[self.target_group]

          new_group.layers         = bpy.context.scene.objects[obj_name].layers
          new_group.location       = bpy.context.scene.objects[obj_name].location
          new_group.rotation_euler = bpy.context.scene.objects[obj_name].rotation_euler
          new_group.scale          = bpy.context.scene.objects[obj_name].scale
          bpy.data.objects.remove(bpy.context.scene.objects[obj_name])
          new_group.name           = obj_name

          bpy.context.scene.objects.link(new_group)

    return {'FINISHED'}