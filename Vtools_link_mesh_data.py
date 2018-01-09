import bpy

class link_mesh_data(bpy.types.Operator):
  '''Link mesh data of objects with identical geometry.'''
  bl_idname = 'object.link_mesh_data'
  bl_label = 'Link Mesh Data'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    print("-"*79)
    print("Starting...")


    # take object
    #   - read it's polygons and save them to a dictionary
    #     - object name
    #       - mesh data name
    #          - polygon ID
    #             - polygon X location
    #             - polygon Y location
    #             - polygon Z location

    # take object
    #   - compare it's polygon data to the previous objects in dictionary
    #     - if the same, link to that object
    #     - if not the same, create new dictionary item


    class object_data:
      def __init__(self, obj):
        self.name = obj.name
        self.mesh_name = obj.data.name
        self.vertices = obj.data.vertices
      def __repr__(self):
        return 'Object name: ' + self.name + ' Mesh name: ' + self.mesh_name

    # put first object to the list
    i = 0
    for obj in bpy.data.objects:
      if obj.type == 'MESH':
        print(obj.name)
        break
      i+=1
      print(i)
    objects = [object_data(bpy.data.objects[i])]
    print('First object is: ', objects)

    # go through all objects, skipping the first one
    for obj in bpy.data.objects[1:]:
      if obj.type == 'MESH':

        # construct vertex data tuple for iterated object
        obj_vertex_data_x = []
        obj_vertex_data_y = []
        obj_vertex_data_z = []
        for vertex in obj.data.vertices:
          obj_vertex_data_x.append(vertex.co[0])
          obj_vertex_data_y.append(vertex.co[1])
          obj_vertex_data_z.append(vertex.co[2])
        obj_vertex_data = (obj_vertex_data_x, obj_vertex_data_y, obj_vertex_data_z)

        # go through all objects in the list
        for object_class in objects:
          print('------')
          print('Trying objects ', object_class.name, ' vs ', obj.name)
          

          # construct vertex data tuple for object_class object
          list_x = []
          list_y = []
          list_z = []      
          for vertex in object_class.vertices:
            list_x.append(vertex.co[0])
            list_y.append(vertex.co[1])
            list_z.append(vertex.co[2])
          object_class_vertex_data = (list_x, list_y, list_z)
          
          #for (u,v) in zip(obj_vertex_data,object_class_vertex_data):
          #  print(u, v)

          # if data is the same, link the mesh data and stop iterating for this object
          if obj_vertex_data == object_class_vertex_data:
            print('Vertices same between', obj.name, 'and', object_class.name)
            print('Target mesh name then is ... ', object_class.mesh_name)
            obj.data = bpy.data.meshes[object_class.mesh_name]
            match_found = 1
            break
          # if no match has been found, append object to the list after all iterations
          else:
            match_found = 0
        if match_found == 0:
          objects.append(object_data(obj))

    for o in objects:
      print(o)
    
    return {'FINISHED'}