import bpy

class object_cycles_settings(bpy.types.Operator):
  '''Change cycles settings of selected objects.'''
  bl_idname = 'object.object_cycles_settings'
  bl_label = 'Object Cycles Settings'
  bl_options = {'REGISTER', 'UNDO'}

  object_cycles_settings_camera = bpy.props.BoolProperty(
    name = 'Camera',
    description = 'Camera',
    default = False
  )
  object_cycles_settings_diffuse = bpy.props.BoolProperty(
    name = 'Diffuse',
    description = 'Diffuse',
    default = False
  )
  object_cycles_settings_glossy = bpy.props.BoolProperty(
    name = 'Glossy',
    description = 'Glossy',
    default = False
  )
  object_cycles_settings_transmission = bpy.props.BoolProperty(
    name = 'Transmission',
    description = 'Transmission',
    default = False
  )
  object_cycles_settings_scatter = bpy.props.BoolProperty(
    name = 'Volume',
    description = 'Volume Scatter',
    default = False
  )
  object_cycles_settings_shadow = bpy.props.BoolProperty(
    name = 'Shadow',
    description = 'Shadow',
    default = False
  )
  object_cycles_settings_shadow_catcher = bpy.props.BoolProperty(
    name = 'Shadow Catcher',
    description = 'Shadow Catcher',
    default = False
  )

  def execute(self, context):
    for obj in bpy.context.selected_objects:
        bpy.context.scene.objects.active = obj
        bpy.context.object.cycles_visibility.camera =       self.object_cycles_settings_camera
        bpy.context.object.cycles_visibility.diffuse =      self.object_cycles_settings_diffuse
        bpy.context.object.cycles_visibility.glossy =       self.object_cycles_settings_glossy
        bpy.context.object.cycles_visibility.transmission = self.object_cycles_settings_transmission
        bpy.context.object.cycles_visibility.scatter =      self.object_cycles_settings_scatter
        bpy.context.object.cycles_visibility.shadow =       self.object_cycles_settings_shadow
        bpy.context.object.cycles.is_shadow_catcher =       self.object_cycles_settings_shadow_catcher
    
    return {'FINISHED'}