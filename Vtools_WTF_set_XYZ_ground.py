import bpy

class WTF_set_XYZ_ground(bpy.types.Operator):
  '''Sets the name of the object to XYZ-GROUND-PLANE.'''
  bl_idname = 'scene.wtf_set_xyz_ground'
  bl_label = 'WTF Set XYZ Ground'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    active_object = bpy.context.active_object

    ground_suffix = 'XYZ-GROUND-'
    ground_suffix_length = len(ground_suffix)
    #print(active_object.name[:ground_suffix_length])
    for obj in bpy.context.scene.objects:
      if obj.name[:ground_suffix_length] == ground_suffix:
        obj.name = obj.name[ground_suffix_length:]
    if active_object.name[:ground_suffix_length] != ground_suffix:
      active_object.name = 'XYZ-GROUND-' + active_object.name
    
    return {'FINISHED'}
