import bpy
import math

class default_render_settings(bpy.types.Operator):
  '''Set our default render settings.'''
  bl_idname = 'render.default_render_settings'
  bl_label = 'Default Render Settings'
  bl_options = {'REGISTER', 'UNDO'}
  

  set_for_all_scenes = bpy.props.BoolProperty(
    name = 'Set for all scenes',
    description = 'Set the following settings for all Scenes in this .blend file.',
    default = False
  )

  set_render_engine = bpy.props.EnumProperty(
    name = 'Render Engine',
    description = 'Select rendering engine',
    items = [
      ('CYCLES', 'Cycles',''),
      ('BLENDER_RENDER', 'Blender Render','')
    ]
  )

  set_render_device = bpy.props.EnumProperty(
    name = 'Render Device',
    description = 'Select rendering device. GPU can only be used by Cycles.',
    items = [
      ('GPU', 'GPU',''),
      ('CPU', 'CPU','')
    ]
  )

  resolution_mode = bpy.props.EnumProperty(
    name = 'Resolution mode',
    description = 'Choose if the render resolution should adapt to the camera Orthographic scale, if the camera should adapt to the render resolution, or set resolution manually.',
    items = [
      ('Smart Resolution', 'Smart Resolution', ''),
      ('Smart Camera'    , 'Smart Camera'    , ''),
      ('Manual'          , 'Manual'          , '')
    ]
  )

  set_resolution_x = bpy.props.IntProperty(
    name = 'Render Resolution X',
    default = 576
  )
  set_resolution_y = bpy.props.IntProperty(
    name = 'Render Resolution Y',
    default = 576
  )
  set_resolution_percentage = bpy.props.IntProperty(
    name = 'Resolution Percentage',
    default = 100
  )

  set_multicomputer = bpy.props.BoolProperty(
    name = 'Render on multiple computers',
    description = 'To render on multiple computers, the output filepath will change to a cache, enabling Placeholder and disabling Overwrite settings.',
    default = False
  )

  set_filepath = bpy.props.StringProperty(
    name = 'Render Output File Path',
    description = 'Path for render output, disabled if Multicomputer is used. Compositor File Output nodes are unaffected.',
    default = '//OUTPUT\\\\x\\x_'
  )

  set_image_compression = bpy.props.IntProperty(
    name = 'Image Compression',
    default = 0,
    min = 0,
    max = 100
  )

  set_frame_start_override = bpy.props.BoolProperty(
    name = 'Override Starting frame',
    description = 'Choose if the Starting frame should be changed',
    default = False
  )
  set_frame_start = bpy.props.IntProperty(
    name = 'Starting frame',
    description = 'Set the first rendered frame.',
    default = 0
  )

  set_frame_end_override = bpy.props.BoolProperty(
    name = 'Override Ending frame',
    description = 'Choose if the Ending frame should be changed',
    default = False
  )
  set_frame_end = bpy.props.IntProperty(
    name = 'Ending frame',
    description = 'Set the last rendered frame.',
    default = 0
  )
  

  set_use_border = bpy.props.BoolProperty(
    name = 'Use render border',
    description = 'Use the render border set by Ctrl+B.',
    default = False
  )
  set_crop_to_border = bpy.props.BoolProperty(
    name = 'Crop render to border',
    description = 'Crop the render to the border set by Ctrl+B.',
    default = False
  )

  set_samples = bpy.props.IntProperty(
    name = 'Samples',
    description = 'Rendering samples.',
    default = 1000
  )
  set_use_animated_seed = bpy.props.BoolProperty(
    name = 'Animated Seed for Samples',
    description = 'Each frame is rendered with different seed for sampling.',
    default = True
  )

  set_automatic_render_tile_size = bpy.props.BoolProperty(
    name = 'Automatic render tile size',
    description = 'Automatically set size of render tiles. Maximal for GPU, minimal for CPU.',
    default = True
  )
  set_render_tile_size_x = bpy.props.IntProperty(
    name = 'Manual render tile size X',
    description = 'Manually set X size of render tiles. Only works when Automatic render tile size is OFF.',
    default = 128
  )
  set_render_tile_size_y = bpy.props.IntProperty(
    name = 'Manual render tile size Y',
    description = 'Manually set Y size of render tiles. Only works when Automatic render tile size is OFF.',
    default = 128
  )

  set_transparent_max_bounces = bpy.props.IntProperty(
    name = 'Max Transparent Bounces',
    description = 'Limit the amount of light bounces used for transparency.',
    default = 0
  )
  set_caustics_reflective = bpy.props.BoolProperty(
    name = 'Reflective Caustics',
    description = 'Enable or disable reflective caustics.',
    default = False
  )
  set_caustics_refractive = bpy.props.BoolProperty(
    name = 'Refractive Caustics',
    description = 'Enable or disable refractive caustics.',
    default = False
  )
  set_transparent_film = bpy.props.BoolProperty(
    name = 'Transparent Film',
    description = 'Enable or disable Transparent film.',
    default = True
  )

  def execute(self,context):
    
    # settings for current scene or all scenes
    if self.set_for_all_scenes == False:
      list_of_scenes = [bpy.context.scene]
    else:
      list_of_scenes = []
      for scene in bpy.data.scenes:
        list_of_scenes.append(scene)

    for scn in list_of_scenes:
      # cycles
      scn.render.engine = self.set_render_engine

      # GPU rendering
      scn.cycles.device = self.set_render_device


      # Disable Border
      scn.render.use_crop_to_border = self.set_crop_to_border
      scn.render.use_border = self.set_use_border

      # Camera settings
      #obj_camera = bpy.data.objects['CAME-GAME']
      #obj_camera.data.ortho_scale = 36

      # File output path for scene
      if self.set_multicomputer == False:
        scn.render.filepath = self.set_filepath
        scn.render.use_overwrite = True
        scn.render.use_placeholder = False
      else:
        scn.render.filepath = '//cache\\\\' + scn.name + '/' + scn.name + '-cache_'
        scn.render.use_overwrite = False
        scn.render.use_placeholder = True


      # 1000 samples
      scn.cycles.samples = self.set_samples

      # Random seed for sampling
      scn.cycles.use_animated_seed = self.set_use_animated_seed

      # Light Paths and Caustics
      scn.cycles.transparent_max_bounces = self.set_transparent_max_bounces
      scn.cycles.caustics_reflective = self.set_caustics_reflective
      scn.cycles.caustics_refractive = self.set_caustics_refractive

      # Render Dimensions

      # get scene's camera
      

      if self.resolution_mode == 'Smart Resolution':
        if bpy.context.scene.camera is None:
          self.report({'ERROR'}, 'Scene has no active camera.')
        else:
          camera_ortho_scale = bpy.data.cameras[bpy.context.scene.camera.data.name].ortho_scale
          scn.render.resolution_x = round(camera_ortho_scale / 4 * 64)
          scn.render.resolution_y = round(camera_ortho_scale / 4 * 64)

      elif self.resolution_mode == 'Smart Camera':
        if bpy.context.scene.camera is None:
          self.report({'ERROR'}, 'Scene has no active camera.')
        else:
          bpy.data.cameras[bpy.context.scene.camera.data.name].ortho_scale = scn.render.resolution_x *4 /64

      else: # Manual mode
        scn.render.resolution_x = self.set_resolution_x
        scn.render.resolution_y = self.set_resolution_y
      
      # render resolution percentage
      scn.render.resolution_percentage = self.set_resolution_percentage

      # Render tile size
      if self.set_automatic_render_tile_size == True:
        if self.set_render_engine == 'CYCLES' and self.set_render_device == 'GPU':
          scn.render.tile_x = scn.render.resolution_x
          scn.render.tile_y = scn.render.resolution_x
        else:
          scn.render.tile_x = 32
          scn.render.tile_y = 32
      else:
        scn.render.tile_x = self.set_render_tile_size_x
        scn.render.tile_y = self.set_render_tile_size_y
      
      # PNG compression
      scn.render.image_settings.compression = self.set_image_compression

      # Transparent Film
      scn.cycles.film_transparent = self.set_transparent_film

      # start and end frame
      if self.set_frame_start_override == True:
        scn.frame_start = self.set_frame_start
      if self.set_frame_end_override == True:
        scn.frame_end = self.set_frame_end



    
    return {'FINISHED'}