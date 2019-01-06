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
    original_cache_filepath = bpy.context.scene.render.filepath
    bpy.context.scene.render.filepath = '//cache\\' + 'cache_' + new_scene_name + '\\' + 'cache_' + new_scene_name + '_'
    # set antialiasing
    original_antialiasing = bpy.context.scene.cycles.pixel_filter_type
    bpy.context.scene.cycles.pixel_filter_type = 'GAUSSIAN'
    original_filter_width = bpy.context.scene.cycles.filter_width
    bpy.context.scene.cycles.filter_width = 1.5
    # Define nodes for relinking
    WTF_group      = bpy.data.node_groups['WTFgroup']
    WTF_XYZnode    = WTF_group.nodes['XYZgroup']
    WTF_Normalnode = WTF_group.nodes['Normalgroup']
    WTF_outputnode = WTF_group.nodes['WTF_Output_Node']
    # unlink XYZ node (unnecessary, creating a new link already removes the conflicting one)
    #for link in WTF_XYZnode.outputs[0].links:
    #  if link.to_socket == WTF_outputnode.inputs[0]:
    #    WTF_group.links.remove(link)
    # link Normal node
    WTF_group.links.new(WTF_Normalnode.outputs[0], WTF_outputnode.inputs[0])

    # generate new render nodes
    bpy.ops.nodes.generate_render_nodes()

    # ----------------------------------------------------------------------
    # render      
    bpy.ops.render.render(animation=True)
    # ----------------------------------------------------------------------

    # revert scene name
    bpy.context.scene.name = original_scene_name
    # revert cache path
    bpy.context.scene.render.filepath = original_cache_filepath
    # rever antialiasing
    bpy.context.scene.sycles.pixel_filter_type = original_antialiasing
    bpy.context.scene.cycles.filter_width = original_filter_width
    # revert WTF node group to XYZ
    WTF_group.links.new(WTF_XYZnode.outputs[0], WTF_outputnode.inputs[0])


    return {'FINISHED'}