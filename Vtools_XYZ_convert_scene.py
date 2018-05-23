import bpy

class XYZ_convert_scene(bpy.types.Operator):
  '''Convert all scenes to special map rendering.'''
  bl_idname = 'scene.xyz_convert_scene'
  bl_label = 'XYZ Convert scene'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
    def xyz_render_settings():
      bpy.context.scene.render.engine = 'CYCLES'
      #bpy.context.scene.render.engine = 'BLENDER_RENDER'
      bpy.context.scene.view_settings.view_transform = 'Raw'

      bpy.context.scene.render.image_settings.compression = 0

      bpy.context.scene.cycles.samples = 1
      bpy.context.scene.cycles.max_bounces = 0
      bpy.context.scene.cycles.min_bounces = 0
      bpy.context.scene.cycles.diffuse_bounces = 0
      bpy.context.scene.cycles.glossy_bounces = 0
      bpy.context.scene.cycles.transmission_bounces = 0
      bpy.context.scene.cycles.volume_bounces = 0

      bpy.context.scene.cycles.use_transparent_shadows = False
      bpy.context.scene.cycles.caustics_reflective = False
      bpy.context.scene.cycles.caustics_refractive = False

      bpy.context.scene.cycles.pixel_filter_type = 'GAUSSIAN'
      bpy.context.scene.cycles.filter_width = 1.5

    
    def remove_lights():
      #remove all lamps
      for obj in bpy.data.objects:
        if obj.type == 'LAMP':
          bpy.data.objects.remove(obj)

    def clean_renderlayers():
      for renderlayer in bpy.context.scene.render.layers:
        remove_layer = False
        shadow_appendix = 'shadow'
        height_appendix = 'height'
        shadow_appendix_count = len(shadow_appendix)
        height_appendix_count = len(height_appendix)

        print(renderlayer.name[:shadow_appendix_count])
        # see if the layer needs to be removed
        if renderlayer.name[-shadow_appendix_count:].lower() == shadow_appendix.lower():
          if renderlayer.use_pass_shadow == True:
            remove_layer = True
        elif renderlayer.name[-height_appendix_count:].lower() == height_appendix.lower():
          if renderlayer.material_override is not None:
            remove_layer = True
        if renderlayer.name[:shadow_appendix_count].lower() == shadow_appendix.lower():
          if renderlayer.use_pass_shadow == True:
            remove_layer = True
        elif renderlayer.name[:height_appendix_count].lower() == height_appendix.lower():
          if renderlayer.material_override is not None:
            remove_layer = True
            

        if remove_layer == True:  
          bpy.context.scene.render.layers.remove(renderlayer)

    def generate_xyz_material():
      if bpy.data.materials.get('XYZmap') is None:
        # create XYZmap material
        xyz_material = bpy.data.materials.new('XYZmap')
        xyz_material.use_nodes = True
      else:
        xyz_material = bpy.data.materials['XYZmap']

      xyz_tree = xyz_material.node_tree
      xyz_nodes = xyz_tree.nodes
      xyz_links = xyz_tree.links
      # clean all nodes
      for node in xyz_nodes:
        xyz_nodes.remove(node)
      
      # add nodes
      loc_x = 0
      loc_y = 0

      xyz_geometry_node = xyz_nodes.new('ShaderNodeNewGeometry')
      xyz_geometry_node.location = (loc_x, loc_y)
      loc_x = loc_x + 200
      xyz_mapping_node = xyz_nodes.new('ShaderNodeMapping')
      xyz_mapping_node.vector_type = 'TEXTURE'
      xyz_mapping_node.translation[0] = -15
      xyz_mapping_node.translation[1] = -15
      xyz_mapping_node.translation[2] = -2
      xyz_mapping_node.rotation[0] = 0
      xyz_mapping_node.rotation[1] = 0
      xyz_mapping_node.rotation[2] = 0
      xyz_mapping_node.scale[0] = 40
      xyz_mapping_node.scale[1] = 40
      xyz_mapping_node.scale[2] = 40
      xyz_mapping_node.location = (loc_x, loc_y)
      loc_x = loc_x + 400

      xyz_emission_node = xyz_nodes.new('ShaderNodeEmission')
      xyz_emission_node.location = (loc_x, loc_y)
      loc_x = loc_x + 200

      xyz_output_node = xyz_nodes.new('ShaderNodeOutputMaterial')
      xyz_output_node.location = (loc_x, loc_y)

      # add links
      xyz_links.new(xyz_geometry_node.outputs['Position'], xyz_mapping_node.inputs[0])
      xyz_links.new(xyz_mapping_node.outputs[0], xyz_emission_node.inputs[0])
      xyz_links.new(xyz_emission_node.outputs[0], xyz_output_node.inputs[0])
    
    def replace_materials(obj, material_name):
      # assign material to objects if it's a mesh
      DestinationMaterial = bpy.data.materials.get(material_name)
      if obj.type == 'MESH':
        meshName = obj.name
        if obj.data.materials:
          slotCount = len(obj.material_slots)
          slotNumber = 0
          #print(meshName, 'slotCount is',s
          # lotCount)
          for slotNumber in range(0, slotCount):
            obj.material_slots[slotNumber].material = DestinationMaterial
            #print('Adding material to',meshName, 'slot number', slotNumber)   
          
        else:
          obj.data.materials.append(DestinationMaterial)
          #print('No slots found on ',meshName, '. Applying material to object.', meshName)

    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                        E X E C U T E   T O O L
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    xyz_render_settings()
    remove_lights()
    clean_renderlayers()
    generate_xyz_material()
    for obj in bpy.data.objects:
      replace_materials(obj, 'XYZmap')

    return {'FINISHED'}