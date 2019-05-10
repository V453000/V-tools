import bpy
import math

class WTF_render_Normal(bpy.types.Operator):
  '''Renders Normal map.'''
  bl_idname = 'scene.wtf_render_normal'
  bl_label = 'Render Normal'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):

    # make sure there is a camera in the scene
    if bpy.context.scene.camera is not None:
      # enable all layers
      for i in range(0,20):
        bpy.context.scene.layers[i] = True

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
      # sampling
      original_samples = bpy.context.scene.cycles.samples
      original_max_bounces = bpy.context.scene.cycles.max_bounces
      original_min_bounces = bpy.context.scene.cycles.min_bounces
      original_diffuse_bounces = bpy.context.scene.cycles.diffuse_bounces
      original_glossy_bounces = bpy.context.scene.cycles.glossy_bounces
      original_transmission_bounces = bpy.context.scene.cycles.transmission_bounces
      original_volume_bounces = bpy.context.scene.cycles.volume_bounces
      # resolution
      resolution_multiplier = 1
      #resolution_percentage = bpy.context.scene.render.resolution_percentage
      #bpy.context.scene.render.resolution_percentage = resolution_percentage*resolution_multiplier
      original_resolution_x = bpy.context.scene.render.resolution_x
      original_resolution_y = bpy.context.scene.render.resolution_y
      bpy.context.scene.render.tile_x = bpy.context.scene.render.resolution_x *resolution_multiplier
      bpy.context.scene.render.tile_y = bpy.context.scene.render.resolution_y *resolution_multiplier

        

      bpy.context.scene.cycles.samples = 1000
      bpy.context.scene.cycles.max_bounces = 0
      bpy.context.scene.cycles.min_bounces = 0
      bpy.context.scene.cycles.diffuse_bounces = 0
      bpy.context.scene.cycles.glossy_bounces = 0
      bpy.context.scene.cycles.transmission_bounces = 0
      bpy.context.scene.cycles.volume_bounces = 0


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
      bpy.context.scene.cycles.pixel_filter_type = original_antialiasing
      bpy.context.scene.cycles.filter_width = original_filter_width
      # revert WTF node group to XYZ
      WTF_group.links.new(WTF_XYZnode.outputs[0], WTF_outputnode.inputs[0])
      # revert sampling
      bpy.context.scene.cycles.samples = original_samples
      bpy.context.scene.cycles.max_bounces = original_max_bounces
      bpy.context.scene.cycles.min_bounces = original_min_bounces
      bpy.context.scene.cycles.diffuse_bounces = original_diffuse_bounces
      bpy.context.scene.cycles.glossy_bounces = original_glossy_bounces
      bpy.context.scene.cycles.transmission_bounces = original_transmission_bounces
      bpy.context.scene.cycles.volume_bounces = original_volume_bounces
      # revert resolution
      bpy.context.scene.render.tile_x = original_resolution_x
      bpy.context.scene.render.tile_y = original_resolution_y

    return {'FINISHED'}