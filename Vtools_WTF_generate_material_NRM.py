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

      normalmap_tree = normalmap_material.node_tree
      normalmap_nodes = normalmap_tree.nodes
      normalmap_links = normalmap_tree.links
      # clean all nodes
      for node in normalmap_nodes:
        normalmap_nodes.remove(node)
      
      # add nodes
      loc_x = 0
      loc_y = 0

      name = 'Geometry_node'
      normalmap_geometry_node = normalmap_nodes.new('ShaderNodeNewGeometry')
      normalmap_geometry_node.location = (loc_x, loc_y)
      normalmap_geometry_node.name = name
      normalmap_geometry_node.label = normalmap_geometry_node.name
      loc_x =+ 200

      cam_z_rot = bpy.context.scene.camera.matrix_world.to_euler()[2] # Z rotation of the current scene's camera

      normalmap_mapping_node = normalmap_nodes.new('ShaderNodeMapping')
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
      normalmap_separate_XYZ_node = normalmap_nodes.new('ShaderNodeSeparateXYZ')
      normalmap_separate_XYZ_node.location = (loc_x, loc_y)
      normalmap_separate_XYZ_node.name = name
      normalmap_separate_XYZ_node.label = normalmap_separate_XYZ_node.name
      loc_x += 200

      loc_y += 200
      name = 'X_multiply_node'
      normalmap_X_multiply_node = normalmap_nodes.new('ShaderNodeMath')
      normalmap_X_multiply_node.location = (loc_x, loc_y)
      normalmap_X_multiply_node.operation = 'MULTIPLY'
      normalmap_X_multiply_node.name = name
      normalmap_X_multiply_node.label = normalmap_X_multiply_node.name
      loc_y -= 200
      name = 'Y_multiply_node'
      normalmap_Y_multiply_node = normalmap_nodes.new('ShaderNodeMath')
      normalmap_Y_multiply_node.location = (loc_x, loc_y)
      normalmap_Y_multiply_node.operation = 'MULTIPLY'
      normalmap_Y_multiply_node.name = name
      normalmap_Y_multiply_node.label = normalmap_Y_multiply_node.name
      loc_y -= 200
      name = 'Z_multiply_node'
      normalmap_Z_multiply_node = normalmap_nodes.new('ShaderNodeMath')
      normalmap_Z_multiply_node.location = (loc_x, loc_y)
      normalmap_Z_multiply_node.operation = 'MULTIPLY'
      normalmap_Z_multiply_node.name = name
      normalmap_Z_multiply_node.label = normalmap_Z_multiply_node.name
      loc_y = 0
      loc_x += 200

      loc_y += 200
      name = 'X_add_node'
      normalmap_X_add_node = normalmap_nodes.new('ShaderNodeMath')
      normalmap_X_add_node.location = (loc_x, loc_y)
      normalmap_X_add_node.operation = 'ADD'
      normalmap_X_add_node.name = name
      normalmap_X_add_node.label = normalmap_X_add_node.name
      loc_y -= 200
      name = 'Y_add_node'
      normalmap_Y_add_node = normalmap_nodes.new('ShaderNodeMath')
      normalmap_Y_add_node.location = (loc_x, loc_y)
      normalmap_Y_add_node.operation = 'ADD'
      normalmap_Y_add_node.name = name
      normalmap_Y_add_node.label = normalmap_Y_add_node.name
      loc_y -= 200
      name = 'Z_add_node'
      normalmap_Z_add_node = normalmap_nodes.new('ShaderNodeMath')
      normalmap_Z_add_node.location = (loc_x, loc_y)
      normalmap_Z_add_node.operation = 'ADD'
      normalmap_Z_add_node.name = name
      normalmap_Z_add_node.label = normalmap_Z_add_node.name
      loc_y = 0
      loc_x += 200

      name = 'Combine_XYZ_node'
      normalmap_combine_XYZ_node = normalmap_nodes.new('ShaderNodeCombineXYZ')
      normalmap_combine_XYZ_node.location = (loc_x, loc_y)
      normalmap_combine_XYZ_node.name = name
      normalmap_combine_XYZ_node.label = normalmap_combine_XYZ_node.name
      loc_x += 200

      name = 'Emission_node'
      normalmap_emission_node = normalmap_nodes.new('ShaderNodeEmission')
      normalmap_emission_node.location = (loc_x, loc_y)
      normalmap_emission_node.name = name
      normalmap_emission_node.label = normalmap_emission_node.name
      loc_x += 200

      name = 'Output_node'
      normalmap_output_node = normalmap_nodes.new('ShaderNodeOutputMaterial')
      normalmap_output_node.location = (loc_x, loc_y)
      normalmap_output_node.name = name
      normalmap_output_node.label = normalmap_output_node.name

      # add links
      normalmap_links.new(normalmap_geometry_node.outputs['Normal'], normalmap_mapping_node.inputs[0])
      normalmap_links.new(normalmap_mapping_node.outputs[0], normalmap_separate_XYZ_node.inputs[0])

      normalmap_links.new(normalmap_separate_XYZ_node.outputs[0], normalmap_X_multiply_node.inputs[0])
      normalmap_links.new(normalmap_separate_XYZ_node.outputs[1], normalmap_Y_multiply_node.inputs[0])
      normalmap_links.new(normalmap_separate_XYZ_node.outputs[2], normalmap_Z_multiply_node.inputs[0])

      normalmap_links.new(normalmap_X_multiply_node.outputs[0], normalmap_X_add_node.inputs[0])
      normalmap_links.new(normalmap_Y_multiply_node.outputs[0], normalmap_Y_add_node.inputs[0])
      normalmap_links.new(normalmap_Z_multiply_node.outputs[0], normalmap_Z_add_node.inputs[0])

      normalmap_links.new(normalmap_X_add_node.outputs[0], normalmap_combine_XYZ_node.inputs[0])
      normalmap_links.new(normalmap_Y_add_node.outputs[0], normalmap_combine_XYZ_node.inputs[1])
      normalmap_links.new(normalmap_Z_add_node.outputs[0], normalmap_combine_XYZ_node.inputs[2])

      normalmap_links.new(normalmap_combine_XYZ_node.outputs[0], normalmap_emission_node.inputs[0])
      normalmap_links.new(normalmap_emission_node.outputs[0], normalmap_output_node.inputs[0])

    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                        E X E C U T E   T O O L
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    generate_normalmap_material()

    return {'FINISHED'}