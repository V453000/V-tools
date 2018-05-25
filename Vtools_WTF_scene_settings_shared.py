import bpy

class WTF_scene_settings_shared(bpy.types.Operator):
  '''Convert all scenes to special map rendering.'''
  bl_idname = 'scene.wtf_scene_settings_shared'
  bl_label = 'WTF Scene Settings'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
    def xyz_render_settings():
      bpy.context.scene.render.engine = 'CYCLES'
      #bpy.context.scene.render.engine = 'BLENDER_RENDER'
      bpy.context.scene.view_settings.view_transform = 'Raw'

      bpy.context.scene.render.image_settings.compression = 0

      bpy.context.scene.cycles.samples = 1
      bpy.context.scene.cycles.max_bounces = 0
      bpy.context.scene.cycles.min_bounces = 0
      bpy.context.scene.cycles.diffuse_bounces = 0
      bpy.context.scene.cycles.glossy_bounces = 0
      bpy.context.scene.cycles.transmission_bounces = 0
      bpy.context.scene.cycles.volume_bounces = 0

      bpy.context.scene.cycles.use_transparent_shadows = False
      bpy.context.scene.cycles.caustics_reflective = False
      bpy.context.scene.cycles.caustics_refractive = False

      bpy.context.scene.cycles.pixel_filter_type = 'GAUSSIAN'
      bpy.context.scene.cycles.filter_width = 1.5

    
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
          shadow_appendix_count = len(shadow_appendix)
          height_appendix_count = len(height_appendix)

          print(renderlayer.name[:shadow_appendix_count])
          # see if the layer needs to be removed
          if renderlayer.name[-shadow_appendix_count:].lower() == shadow_appendix.lower():
            if renderlayer.use_pass_shadow == True:
              remove_layer = True
          elif renderlayer.name[-height_appendix_count:].lower() == height_appendix.lower():
            if renderlayer.material_override is not None:
              remove_layer = True
          if renderlayer.name[:shadow_appendix_count].lower() == shadow_appendix.lower():
            if renderlayer.use_pass_shadow == True:
              remove_layer = True
          elif renderlayer.name[:height_appendix_count].lower() == height_appendix.lower():
            if renderlayer.material_override is not None:
              remove_layer = True
          # remove the layer if it should be removed
          if remove_layer == True:  
            bpy.context.scene.render.layers.remove(renderlayer)

    
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                        E X E C U T E   T O O L
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    xyz_render_settings()
    remove_lights()
    clean_renderlayers()

    return {'FINISHED'}