import bpy

class link_to_all_scenes(bpy.types.Operator):
  '''Link selected objects to all scenes.'''
  bl_idname = 'object.link_to_all_scenes'
  bl_label = 'Link Objects to all Scenes'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):

    currentScene = bpy.context.scene
    for s in bpy.data.scenes:
      if s != currentScene:
        bpy.ops.object.make_links_scene(scene=s.name)
        print("Linked to " + s.name)

    return {'FINISHED'}