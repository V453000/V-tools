import bpy
import mathutils
import math
pi = math.pi

class WTF_generate_material_XYZ(bpy.types.Operator):
  '''Generates the XYZmap material.'''
  bl_idname = 'scene.wtf_generate_material_xyz'
  bl_label = 'Generate XYZmap'
  bl_options = {'REGISTER', 'UNDO'}

  XYZ_wtfscale = bpy.props.FloatProperty(
  name = 'Scale',
  default = 32
  )
  XYZ_groundheight = bpy.props.FloatProperty(
  name = 'Ground Height',
  default = 0
  )
  XYZ_groundheight_from_selected = bpy.props.BoolProperty(
  name = 'Active object sets Ground Height',
  default = False
  )

  def execute(self, context):

    def generate_xyz_material(XYZ_scale, XYZ_groundheight, XYZ_groundheight_from_selected):
      # check if XYZmap material exists
      if bpy.data.materials.get('XYZmap') is None:
        # create XYZmap material
        xyz_material = bpy.data.materials.new('XYZmap')
        xyz_material.use_nodes = True
      else:
        xyz_material = bpy.data.materials['XYZmap']
      
      # check if XYZmap group exists
      if bpy.data.node_groups.get('XYZgroup') is None:
        # create XYZmap group
        xyz_group = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = 'XYZgroup')
      else:
        xyz_group = bpy.data.node_groups['XYZgroup']

      # add input socket for alpha      
      if xyz_group.inputs.get('Alpha') is None:
        xyz_group.inputs.new('NodeSocketFloat', 'Alpha')

      xyz_material_nodes = xyz_material.node_tree.nodes
      xyz_material_links = xyz_material.node_tree.links
      xyz_group_nodes = xyz_group.nodes
      xyz_group_links = xyz_group.links

      # clean all nodes from both the material and the group
      for node in xyz_group_nodes:
        xyz_group_nodes.remove(node)
      for node in xyz_material_nodes:
        xyz_material_nodes.remove(node)

      # adding XYZ-settings in the material group for easy access/visibility
      if bpy.data.node_groups['XYZgroup'].nodes.get('XYZ-settings') is None:
        print('---------------------------------------------XYZ group not found in material, generating...')
        xyz_setting_group_in_material = bpy.data.node_groups['XYZgroup'].nodes.new('ShaderNodeGroup')
        xyz_setting_group_in_material.node_tree = bpy.data.node_groups['XYZ-settings']
        xyz_setting_group_in_material.name = 'XYZ-settings'
        xyz_setting_group_in_material.label = 'XYZ-settings'    
      else:
        print('------------------------------------------------------XYZ group exists.')
        xyz_setting_group_in_material = bpy.data.node_groups['XYZgroup'].nodes['XYZ-settings']
      xyz_setting_group_in_material.location = (-100, 100)
      xyz_setting_group_in_material.use_custom_color = True
      xyz_setting_group_in_material.color = (1,0,1)
      xyz_setting_group_in_material.width = 300

      xyz_group_in_material = xyz_material_nodes.new('ShaderNodeGroup')
      xyz_group_in_material.node_tree = xyz_group
      xyz_group_in_material.name = 'XYZ_material_group'
      xyz_group_in_material.label = 'XYZ_material_group'

      # add nodes
      loc_x = 0
      loc_y = 0

      xyz_geometry_node = xyz_group_nodes.new('ShaderNodeNewGeometry')
      xyz_geometry_node.location = (loc_x, loc_y)
      loc_x = loc_x + 200

      # figure out the rotation of the camera to get the rotation and position of the XYZ map
      cam_z_rot = 0
      if bpy.context.scene.camera is not None:
        cam_z_rot = bpy.context.scene.camera.matrix_world.to_euler()[2] # Z rotation of the current scene's camera
      texture_z_rot = -cam_z_rot+(pi*3/2) #cam_z_rot
      texture_z_rot_simplified = texture_z_rot *2 /pi
      texture_z_rot_rounded = round(texture_z_rot_simplified, 0)
      texture_z_rot_int = (int(texture_z_rot_rounded)-3)*-1
      # figure out the camera target on the ground plane
      camera_position = bpy.context.scene.camera.matrix_world.to_translation()
      camera_position_3x3 = bpy.context.scene.camera.matrix_world.to_3x3()
      camera_rotation   = bpy.context.scene.camera.matrix_world.to_euler()
      zero_camera_vector = mathutils.Vector((0,0,1))
      camera_vector = camera_position_3x3 * zero_camera_vector
      camera_vector_1z = mathutils.Vector((camera_vector[0]/camera_vector[2],camera_vector[1]/camera_vector[2],camera_vector[2]/camera_vector[2]))
      camera_ground_target = camera_position - ( camera_vector * (camera_position[2] / camera_vector[2]))
      cam_offset = camera_ground_target
      #height_offset = bpy.context.scene.objects['HEIGHT'].location[2]

      # go through all objects and try to find XYZ-GROUND
      ground_suffix = 'XYZ-GROUND-'
      ground_suffix_length = len(ground_suffix)

      ground_object_found = False
      for ground_object in bpy.context.scene.objects:
        if ground_object.name[:ground_suffix_length] == ground_suffix:
          height_offset = ground_object.location[2]
          XYZ_groundheight = height_offset

      if ground_object_found == False:                  
        if XYZ_groundheight_from_selected == True:
          height_offset = bpy.context.scene.objects.active.location[2]
        else:
          height_offset = XYZ_groundheight

      print('Camera vector is:   ', camera_vector)
      print('Camera vector_1z is:', camera_vector_1z)
      print('Camera target is:   ', camera_ground_target)
      print('Height offset is:   ', height_offset)

      xyz_mapping_node = xyz_group_nodes.new('ShaderNodeMapping')
      xyz_mapping_node.vector_type = 'TEXTURE'


      xyz_mapping_node.rotation[0] = 0
      xyz_mapping_node.rotation[1] = 0
      #xyz_mapping_node.rotation[2] = -cam_z_rot+(pi*3/2)

      #XYZ_scale = self.XYZ_scale
      offset_vector = (1,1,1)
      if texture_z_rot_int == 0:
        offset_vector = (-1,-1,-1)
        o = offset_vector
        xyz_mapping_node.translation = (XYZ_scale*o[0] - cam_offset[0]*o[0] + camera_vector_1z[0]*height_offset,
                                        XYZ_scale*o[1] - cam_offset[1]*o[1] + camera_vector_1z[1]*height_offset,
                                        XYZ_scale*o[2] - cam_offset[2]*o[2] + height_offset)
        xyz_mapping_node.rotation[2] = 0
        print('0')

      if texture_z_rot_int == 1:
        offset_vector = ( 1,-1,-1)
        o = offset_vector
        xyz_mapping_node.translation = (XYZ_scale*o[0] + cam_offset[0]*o[0] + camera_vector_1z[0]*height_offset,
                                        XYZ_scale*o[1] - cam_offset[1]*o[1] + camera_vector_1z[1]*height_offset,
                                        XYZ_scale*o[2] - cam_offset[2]*o[2] + height_offset)
        xyz_mapping_node.rotation[2] = pi/2
        print('1')

      if texture_z_rot_int == 2 or texture_z_rot_int == -2:
        offset_vector = ( 1, 1,-1)
        o = offset_vector
        xyz_mapping_node.translation = (XYZ_scale*o[0] + cam_offset[0]*o[0] + camera_vector_1z[0]*height_offset,
                                        XYZ_scale*o[1] + cam_offset[1]*o[1] + camera_vector_1z[1]*height_offset,
                                        XYZ_scale*o[2] - cam_offset[2]*o[2] + height_offset)
        xyz_mapping_node.rotation[2] = pi
        print('2 / -2')

      if texture_z_rot_int == -1:
        offset_vector = (-1, 1,-1)
        o = offset_vector
        xyz_mapping_node.translation = (XYZ_scale*o[0] - cam_offset[0]*o[0] + camera_vector_1z[0]*height_offset,
                                        XYZ_scale*o[1] + cam_offset[1]*o[1] + camera_vector_1z[1]*height_offset,
                                        XYZ_scale*o[2] - cam_offset[2]*o[2] + height_offset)
        xyz_mapping_node.rotation[2] = -pi/2
        print('-1')

      xyz_mapping_node.scale[0] = XYZ_scale*2
      xyz_mapping_node.scale[1] = XYZ_scale*2
      xyz_mapping_node.scale[2] = XYZ_scale*2
      xyz_mapping_node.location = (loc_x, loc_y)
      loc_x = loc_x + 400

      xyz_emission_node = xyz_group_nodes.new('ShaderNodeEmission')
      xyz_emission_node.location = (loc_x, loc_y)
      loc_y = loc_y + 200
      
      # TRANSPARENCY STUFF
      xyz_group_input_node = xyz_group_nodes.new('NodeGroupInput')
      xyz_group_input_node.location = (loc_x, loc_y)
      loc_x = loc_x + 200
      
      xyz_greater_than_node = xyz_group_nodes.new('ShaderNodeMath')
      xyz_greater_than_node.operation = 'GREATER_THAN'
      xyz_greater_than_node.location = (loc_x, loc_y)
      loc_y = loc_y - 400
      
      xyz_transparent_node = xyz_group_nodes.new('ShaderNodeBsdfTransparent')
      xyz_transparent_node.location = (loc_x, loc_y)
      loc_x = loc_x + 200
      loc_y = loc_y + 200

      xyz_mix_transparency_node = xyz_group_nodes.new('ShaderNodeMixShader')
      xyz_mix_transparency_node.location = (loc_x, loc_y)
      loc_x = loc_x + 200
      # END OF TRANSPARENCY STUFF

      xyz_group_output_node = xyz_group_nodes.new('NodeGroupOutput')
      xyz_group_output_node.location = (loc_x, loc_y)
      #xyz_group_output_node.inputs.new(type = 'SHADER', name = 'XYZ') # this doesn't seem to do anything, the linking works without it

      xyz_output_node = xyz_material_nodes.new('ShaderNodeOutputMaterial')
      xyz_output_node.location = (loc_x, loc_y)

      # add links
      xyz_group_links.new(xyz_geometry_node.outputs['Position'], xyz_mapping_node.inputs[0])
      xyz_group_links.new(xyz_mapping_node.outputs[0], xyz_emission_node.inputs[0])
      xyz_group_links.new(xyz_emission_node.outputs[0], xyz_mix_transparency_node.inputs[1])
      xyz_group_links.new(xyz_transparent_node.outputs[0], xyz_mix_transparency_node.inputs[2])
      xyz_group_links.new(xyz_group_input_node.outputs[0], xyz_greater_than_node.inputs[0])
      xyz_group_links.new(xyz_greater_than_node.outputs[0], xyz_mix_transparency_node.inputs[0])
      xyz_group_links.new(xyz_mix_transparency_node.outputs[0], xyz_group_output_node.inputs[0])
      # add links in xyz_material
      xyz_material_links.new(xyz_group_in_material.outputs[0], xyz_output_node.inputs[0])

      xyz_group_output_node.inputs[0].name = 'XYZ Shader'
      xyz_group.outputs[0].name = 'XYZ Shader'

    def override_material_diffuse(material, node_group):

      print('-'*60,material.name)
      if material.node_tree is not None:
        if material.node_tree.nodes.get('Material Output'):
          override_material_output_node = material.node_tree.nodes['Material Output']

          if material.node_tree.nodes.get('XYZ_material_group') is None:
            override_xyz_group = material.node_tree.nodes.new('ShaderNodeGroup')
            override_xyz_group.node_tree = node_group
            override_xyz_group.name = 'XYZ_material_group'
            override_xyz_group.label = 'XYZ_material_group'
          else:
            override_xyz_group = material.node_tree.nodes['XYZ_material_group']

          override_xyz_group.location = (override_material_output_node.location[0]-300, override_material_output_node.location[1])

          override_links = material.node_tree.links

          override_links.new(override_xyz_group.outputs[0], override_material_output_node.inputs[0])


    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                        E X E C U T E   T O O L
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    # generate the XYZ materials with correct coordinates based on camera
    generate_xyz_material(self.XYZ_wtfscale, self.XYZ_groundheight, self.XYZ_groundheight_from_selected)

    # add the XYZ group to every other material's diffuse channel
    for material in bpy.data.materials:
      override_material_diffuse(material, bpy.data.node_groups['XYZgroup'])

    return {'FINISHED'}
