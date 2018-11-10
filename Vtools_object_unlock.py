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
      ('Scene'   , 'Current Scene' , ''),
      ('All'     , 'All scenes'    , ''),
      ('Selected', 'Selected'      , '')
    ]
  )
  set_viewport = bpy.props.EnumProperty(
    name = 'Viewport visibility',
    description = 'Choose whether objects should show in viewport.',
    items = [
      ('No change' , 'No change'    , ''),
      ('Visible'   , 'Visible'      , ''),
      ('Hidden'    , 'Hidden'       , '')
    ]
  )
  set_select = bpy.props.EnumProperty(
    name = 'Selecting',
    description = 'Choose whether objects should be selectible.',
    items = [
      ('No change'   , 'No change'    , ''),
      ('Allowed'     , 'Allowed'      , ''),
      ('Disabled'    , 'Disabled'     , '')
    ]
  )
  set_render = bpy.props.EnumProperty(
    name = 'Render visibility',
    description = 'Choose whether objects should show in render.',
    items = [
      ('No change' , 'No change'    , ''),
      ('Visible'   , 'Visible'      , ''),
      ('Hidden'    , 'Hidden'       , '')
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