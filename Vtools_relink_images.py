import bpy

class relink_images(bpy.types.Operator):
  '''Relinks all image paths to a different folder.'''
  bl_idname = 'scene.relink_images'
  bl_label = 'Relink Images'
  bl_options = {'REGISTER', 'UNDO'}

  old_path = bpy.props.StringProperty(
    name = 'Old Path',
    description = 'Original path to convert from.',
    default = '10.0.0.1\\tank_volume1'
  )
  new_path = bpy.props.StringProperty(
    name = 'New Path',
    description = 'Destination path to convert to.',
    default = 'nas.factorio.com\\tank'
  )


  def execute(self, context):
    
    for img in bpy.data.images:
      #print(img.filepath)
      image_filename = img.filepath
      
      if self.old_path in image_filename:
        print('Found and replaced a filename to:')
        replaced_image = image_filename.replace(self.old_path, self.new_path)
        img.filepath = replaced_image
        print(replaced_image)
    return {'FINISHED'}