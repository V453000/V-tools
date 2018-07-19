bl_info = {
    'name': 'V-tools',
    'author': 'V453000',
    'description': 'Various tools.',
    'category': 'User',
    'version': (0, 2, 5),
    'blender': (2, 7, 9)
}

import bpy

from . import addon_updater_ops

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

# To support reload properly, try to access a package var, if it's there, reload everything
if "bpy" in locals():
  import importlib
  if "config" in locals():
    importlib.reload(Vtools_object_draw_type)
    importlib.reload(Vtools_default_render_settings)
    importlib.reload(Vtools_generate_render_nodes)
    importlib.reload(Vtools_link_mesh_data)
    importlib.reload(Vtools_clean_material_slots)
    importlib.reload(Vtools_unpack_images)
    importlib.reload(Vtools_object_cycles_settings)
    importlib.reload(Vtools_object_lock_transforms)
    importlib.reload(Vtools_subsurf_settings)
    importlib.reload(Vtools_link_to_all_scenes)
    importlib.reload(Vtools_delete_from_all_scenes)
    importlib.reload(Vtools_save_backup)
    importlib.reload(Vtools_layered_transfer_copy)
    importlib.reload(Vtools_layered_transfer_paste)
    importlib.reload(Vtools_link_material_to)
    importlib.reload(Vtools_duplicate_render_layer)

    importlib.reload(Vtools_material_replace)

    importlib.reload(Vtools_WTF_generate_material_XYZ)
    importlib.reload(Vtools_WTF_generate_material_NRM)
    importlib.reload(Vtools_WTF_scene_settings_shared)
    importlib.reload(Vtools_WTF_scene_settings_XYZ)
    importlib.reload(Vtools_WTF_scene_settings_NRM)
    importlib.reload(Vtools_WTF_render_XYZ)

    importlib.reload(Vtools_XYZ_convert_scene)


  from . import Vtools_object_draw_type
  from . import Vtools_default_render_settings
  from . import Vtools_generate_render_nodes
  from . import Vtools_link_mesh_data
  from . import Vtools_clean_material_slots
  from . import Vtools_unpack_images
  from . import Vtools_object_cycles_settings
  from . import Vtools_object_lock_transforms
  from . import Vtools_subsurf_settings
  from . import Vtools_link_to_all_scenes
  from . import Vtools_delete_from_all_scenes
  from . import Vtools_save_backup
  from . import Vtools_layered_transfer_copy
  from . import Vtools_layered_transfer_paste
  from . import Vtools_link_material_to
  from . import Vtools_duplicate_render_layer

  from . import Vtools_material_replace

  from . import Vtools_WTF_generate_material_XYZ
  from . import Vtools_WTF_generate_material_NRM
  from . import Vtools_WTF_scene_settings_shared
  from . import Vtools_WTF_scene_settings_XYZ
  from . import Vtools_WTF_scene_settings_NRM
  from . import Vtools_WTF_render_XYZ

  from . import Vtools_XYZ_convert_scene


object_draw_mode =        Vtools_object_draw_type.object_draw_mode
default_render_settings = Vtools_default_render_settings.default_render_settings
generate_render_nodes =   Vtools_generate_render_nodes.generate_render_nodes
link_mesh_data =          Vtools_link_mesh_data.link_mesh_data
clean_material_slots =    Vtools_clean_material_slots.clean_material_slots
unpack_images =           Vtools_unpack_images.unpack_images
object_cycles_settings =  Vtools_object_cycles_settings.object_cycles_settings
object_lock_transforms =  Vtools_object_lock_transforms.object_lock_transforms
subsurf_settings =        Vtools_subsurf_settings.subsurf_settings
link_to_all_scenes =      Vtools_link_to_all_scenes.link_to_all_scenes
delete_from_all_scenes =  Vtools_delete_from_all_scenes.delete_from_all_scenes
save_backup =             Vtools_save_backup.save_backup
layered_transfer_copy =   Vtools_layered_transfer_copy.layered_transfer_copy
layered_transfer_paste =  Vtools_layered_transfer_paste.layered_transfer_paste
link_material_to =        Vtools_link_material_to.link_material_to
duplicate_render_layer =  Vtools_duplicate_render_layer.duplicate_render_layer

material_replace =        Vtools_material_replace.material_replace
material_replace_panel =  Vtools_material_replace.material_replace_panel

WTF_generate_material_XYZ    =   Vtools_WTF_generate_material_XYZ.WTF_generate_material_XYZ
WTF_generate_material_NRM    =   Vtools_WTF_generate_material_NRM.WTF_generate_material_NRM
WTF_scene_settings_shared =   Vtools_WTF_scene_settings_shared.WTF_scene_settings_shared
WTF_scene_settings_XYZ    =   Vtools_WTF_scene_settings_XYZ.WTF_scene_settings_XYZ
WTF_scene_settings_NRM    =   Vtools_WTF_scene_settings_NRM.WTF_scene_settings_NRM
WTF_render_XYZ =              Vtools_WTF_render_XYZ.WTF_render_XYZ

XYZ_convert_scene =       Vtools_XYZ_convert_scene.XYZ_convert_scene




# --------------------------------------------------------
#          B U T T O N S
# --------------------------------------------------------

class tool_panel_blend(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-tools'
  bl_label = 'V-tools - Blend file'
  bl_idname = 'tool_panel_blend'

  def draw(self,context):
    layout = self.layout
    layout.operator('blend.save_backup'             , text = 'Save Backup'            , icon = 'SAVE_COPY'          )
    layout.operator('scene.unpack_images'           , text = 'Unpack Images'          , icon = 'IMAGE_COL'          )

class tool_panel_scene(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-tools'
  bl_label = 'V-tools - Scene'
  bl_idname = 'tool_panel_scene'

  def draw(self,context):
    layout = self.layout
    layout.operator('render.default_render_settings', text = 'Default Render Settings', icon = 'RESTRICT_RENDER_OFF')
    layout.operator('nodes.generate_render_nodes'   , text = 'Generate Render Nodes'  , icon = 'NODETREE'           )
    layout.operator('scene.duplicate_render_layer'  , text = 'Duplicate RenderLayer'  , icon = 'RENDERLAYERS'       )

class tool_panel_object(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-tools'
  bl_label = 'V-tools - Object'
  bl_idname = 'tool_panel_object'

  def draw(self,context):
    layout = self.layout
    layout.operator('object.draw_mode'              , text = 'Draw mode'               , icon = 'WIRE'               )
    layout.operator('object.object_cycles_settings' , text = 'Cycles Settings'         , icon = 'RESTRICT_RENDER_ON' )
    layout.operator('object.object_lock_transforms' , text = 'Lock Transforms'         , icon = 'LOCKED'             )
    layout.operator('object.subsurf_settings'       , text = 'Subsurf Settings'        , icon = 'MOD_SUBSURF'        )
    layout.operator('object.clean_material_slots'   , text = 'Clean Material Slots'    , icon = 'MATERIAL'           )
    layout.operator('object.link_to_all_scenes'     , text = 'Link to All Scenes'      , icon = 'LINK_AREA'          )
    layout.operator('object.delete_from_all_scenes' , text = 'Delete From All Scenes'  , icon = 'X'                  )
    layout.operator('object.link_mesh_data'         , text = 'Link Identical Mesh Data', icon = 'MOD_TRIANGULATE'    )
    layout.operator('object.link_material_to'       , text = 'Link Material to...'     , icon = 'LINKED'             )
    row = layout.row()
    row.operator('object.layered_transfer_copy'     , text = 'Layered Transfer COPY'   , icon = 'COPYDOWN'           )
    row.operator('object.layered_transfer_paste'    , text = 'Layered Transfer PASTE'  , icon = 'PASTEDOWN'          )


class tool_panel_XYZ(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-tools'
  bl_label = 'V-tools - XYZ'
  bl_idname = 'tool_panel_XYZ'
  def draw(self,context):
    layout = self.layout
    #row = layout.row()
    #row.operator('scene.wtf_scene_settings_shared'    , text = 'Shared settings'    , icon = 'SCENE_DATA'   )
    #row = layout.row()
    #row.operator('scene.wtf_generate_material_xyz'    , text = 'Mtl'    , icon = 'RADIO'              )
    #row.operator('scene.wtf_generate_material_nrm'    , text = 'Mtl'    , icon = 'MATCAP_23'          )
    row2 = layout.row()
    row2.operator('scene.wtf_scene_settings_xyz'       , text = 'Set XYZ'    , icon = 'RADIO'              )
    row2.operator('scene.wtf_scene_settings_nrm'       , text = 'Set NRM'    , icon = 'MATCAP_23'          )
    row3 = layout.row()
    row3.operator('scene.wtf_render_xyz'               , text = 'XYZ Render'      , icon = 'RADIO'              )



class tool_panel_updater(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-tools'
  bl_label = 'V-tools - Update'
  bl_idname = 'tool_panel_update'

  def draw(self,context):
    layout = self.layout
    addon_updater_ops.check_for_update_background()
    if addon_updater_ops.updater.update_ready == True:
      layout.label('A new version of V-Tools is available!', icon ='RADIO')
    addon_updater_ops.update_notice_box_ui(self, context)



# PROPERTIES PANELS
# Render
# Render Layers
# Scene
# World
# Object
# Constraints
# Modifiers
# Data
# Material
# Texture
# Particles
# Physics

class render_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'render'
  bl_category = 'V-tools-render'
  bl_label = 'V-tools-render'
  bl_idname = 'render_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('render.default_render_settings', text = 'Default Render Settings', icon = 'RESTRICT_RENDER_OFF')
    layout.operator('scene.unpack_images'           , text = 'Unpack Images'          , icon = 'IMAGE_COL'          )
    layout.operator('blend.save_backup'             , text = 'Save Backup'            , icon = 'SAVE_COPY'          )

class render_layer_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'render_layer'
  bl_category = 'V-tools-render-layers'
  bl_label = 'V-tools-render-layers'
  bl_idname = 'render_layer_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('nodes.generate_render_nodes'   , text = 'Generate Render Nodes'  , icon = 'NODETREE'           )

class material_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'material'
  bl_category = 'V-tools-material'
  bl_label = 'V-tools-material'
  bl_idname = 'material_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('object.clean_material_slots', text = 'Clean Material Slots'   , icon = 'MATERIAL' )
    layout.operator('object.link_material_to'       , text = 'Material Mode'          , icon = 'LINKED'   )




class object_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'object'
  bl_category = 'V-tools-object'
  bl_label = 'V-tools-object'
  bl_idname = 'object_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('object.draw_mode'             , text = 'Object Draw Mode'         , icon = 'WIRE'                )
    layout.operator('object.object_cycles_settings', text = 'Object Cycles Settings'   , icon = 'RESTRICT_RENDER_ON'  )
    layout.operator('object.object_lock_transforms', text = 'Object Lock Transforms'   , icon = 'LOCKED'              )
    layout.operator('object.subsurf_settings'      , text = 'Subsurf Settings'         , icon = 'MOD_SUBSURF'         )
    layout.operator('object.link_to_all_scenes'    , text = 'Link to All Scenes'       , icon = 'LINK_AREA'           )
    layout.operator('object.delete_from_all_scenes', text = 'Delete From All Scenes'   , icon = 'X'                   )
    layout.operator('object.link_mesh_data'        , text = 'Link Identical Mesh Data' , icon = 'MOD_TRIANGULATE'     )
    row = layout.row()
    row.operator('object.layered_transfer_copy'     , text = 'Layered Transfer COPY'   , icon = 'COPYDOWN'           )
    row.operator('object.layered_transfer_paste'    , text = 'Layered Transfer PASTE'  , icon = 'PASTEDOWN'          )

class modifier_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'modifier'
  bl_category = 'V-tools-modifier'
  bl_label = 'V-tools-modifier'
  bl_idname = 'modifier_panel_layout'

  def draw(self,context):
    layout = self.layout
    row = layout.row()
    row.operator('object.subsurf_settings',       text = 'Subsurf Settings',       icon = 'MOD_SUBSURF'  )

class data_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'data'
  bl_category = 'V-tools-data'
  bl_label = 'V-tools-data'
  bl_idname = 'data_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('object.link_mesh_data'      , text = 'Link Identical Mesh Data'         , icon = 'MOD_TRIANGULATE'    )

class VTools_preferences(bpy.types.AddonPreferences):
  bl_idname = __package__

  # addon updater preferences from `__init__`, be sure to copy all of them
  auto_check_update = bpy.props.BoolProperty(
    name = "Auto-check for Update",
    description = "If enabled, auto-check for updates using an interval",
    default = False,
  )
  updater_intrval_months = bpy.props.IntProperty(
    name='Months',
    description = "Number of months between checking for updates",
    default=0,
    min=0
  )
  updater_intrval_days = bpy.props.IntProperty(
    name='Days',
    description = "Number of days between checking for updates",
    default=7,
    min=0,
  )
  updater_intrval_hours = bpy.props.IntProperty(
    name='Hours',
    description = "Number of hours between checking for updates",
    default=0,
    min=0,
    max=23
  )
  updater_intrval_minutes = bpy.props.IntProperty(
    name='Minutes',
    description = "Number of minutes between checking for updates",
    default=0,
    min=0,
    max=59
  )

  def draw(self, context):
    layout = self.layout
    addon_updater_ops.update_settings_ui(self, context)

def register():

  # Auto updater
  addon_updater_ops.register(bl_info)
  bpy.utils.register_class(VTools_preferences)

  # Operators
  bpy.utils.register_class(object_draw_mode)
  bpy.utils.register_class(generate_render_nodes)
  bpy.utils.register_class(default_render_settings)
  bpy.utils.register_class(link_mesh_data)
  bpy.utils.register_class(clean_material_slots)
  bpy.utils.register_class(unpack_images)
  bpy.utils.register_class(object_cycles_settings)
  bpy.utils.register_class(object_lock_transforms)
  bpy.utils.register_class(subsurf_settings)
  bpy.utils.register_class(link_to_all_scenes)
  bpy.utils.register_class(delete_from_all_scenes)
  bpy.utils.register_class(save_backup)
  bpy.utils.register_class(layered_transfer_copy)
  bpy.utils.register_class(layered_transfer_paste)
  bpy.utils.register_class(link_material_to)
  bpy.utils.register_class(duplicate_render_layer)

  bpy.utils.register_class(WTF_generate_material_XYZ   )
  bpy.utils.register_class(WTF_generate_material_NRM   )
  bpy.utils.register_class(WTF_scene_settings_shared   )
  bpy.utils.register_class(WTF_scene_settings_XYZ      )
  bpy.utils.register_class(WTF_scene_settings_NRM      )
  bpy.utils.register_class(WTF_render_XYZ              )

  bpy.utils.register_class(XYZ_convert_scene)

  # Buttons
  bpy.utils.register_class(tool_panel_blend)
  bpy.utils.register_class(tool_panel_scene)
  bpy.utils.register_class(tool_panel_object)

  Vtools_material_replace.register()
  bpy.utils.register_class(tool_panel_XYZ)


  #bpy.utils.register_class(material_replace)
  #bpy.utils.register_class(material_replace_panel)

  bpy.utils.register_class(tool_panel_updater)
  bpy.utils.register_class(render_panel)
  bpy.utils.register_class(render_layer_panel)
  bpy.utils.register_class(object_panel)
  bpy.utils.register_class(material_panel)
  bpy.utils.register_class(modifier_panel)
  bpy.utils.register_class(data_panel)



def unregister():

  # Operators
  bpy.utils.unregister_class(object_draw_mode)
  bpy.utils.unregister_class(generate_render_nodes)
  bpy.utils.unregister_class(default_render_settings)
  bpy.utils.unregister_class(link_mesh_data)
  bpy.utils.unregister_class(clean_material_slots)
  bpy.utils.unregister_class(unpack_images)
  bpy.utils.unregister_class(object_cycles_settings)
  bpy.utils.unregister_class(object_lock_transforms)
  bpy.utils.unregister_class(subsurf_settings)
  bpy.utils.unregister_class(link_to_all_scenes)
  bpy.utils.unregister_class(delete_from_all_scenes)
  bpy.utils.unregister_class(save_backup)
  bpy.utils.unregister_class(layered_transfer_copy)
  bpy.utils.unregister_class(layered_transfer_paste)
  bpy.utils.unregister_class(link_material_to)
  bpy.utils.unregister_class(duplicate_render_layer)

  bpy.utils.unregister_class(WTF_generate_material_XYZ   )
  bpy.utils.unregister_class(WTF_generate_material_NRM   )
  bpy.utils.unregister_class(WTF_scene_settings_shared   )
  bpy.utils.unregister_class(WTF_scene_settings_XYZ      )
  bpy.utils.unregister_class(WTF_scene_settings_NRM      )
  bpy.utils.unregister_class(WTF_render_XYZ              )

  bpy.utils.unregister_class(XYZ_convert_scene)

  Vtools_material_replace.unregister()


  # Buttons
  bpy.utils.unregister_class(tool_panel_blend)
  bpy.utils.unregister_class(tool_panel_scene)
  bpy.utils.unregister_class(tool_panel_object)
  bpy.utils.unregister_class(tool_panel_XYZ)
  bpy.utils.unregister_class(tool_panel_updater)
  bpy.utils.unregister_class(render_panel)
  bpy.utils.unregister_class(render_layer_panel)
  bpy.utils.unregister_class(object_panel)
  bpy.utils.unregister_class(material_panel)
  bpy.utils.unregister_class(modifier_panel)
  bpy.utils.unregister_class(data_panel)


if __name__ == '__main__':
  register()
