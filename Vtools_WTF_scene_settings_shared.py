import bpy

class WTF_scene_settings_shared(bpy.types.Operator):
  '''Convert all scenes to special map rendering.'''
  bl_idname = 'scene.wtf_scene_settings_shared'
  bl_label = 'WTF Scene Settings'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):

    def xyz_render_settings():
      scene = bpy.context.scene

      scene.render.engine = 'CYCLES'
      #bpy.context.scene.render.engine = 'BLENDER_RENDER'
      scene.view_settings.view_transform = 'Raw'

      scene.render.image_settings.compression = 0

      scene.cycles.samples = 1
      scene.cycles.max_bounces = 0
      scene.cycles.min_bounces = 0
      scene.cycles.diffuse_bounces = 0
      scene.cycles.glossy_bounces = 0
      scene.cycles.transmission_bounces = 0
      scene.cycles.volume_bounces = 0

      scene.view_settings.exposure = 0
      scene.view_settings.gamma = 1

      scene.cycles.use_transparent_shadows = False
      scene.cycles.caustics_reflective = False
      scene.cycles.caustics_refractive = False

      #scene.cycles.pixel_filter_type = 'GAUSSIAN'
      #scene.cycles.pixel_filter_type = 'BLACKMAN_HARRIS'
      #scene.cycles.filter_width = 0.01

      scene.cycles.pixel_filter_type = 'BOX'

      scene.render.image_settings.color_depth = '16'

      if scene.cycles.device == 'CPU':
        scene.render.tile_x = 64
        scene.render.tile_y = 64
      else:
        scene.render.tile_x = scene.render.resolution_x
        scene.render.tile_y = scene.render.resolution_y


    def remove_lights():
      #remove all lamps
      for obj in bpy.data.objects:
        if obj.type == 'LAMP':
          bpy.data.objects.remove(obj)

    def clean_renderlayers():
      for scene in bpy.data.scenes:
        for renderlayer in scene.render.layers:
          remove_layer = False
          shadow_appendix = 'shadow'
          height_appendix = 'height'
          mask_appendix = 'mask'
          shadow_appendix_count = len(shadow_appendix)
          height_appendix_count = len(height_appendix)
          mask_appendix_count = len(mask_appendix)

          print(renderlayer.name[:shadow_appendix_count])
          # see if the layer needs to be removed
          if renderlayer.name[-shadow_appendix_count:].lower() == shadow_appendix.lower():
            if renderlayer.use_pass_shadow == True:
              remove_layer = True
          elif renderlayer.name[-height_appendix_count:].lower() == height_appendix.lower():
            if renderlayer.material_override is not None:
              remove_layer = True
          elif renderlayer.name[-mask_appendix_count:].lower() == mask_appendix.lower():
            remove_layer = True
          
          if renderlayer.name[:shadow_appendix_count].lower() == shadow_appendix.lower():
            if renderlayer.use_pass_shadow == True:
              remove_layer = True
          elif renderlayer.name[:height_appendix_count].lower() == height_appendix.lower():
            if renderlayer.material_override is not None:
              remove_layer = True
          elif renderlayer.name[:mask_appendix_count].lower() == mask_appendix.lower():
            remove_layer = True
          # remove the layer if it should be removed
          if remove_layer == True:
            scene.render.layers.remove(renderlayer)


    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                        E X E C U T E   T O O L
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    xyz_render_settings()
    remove_lights()
    clean_renderlayers()

    return {'FINISHED'}
