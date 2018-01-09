import bpy

class unpack_images(bpy.types.Operator):
  '''Unpack all packed images to /textures folder.'''
  bl_idname = 'scene.unpack_images'
  bl_label = 'Unpack Images'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
    for img in bpy.data.images:
      if img.packed_file is not None:
        img.unpack()
        print('Unpacked ' + img.name + ' to textures folder.')
      else:
        print(img.name + ' is not a packed file. Skipping.')

    return {'FINISHED'}