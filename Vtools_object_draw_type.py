import bpy

class object_draw_mode(bpy.types.Operator):
  '''Change draw mode of selected objects.'''
  bl_idname = 'object.draw_mode'
  bl_label = 'Object Draw Mode'
  bl_options = {'REGISTER', 'UNDO'}

  object_draw_mode_dropdown = bpy.props.EnumProperty(
    name = 'Mode',
    description = 'Maximum Draw Mode',
    items = [
      ('BOUNDS', 'BOUNDS',''),
      ('WIRE', 'WIRE',''),
      ('SOLID', 'SOLID',''),
      ('TEXTURED', 'TEXTURED','')
    ]
  )

  def execute(self, context):
    for obj in context.selected_objects:
      obj.draw_type = self.object_draw_mode_dropdown
      
    
    return {'FINISHED'}
