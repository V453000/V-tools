import bpy

print('-'*36)
print('Starting...')

# ----------------------------- #
# # # FUNCTION  DEFINITIONS # # #
# ----------------------------- #

def layer_preprocess(obj):
  if obj.name[:8] == '|Layers|':
    print('Layers Skipped for ' + obj.name)
  else:
    # define appendix list with first item
    appendix = ['Layers']
    # go through all layers
    for n in range(0,20):
      # if object uses a layer, append that ID to the appendix
      if obj.layers[n] == True:
        # format n to always have 2 digit layer IDs
        n_2d = format(n,'02d')
        # append it
        appendix.append(n_2d)
    # put together the added string
    string_to_add = ''
    for a in appendix:
      string_to_add = string_to_add + '|' + a
    string_to_add = string_to_add + '_'
    print('Layers Processed for ' + string_to_add + obj.name)

    obj.name = string_to_add + obj.name


def mesh_data_preprocess(mesh_name):
  if mesh_name[:9] == 'Transfer_':
    print('Mesh Data Skipped ' + mesh_name)
  else:
    bpy.data.meshes[mesh_name].name = 'Transfer_' + mesh_name
    print('Mesh Data Processed Transfer_' + mesh_name)


def material_preprocess(mat_name):
  if mat_name[:9] == 'Transfer_':
    print('Material Skipped ' + mat_name)
  else:
    bpy.data.materials[mat_name].name = 'Transfer_' + mat_name
    print('Material Processed Transfer_' + mat_name)
  










# --- # 
# RUN #
# --- #

# go through all objects and process layer names
for obj in bpy.context.scene.objects:
  layer_preprocess(obj)

# process all mesh data names
# create a mesh list so it doesn't iterate through new names
mesh_list = []
for mesh_data in bpy.data.meshes:
  mesh_list.append(mesh_data.name)
# iterate through list
for mesh_name in mesh_list:
  mesh_data_preprocess(mesh_name)

#process all material names
# create a material list so it doesn't iterate through new names
mat_list = []
for mat in bpy.data.materials:
  mat_list.append(mat.name)
for mat_name in mat_list:
  material_preprocess(mat_name)