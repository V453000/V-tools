import bpy
import math

class WTF_render_Normal(bpy.types.Operator):
  '''Renders Normal map.'''
  bl_idname = 'scene.wtf_render_normal'
  bl_label = 'Render Normal'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    # save scene name and change it
    original_scene_name = bpy.context.scene.name
    new_scene_name = original_scene_name + '_Normal'
    bpy.context.scene.name = new_scene_name
    # set cache path
    bpy.context.scene.render.filepath = '//cache\\' + 'cache_' + new_scene_name + '\\' + 'cache_' + new_scene_name + '_'

    # generate new render nodes
    bpy.ops.nodes.generate_render_nodes()

    # render      
    bpy.ops.render.render(animation=True)

    # revert scene name
    bpy.context.scene.name = original_scene_name

    return {'FINISHED'}