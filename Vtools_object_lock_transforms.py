import bpy

class object_lock_transforms(bpy.types.Operator):
  '''Lock or unlock the object transforms.'''
  bl_idname = 'object.object_lock_transforms'
  bl_label = 'Object Lock Transforms'
  bl_options = {'REGISTER', 'UNDO'}

  object_lock_transforms_LocX = bpy.props.BoolProperty(
    name = 'Location X',
    default = True
  )
  object_lock_transforms_LocY = bpy.props.BoolProperty(
    name = 'Location Y',
    default = True
  )
  object_lock_transforms_LocZ = bpy.props.BoolProperty(
    name = 'Location Z',
    default = True
  )
  object_lock_transforms_RotX = bpy.props.BoolProperty(
    name = 'Rotation X',
    default = True
  )
  object_lock_transforms_RotY = bpy.props.BoolProperty(
    name = 'Rotation Y',
    default = True
  )
  object_lock_transforms_RotZ = bpy.props.BoolProperty(
    name = 'Rotation Z',
    default = True
  )
  object_lock_transforms_ScaleX = bpy.props.BoolProperty(
    name = 'Scale X',
    default = True
  )
  object_lock_transforms_ScaleY = bpy.props.BoolProperty(
    name = 'Scale Y',
    default = True
  )
  object_lock_transforms_ScaleZ = bpy.props.BoolProperty(
    name = 'Scale Z',
    default = True
  )

  def execute(self, context):
    for obj in bpy.context.selected_objects:
      obj.lock_location[0] = self.object_lock_transforms_LocX
      obj.lock_location[1] = self.object_lock_transforms_LocY
      obj.lock_location[2] = self.object_lock_transforms_LocZ

      obj.lock_rotation[0] = self.object_lock_transforms_RotX
      obj.lock_rotation[1] = self.object_lock_transforms_RotY
      obj.lock_rotation[2] = self.object_lock_transforms_RotZ

      obj.lock_scale[0] =    self.object_lock_transforms_ScaleX
      obj.lock_scale[1] =    self.object_lock_transforms_ScaleY
      obj.lock_scale[2] =    self.object_lock_transforms_ScaleZ
    
    return {'FINISHED'}