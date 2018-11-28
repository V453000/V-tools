import bpy

class object_unlock(bpy.types.Operator):
  '''Set if objects should be selectible and visible in viewport or render.'''
  bl_idname = 'object.object_unlock'
  bl_label = 'Viewport settings'
  bl_options = {'REGISTER', 'UNDO'}

  set_targets = bpy.props.EnumProperty(
    name = 'Targets',
    description = 'Which objects to use - All in blend file, all in the current scene or all in the current selection.',
    items = [
      ('Selected', 'Selected'      , '', 'RESTRICT_SELECT_OFF'   , 0),
      ('Scene'   , 'Current Scene' , '', 'SCENE_DATA'            , 1),
      ('All'     , 'All scenes'    , '', 'BLENDER'               , 2)
    ]
  )
  set_viewport = bpy.props.EnumProperty(
    name = 'Viewport visibility',
    description = 'Choose whether objects should show in viewport.',
    items = [
      ('No change' , 'No change'   , '', 'PANEL_CLOSE'               , 1),
      ('Visible'   , 'Visible'     , '', 'VISIBLE_IPO_ON'            , 1),
      ('Hidden'    , 'Hidden'      , '', 'VISIBLE_IPO_OFF'           , 2)
    ]
  )
  set_select = bpy.props.EnumProperty(
    name = 'Selecting',
    description = 'Choose whether objects should be selectible.',
    items = [
      ('No change'   , 'No change'  , '', 'PANEL_CLOSE'              , 0),
      ('Allowed'     , 'Allowed'    , '', 'RESTRICT_SELECT_OFF'      , 1),
      ('Disabled'    , 'Disabled'   , '', 'RESTRICT_SELECT_ON'       , 2)
    ]
  )
  set_render = bpy.props.EnumProperty(
    name = 'Render visibility',
    description = 'Choose whether objects should show in render.',
    items = [
      ('No change' , 'No change'    , '', 'PANEL_CLOSE'              , 0),
      ('Visible'   , 'Visible'      , '', 'RESTRICT_RENDER_OFF'      , 1),
      ('Hidden'    , 'Hidden'       , '', 'RESTRICT_RENDER_ON'       , 2)
    ]
  )


  def execute(self, context):

    def unlock_object(obj):#, set_viewport, set_select, set_render):
      
      if self.set_viewport != 'No change':
        if self.set_viewport == 'Visible':
          obj.hide = False
        elif self.set_viewport == 'Hidden':
          obj.hide = True

      if self.set_select != 'No change':
        if self.set_select == 'Allowed':
          obj.hide_select = False
        elif self.set_select == 'Disabled':
          obj.hide_select = True
      
      if self.set_render != 'No change':
        if self.set_render == 'Visible':
          obj.hide_render = False
        elif self.set_render == 'Hidden':
          obj.hide_render = True

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    
    if self.set_targets == 'All':
      for obj in bpy.data.objects:
        unlock_object(obj)

    elif self.set_targets == 'Scene':
      for obj in bpy.context.scene.objects:
        unlock_object(obj)
    
    elif self.set_targets == 'Selected':
      for obj in bpy.context.selected_objects:
        unlock_object(obj)

      

    return {'FINISHED'}