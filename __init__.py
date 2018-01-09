bl_info = {
    'name': 'V-Tools',
    'author': 'V453000',
    'description': 'Various tools.',
    'category': 'User',
    'version': (0, 1, 0),
    'blender': (2, 7, 9)
}

import bpy
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
link_material_to =           Vtools_link_material_to.link_material_to



# --------------------------------------------------------
#          B U T T O N S
# --------------------------------------------------------

class tool_panel_blend(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-Tools'
  bl_label = 'V-Tools - Blend file'
  bl_idname = 'tool_panel_blend'

  def draw(self,context):
    layout = self.layout
    layout.operator('blend.save_backup'             , text = 'Save Backup'            , icon = 'SAVE_COPY'          )
    layout.operator('scene.unpack_images'           , text = 'Unpack Images'          , icon = 'IMAGE_COL'          )


class tool_panel_scene(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-Tools'
  bl_label = 'V-Tools - Scene'
  bl_idname = 'tool_panel_scene'

  def draw(self,context):
    layout = self.layout
    layout.operator('render.default_render_settings', text = 'Default Render Settings', icon = 'RESTRICT_RENDER_OFF')
    layout.operator('nodes.generate_render_nodes'   , text = 'Generate Render Nodes'  , icon = 'NODETREE'           )

class tool_panel_object(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = 'V-Tools'
  bl_label = 'V-Tools - Object'
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
  bl_category = 'V-Tools-render'
  bl_label = 'V-Tools-render'
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
  bl_category = 'V-Tools-render-layers'
  bl_label = 'V-Tools-render-layers'
  bl_idname = 'render_layer_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('nodes.generate_render_nodes'   , text = 'Generate Render Nodes'  , icon = 'NODETREE'           )  

class material_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'material'
  bl_category = 'V-Tools-material'
  bl_label = 'V-Tools-material'
  bl_idname = 'material_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('object.clean_material_slots', text = 'Clean Material Slots'   , icon = 'MATERIAL' )
    layout.operator('object.link_material_to'       , text = 'Material Mode'          , icon = 'LINKED'   )




class object_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'object'
  bl_category = 'V-Tools-object'
  bl_label = 'V-Tools-object'
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
  bl_category = 'V-Tools-modifier'
  bl_label = 'V-Tools-modifier'
  bl_idname = 'modifier_panel_layout'

  def draw(self,context):
    layout = self.layout
    row = layout.row()
    row.operator('object.subsurf_settings',       text = 'Subsurf Settings',       icon = 'MOD_SUBSURF'  )

class data_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'data'
  bl_category = 'V-Tools-data'
  bl_label = 'V-Tools-data'
  bl_idname = 'data_panel_layout'

  def draw(self,context):
    layout = self.layout
    layout.operator('object.link_mesh_data'      , text = 'Link Identical Mesh Data'         , icon = 'MOD_TRIANGULATE'    )



def register():
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
  
  # Buttons
  bpy.utils.register_class(tool_panel_blend)
  bpy.utils.register_class(tool_panel_scene)
  bpy.utils.register_class(tool_panel_object)
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
  
  # Buttons
  bpy.utils.unregister_class(tool_panel_blend)
  bpy.utils.unregister_class(tool_panel_scene)
  bpy.utils.unregister_class(tool_panel_object)
  bpy.utils.unregister_class(render_panel)
  bpy.utils.unregister_class(render_layer_panel)
  bpy.utils.unregister_class(object_panel)
  bpy.utils.unregister_class(material_panel)
  bpy.utils.unregister_class(modifier_panel)
  bpy.utils.unregister_class(data_panel)


if __name__ == '__main__':
  register()