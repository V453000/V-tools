import bpy
from bpy.app.handlers import persistent

class material_replace(bpy.types.Operator):
  '''Replaces all materials on all objects with selected material.'''
  bl_idname = 'object.material_replace'
  bl_label = 'Material replace'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
    def replace_materials(obj_name, material_name):
      obj = bpy.data.objects[obj_name]
      # assign material to objects if it's a mesh
      DestinationMaterial = bpy.data.materials.get(material_name)
      if obj.type == 'MESH':
        if obj.data.materials:
          slotCount = len(obj.material_slots)
          slotNumber = 0

          for slotNumber in range(0, slotCount):
            obj.material_slots[slotNumber].material = DestinationMaterial
          
        else:
          obj.data.materials.append(DestinationMaterial)

    #replace_materials(self.set_object, self.set_material)

    return {'FINISHED'}


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

class material_replace_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'V-tools'
    bl_label = 'V-Tools- Mat Replace'
    bl_idname = 'tool_panel_material_replace'
    

    def draw(self, context):
        layout = self.layout
        layout.prop_search(context.scene, "Obj_for_mat_replace", context.scene, "Obj_list_for_mat_replace", icon='OBJECT_DATA')
        layout.prop_search(context.scene, "Mtl_for_mat_replace", context.scene, "Mtl_list_for_mat_replace", icon='MATERIAL')
        row = layout.row()
        row.operator('object.material_replace'            , text = 'Replace Materials', icon = 'COLOR')

@persistent
def populate_obj_list(scene):
    #bpy.app.handlers.scene_update_pre.remove(populate_coll)
    scene.Obj_list_for_mat_replace.clear()
    for obj in bpy.data.objects:
        scene.Obj_list_for_mat_replace.add().name = obj.name

@persistent
def populate_mtl_list(scene):
    #bpy.app.handlers.scene_update_pre.remove(populate_coll)
    scene.Mtl_list_for_mat_replace.clear()
    for material in bpy.data.materials:
        scene.Mtl_list_for_mat_replace.add().name = material.name

def register():
    bpy.utils.register_class(material_replace)
    bpy.utils.register_class(material_replace_panel)

    bpy.types.Scene.Obj_list_for_mat_replace = bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup
    )
    bpy.types.Scene.Mtl_list_for_mat_replace = bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup
    )

    bpy.types.Scene.Obj_for_mat_replace = bpy.props.StringProperty()
    bpy.types.Scene.Mtl_for_mat_replace = bpy.props.StringProperty()

    # Hack for testing
    bpy.app.handlers.scene_update_pre.append(populate_obj_list)
    bpy.app.handlers.scene_update_pre.append(populate_mtl_list)

def unregister():
    bpy.utils.unregister_class(material_replace)
    bpy.utils.unregister_class(material_replace_panel)
    del bpy.types.Scene.Obj_list_for_mat_replace
    del bpy.types.Scene.Obj_for_mat_replace
    del bpy.types.Scene.Mtl_list_for_mat_replace
    del bpy.types.Scene.Mtl_for_mat_replace
