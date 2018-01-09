import bpy

class subsurf_settings(bpy.types.Operator):
  '''Change settings of all subsurf modifiers on selected objects.'''
  bl_idname = 'object.subsurf_settings'
  bl_label = 'Subsurf Settings'
  bl_options = {'REGISTER', 'UNDO'}


  subsurf_algorithm = bpy.props.EnumProperty(
    name = 'Mode',
    description = 'Subdivision Algorithm',
    items = [
      ('CATMULL_CLARK', 'Catmull-Clark',''),
      ('SIMPLE', 'Simple','')
    ]
  )
  subsurf_render_visibility = bpy.props.BoolProperty(
    name = 'Render Visibility',
    default = True
  )
  subsurf_viewport_visibility = bpy.props.BoolProperty(
    name = 'Viewport Visibility',
    default = True
  )
  subsurf_editmode_visibility = bpy.props.BoolProperty(
    name = 'Edit Mode Visibility',
    default = True
  )
  subsurf_cage_visibility = bpy.props.BoolProperty(
    name = 'On Cage Visibility',
    default = True
  )
  
  
  subsurf_change_levels = bpy.props.BoolProperty(
    name = 'ChangeViewport Levels',
    default = False
  )
  subsurf_levels = bpy.props.IntProperty(
    name = 'Subsurf Levels',
    default = 1
  )

  subsurf_change_render_levels = bpy.props.BoolProperty(
    name = 'Change Render Levels',
    default = False
  )
  subsurf_render_levels = bpy.props.IntProperty(
    name = 'Subsurf Render Levels',
    default = 2
  )
  


  subsurf_adaptive_subdivision = bpy.props.BoolProperty(
    name = 'Adaptive Subdivision',
    default = False
  )
  subsurf_adaptive_dicing_rate = bpy.props.FloatProperty(
    name = 'Adaptive Dicing Rate',
    default = 1.0
  )


  def execute(self, context):
    
    for obj in bpy.context.selected_objects:
      bpy.context.scene.objects.active = obj
      subsurf_found = False

      if not obj.modifiers:
        print(obj.name + " has no modifiers")
      else:
        for modifier in obj.modifiers:
          if modifier.type == "SUBSURF":
            subsurf_found = True
            modifier.subdivision_type = self.subsurf_algorithm
            modifier.show_render =      self.subsurf_render_visibility
            modifier.show_viewport =    self.subsurf_viewport_visibility
            modifier.show_in_editmode = self.subsurf_editmode_visibility
            modifier.show_on_cage =     self.subsurf_cage_visibility
            if self.subsurf_change_levels == True:
              modifier.levels =           self.subsurf_levels
            if self.subsurf_change_render_levels == True:
              modifier.render_levels =    self.subsurf_render_levels
         
          else:
            print("No Subsurf modifiers for " + obj.name)

      if subsurf_found == True:
        obj.cycles.use_adaptive_subdivision = self.subsurf_adaptive_subdivision
        obj.cycles.dicing_rate = self.subsurf_adaptive_dicing_rate

    return {'FINISHED'}