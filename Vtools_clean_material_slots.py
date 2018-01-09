import bpy

class clean_material_slots(bpy.types.Operator):
  '''Remove material slots which are not assigned to any polygon.'''
  bl_idname = 'object.clean_material_slots'
  bl_label = 'Clean Material Slots'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    import bmesh

    print('-'*36)
    print('Starting...')

    object_list = []

    print('Creating object list')
    # create list of objects
    for obj in bpy.context.scene.objects:
      if obj.type == 'MESH':
        object_list.append(obj.name)
    print(object_list)



    for obj_name in object_list:
      print('Creating material list for ', obj_name)
      # save material names to a list
      obj = bpy.context.scene.objects[obj_name]
      material_list = []
      for mtl in obj.material_slots:
        material_list.append(mtl.name)
      
      print(material_list)
      print(len(material_list))

      # go through polygons of the object
      print('Filtering polygons for ', obj_name)

      mesh = obj.data
      if len(material_list) > 0:
        for poly in mesh.polygons:
          material_list[poly.material_index] = 'used'

      print(obj.name)
      print(material_list)


      # go through material slots and material list and remove unused slots
      material_slot_count = len(obj.material_slots)
      print(material_slot_count)
      
      mtl_index = material_slot_count - 1

      if len(material_list) > 0:
        for mtl_name in reversed(material_list):
          print(mtl_index, mtl_name)
          if mtl_name is not 'used':
            bpy.context.scene.objects.active = obj
            print('Removing ', mtl_index, ' ', mtl_name, ' from ', obj.name)
            obj.active_material_index = mtl_index
            bpy.ops.object.material_slot_remove()
          mtl_index -= 1
    return {'FINISHED'}
      
