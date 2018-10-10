import bpy

class duplicate_render_layer(bpy.types.Operator):
  '''Duplicate the currently active render layer.'''
  bl_idname = 'scene.duplicate_render_layer'
  bl_label = 'Duplicate RenderLayer'
  bl_options = {'REGISTER', 'UNDO'}
  
  set_appendix = bpy.props.StringProperty(
    name = 'Copy Appendix',
    description = 'Text added to the end of the duplicated RenderLayer.',
    default = '-copy'
  )
  set_target_scene = bpy.props.StringProperty(
    name = 'Target scene name',
    description = 'Name of target scene.',
    default = ''
  )
  set_source_scene = bpy.props.StringProperty(
    name = 'Source scene',
    description = 'Name of scene to copy from.',
    default = ''
  )
  set_source_render_layer = bpy.props.StringProperty(
    name = 'Source render layer',
    description = 'Name of render layer to copy.',
    default = ''
  )

  def execute(self, context):
    if self.set_source_scene == '':
      scene = bpy.context.scene
    else:
      scene = bpy.data.scenes[self.set_source_scene]
    render_layers = scene.render.layers

    if self.set_target_scene == '':
      target_scene = bpy.context.scene
    else:
      target_scene = bpy.data.scenes[self.set_target_scene]

    # read selected renderlayer
    if self.set_source_render_layer == '':
      selected_render_layer = render_layers.active
    else:
      selected_render_layer = scene.render.layers[self.set_source_render_layer]


    original_name = selected_render_layer.name
    copy_name = original_name + self.set_appendix
    
    target_render_layers = target_scene.render.layers
    target_render_layers.new(copy_name)


    original = render_layers[original_name]
    copy = target_render_layers[copy_name]

    # layer settings
    for i in range(0,20):
      # visible settings
      copy.layers[i]         = original.layers[i]
      # exclude settings
      copy.layers_exclude[i] = original.layers_exclude[i]
      # mask settings
      copy.layers_zmask[i]    = original.layers_zmask[i]

    copy.material_override = original.material_override

    copy.use_sky        =     original.use_sky
    copy.use_ao         =     original.use_ao
    copy.use_solid      =     original.use_solid
    copy.use_strand     =     original.use_strand

    copy.use_pass_combined       = original.use_pass_combined
    copy.use_pass_z              = original.use_pass_z
    copy.use_pass_mist           = original.use_pass_mist
    copy.use_pass_normal         = original.use_pass_normal
    copy.use_pass_vector         = original.use_pass_vector
    copy.use_pass_uv             = original.use_pass_uv
    copy.use_pass_object_index   = original.use_pass_object_index
    copy.use_pass_material_index = original.use_pass_material_index

    copy.use_pass_diffuse_direct        = original.use_pass_diffuse_direct
    copy.use_pass_diffuse_indirect      = original.use_pass_diffuse_indirect
    copy.use_pass_diffuse_color         = original.use_pass_diffuse_color
    copy.use_pass_glossy_direct         = original.use_pass_glossy_direct
    copy.use_pass_glossy_indirect       = original.use_pass_glossy_indirect
    copy.use_pass_glossy_color          = original.use_pass_glossy_color
    copy.use_pass_transmission_direct   = original.use_pass_transmission_direct
    copy.use_pass_transmission_indirect = original.use_pass_transmission_indirect
    copy.use_pass_transmission_color    = original.use_pass_transmission_color
    copy.use_pass_subsurface_direct     = original.use_pass_subsurface_direct
    copy.use_pass_subsurface_indirect   = original.use_pass_subsurface_indirect
    copy.use_pass_subsurface_color      = original.use_pass_subsurface_color

    copy.use_pass_shadow            = original.use_pass_shadow
    copy.use_pass_ambient_occlusion = original.use_pass_ambient_occlusion
    copy.use_pass_emit              = original.use_pass_emit
    copy.use_pass_environment       = original.use_pass_environment

    copy.pass_alpha_threshold = original.pass_alpha_threshold

    #copy.use_denoising               = original.use_denoising
    #copy.udenoising_radius           = original.denoising_radius
    #copy.udenoising_strength         = original.denoising_strength
    #copy.udenoising_feature_strength = original.denoising_feature_strength
    #copy.udenoising_relative_pca     = original.denoising_relative_pca
    #
    #copy.udenoising_diffuse_direct        = original.denoising_diffuse_direct
    #copy.udenoising_diffuse_indirect      = original.denoising_diffuse_indirect
    #copy.udenoising_glossy_direct         = original.denoising_glossy_direct
    #copy.udenoising_glossy_indirect       = original.denoising_glossy_indirect
    #copy.udenoising_transmission_direct   = original.denoising_transmission_direct
    #copy.udenoising_transmission_indirect = original.denoising_transmission_indirect
    #copy.udenoising_subsurface_direct     = original.denoising_subsurface_direct
    #copy.udenoising_subsurface_indirect   = original.denoising_subsurface_indirect

    return {'FINISHED'}
