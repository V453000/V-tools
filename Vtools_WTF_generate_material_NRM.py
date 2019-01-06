import bpy
import math
pi = math.pi

class WTF_generate_material_NRM(bpy.types.Operator):
  '''Generates the Normalmap material.'''
  bl_idname = 'scene.wtf_generate_material_nrm'
  bl_label = 'Generate Normalmap'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
    def generate_normalmap_material():
      if bpy.data.materials.get('Normalmap') is None:
        # create normalmapmap material
        normalmap_material = bpy.data.materials.new('Normalmap')
        normalmap_material.use_nodes = True
      else:
        normalmap_material = bpy.data.materials['Normalmap']

      
      # check if XYZmap group exists
      if bpy.data.node_groups.get('Normalgroup') is None:
        # create XYZmap group
        normal_group = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = 'Normalgroup')
      else:
        normal_group = bpy.data.node_groups['Normalgroup']

      # add input socket for alpha      
      if normal_group.inputs.get('Alpha') is None:
        normal_group.inputs.new('NodeSocketFloat', 'Alpha')


      normalmap_material_nodes = normalmap_material.node_tree.nodes
      normalmap_material_links = normalmap_material.node_tree.links
      normal_group_nodes = normal_group.nodes
      normal_group_links = normal_group.links

      # clean all nodes
      for node in normalmap_material_nodes:
        normalmap_material_nodes.remove(node)
      for node in normal_group_nodes:
        normal_group_nodes.remove(node)
      
      # add nodes
      loc_x = 0
      loc_y = 0

      name = 'Geometry_node'
      normalmap_geometry_node = normal_group_nodes.new('ShaderNodeNewGeometry')
      normalmap_geometry_node.location = (loc_x, loc_y)
      normalmap_geometry_node.name = name
      normalmap_geometry_node.label = name
      loc_x =+ 200

      cam_z_rot = bpy.context.scene.camera.matrix_world.to_euler()[2] # Z rotation of the current scene's camera

      normalmap_mapping_node = normal_group_nodes.new('ShaderNodeMapping')
      normalmap_mapping_node.vector_type = 'NORMAL'
      normalmap_mapping_node.translation[0] = 0
      normalmap_mapping_node.translation[1] = 0
      normalmap_mapping_node.translation[2] = 0
      normalmap_mapping_node.rotation[0] = 0
      normalmap_mapping_node.rotation[1] = 0
      normalmap_mapping_node.rotation[2] = -cam_z_rot+(pi*3/2) # decide rotation based on camera Z rotation


      normalmap_mapping_node.scale[0] = 0
      normalmap_mapping_node.scale[1] = 0
      normalmap_mapping_node.scale[2] = 0
      normalmap_mapping_node.location = (loc_x, loc_y)
      loc_x = loc_x + 400
      
      name = 'Separate_XYZ_node'
      normalmap_separate_XYZ_node = normal_group_nodes.new('ShaderNodeSeparateXYZ')
      normalmap_separate_XYZ_node.location = (loc_x, loc_y)
      normalmap_separate_XYZ_node.name = name
      normalmap_separate_XYZ_node.label = name
      loc_x += 200

      loc_y += 200
      name = 'X_multiply_node'
      normalmap_X_multiply_node = normal_group_nodes.new('ShaderNodeMath')
      normalmap_X_multiply_node.location = (loc_x, loc_y)
      normalmap_X_multiply_node.operation = 'MULTIPLY'
      normalmap_X_multiply_node.name = name
      normalmap_X_multiply_node.label = name
      loc_y -= 200
      name = 'Y_multiply_node'
      normalmap_Y_multiply_node = normal_group_nodes.new('ShaderNodeMath')
      normalmap_Y_multiply_node.location = (loc_x, loc_y)
      normalmap_Y_multiply_node.operation = 'MULTIPLY'
      normalmap_Y_multiply_node.name = name
      normalmap_Y_multiply_node.label = name
      loc_y -= 200
      name = 'Z_multiply_node'
      normalmap_Z_multiply_node = normal_group_nodes.new('ShaderNodeMath')
      normalmap_Z_multiply_node.location = (loc_x, loc_y)
      normalmap_Z_multiply_node.operation = 'MULTIPLY'
      normalmap_Z_multiply_node.name = name
      normalmap_Z_multiply_node.label = name
      loc_y = 0
      loc_x += 200

      loc_y += 200
      name = 'X_add_node'
      normalmap_X_add_node = normal_group_nodes.new('ShaderNodeMath')
      normalmap_X_add_node.location = (loc_x, loc_y)
      normalmap_X_add_node.operation = 'ADD'
      normalmap_X_add_node.name = name
      normalmap_X_add_node.label = name
      loc_y -= 200
      name = 'Y_add_node'
      normalmap_Y_add_node = normal_group_nodes.new('ShaderNodeMath')
      normalmap_Y_add_node.location = (loc_x, loc_y)
      normalmap_Y_add_node.operation = 'ADD'
      normalmap_Y_add_node.name = name
      normalmap_Y_add_node.label = name
      loc_y -= 200
      name = 'Z_add_node'
      normalmap_Z_add_node = normal_group_nodes.new('ShaderNodeMath')
      normalmap_Z_add_node.location = (loc_x, loc_y)
      normalmap_Z_add_node.operation = 'ADD'
      normalmap_Z_add_node.name = name
      normalmap_Z_add_node.label = name
      loc_y = 0
      loc_x += 200

      name = 'Combine_XYZ_node'
      normalmap_combine_XYZ_node = normal_group_nodes.new('ShaderNodeCombineXYZ')
      normalmap_combine_XYZ_node.location = (loc_x, loc_y)
      normalmap_combine_XYZ_node.name = name
      normalmap_combine_XYZ_node.label = name
      loc_x += 200

      name = 'Emission_node'
      normalmap_emission_node = normal_group_nodes.new('ShaderNodeEmission')
      normalmap_emission_node.location = (loc_x, loc_y)
      normalmap_emission_node.name = name
      normalmap_emission_node.label = name
      loc_y += 200
      
      name = 'Group_input_node'
      normalmap_group_input_node = normal_group_nodes.new('NodeGroupInput')
      normalmap_group_input_node.location = (loc_x, loc_y)
      normalmap_group_input_node.name = name
      normalmap_group_input_node.label = name
      loc_y -= 400
      
      name = 'Transparency_node'
      normalmap_transparency_node = normal_group_nodes.new('ShaderNodeBsdfTransparent')
      normalmap_transparency_node.location = (loc_x, loc_y)
      normalmap_transparency_node.name = name
      normalmap_transparency_node.label = name
      loc_x += 200
      loc_y += 200
      
      name = 'Mix_transparency_node'
      normalmap_mix_transparency_node = normal_group_nodes.new('ShaderNodeMixShader')
      normalmap_mix_transparency_node.location = (loc_x, loc_y)
      normalmap_mix_transparency_node.name = name
      normalmap_mix_transparency_node.label = name
      loc_x += 200

      name = 'Output_node'
      normalmap_output_node = normal_group_nodes.new('NodeGroupOutput')
      normalmap_output_node.location = (loc_x, loc_y)
      normalmap_output_node.name = name
      normalmap_output_node.label = name

      # add links
      normal_group_links.new(normalmap_geometry_node.outputs['Normal'], normalmap_mapping_node.inputs[0])
      normal_group_links.new(normalmap_mapping_node.outputs[0], normalmap_separate_XYZ_node.inputs[0])

      normal_group_links.new(normalmap_separate_XYZ_node.outputs[0], normalmap_X_multiply_node.inputs[0])
      normal_group_links.new(normalmap_separate_XYZ_node.outputs[1], normalmap_Y_multiply_node.inputs[0])
      normal_group_links.new(normalmap_separate_XYZ_node.outputs[2], normalmap_Z_multiply_node.inputs[0])

      normal_group_links.new(normalmap_X_multiply_node.outputs[0], normalmap_X_add_node.inputs[0])
      normal_group_links.new(normalmap_Y_multiply_node.outputs[0], normalmap_Y_add_node.inputs[0])
      normal_group_links.new(normalmap_Z_multiply_node.outputs[0], normalmap_Z_add_node.inputs[0])

      normal_group_links.new(normalmap_X_add_node.outputs[0], normalmap_combine_XYZ_node.inputs[0])
      normal_group_links.new(normalmap_Y_add_node.outputs[0], normalmap_combine_XYZ_node.inputs[1])
      normal_group_links.new(normalmap_Z_add_node.outputs[0], normalmap_combine_XYZ_node.inputs[2])

      normal_group_links.new(normalmap_combine_XYZ_node.outputs[0], normalmap_emission_node.inputs[0])

      normal_group_links.new(normalmap_group_input_node.outputs[0], normalmap_mix_transparency_node.inputs[0])
      normal_group_links.new(normalmap_emission_node.outputs[0], normalmap_mix_transparency_node.inputs[1])
      normal_group_links.new(normalmap_transparency_node.outputs[0], normalmap_mix_transparency_node.inputs[2])
      normal_group_links.new(normalmap_mix_transparency_node.outputs[0], normalmap_output_node.inputs[0])

      normal_group.outputs[0].name = 'Normal shader'

      # add normal group to material
      NRM_in_material = normalmap_material_nodes.new('ShaderNodeGroup')
      NRM_in_material.node_tree = normal_group
      NRM_material_output = normalmap_material_nodes.new('ShaderNodeOutputMaterial')
      NRM_material_output.location = (200,0)
      normalmap_material_links.new(NRM_in_material.outputs[0], NRM_material_output.inputs[0])

    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                        E X E C U T E   T O O L
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    generate_normalmap_material()

    return {'FINISHED'}