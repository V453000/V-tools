import bpy
import math
pi = math.pi

class WTF_generate_material_XYZ(bpy.types.Operator):
  '''Generates the XYZmap material.'''
  bl_idname = 'scene.wtf_generate_material_xyz'
  bl_label = 'Generate XYZmap'
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    
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

      cam_z_rot = bpy.context.scene.camera.matrix_world.to_euler()[2] # Z rotation of the current scene's camera
      texture_z_rot = -cam_z_rot+(pi*3/2) #cam_z_rot
      texture_z_rot_simplified = texture_z_rot *2 /pi
      texture_z_rot_rounded = round(texture_z_rot_simplified, 0)
      texture_z_rot_int = (int(texture_z_rot_rounded)-3)*-1

      xyz_mapping_node = xyz_nodes.new('ShaderNodeMapping')
      xyz_mapping_node.vector_type = 'TEXTURE'

      
      xyz_mapping_node.rotation[0] = 0
      xyz_mapping_node.rotation[1] = 0
      #xyz_mapping_node.rotation[2] = -cam_z_rot+(pi*3/2)

      if texture_z_rot_int == 0:
        xyz_mapping_node.translation = (-32, -32, -32)
        xyz_mapping_node.rotation[2] = 0
        print('0')
      if texture_z_rot_int == 1:
        xyz_mapping_node.translation = ( 32, -32, -32)
        xyz_mapping_node.rotation[2] = pi/2
        print('1')
      if texture_z_rot_int == 2 or texture_z_rot_int == -2:
        xyz_mapping_node.translation = ( 32,  32, -32)
        xyz_mapping_node.rotation[2] = pi
        print('2 / -2')
      if texture_z_rot_int == -1:
        xyz_mapping_node.translation = (-32,  32, -32)
        xyz_mapping_node.rotation[2] = -pi/2
        print('-1')

      xyz_mapping_node.scale[0] = 64
      xyz_mapping_node.scale[1] = 64
      xyz_mapping_node.scale[2] = 64
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

    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                        E X E C U T E   T O O L
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    generate_xyz_material()

    return {'FINISHED'}