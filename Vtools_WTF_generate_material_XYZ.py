import bpy
import numpy
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

    def generate_xyz_material(XYZ_scale):
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

      # figure out the rotation of the camera to get the rotation and position of the XYZ map
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
      if self.XYZ_groundheight_from_selected == True:
        height_offset = bpy.context.scene.objects.active.location[2]
      else:
        height_offset = self.XYZ_groundheight
      print('Camera vector is:   ', camera_vector)
      print('Camera vector_1z is:', camera_vector_1z)
      print('Camera target is:   ', camera_ground_target)
      print('Height offset is:   ', height_offset)

      xyz_mapping_node = xyz_nodes.new('ShaderNodeMapping')
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

    generate_xyz_material(self.XYZ_wtfscale)

    return {'FINISHED'}
