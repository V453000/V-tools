import bpy

print('-'*36)
print('Starting...')

# generate 0..19 layer ID list
layer_list = []
for w in range(0,20):
  w_2d = format(w, '02d')
  layer_list.append(w_2d)
print(str(layer_list))

def process_layers(obj):
  
  if obj.name[:8] == '|Layers|':
    # enable layer 19 to be able to disable any other layer before getting to 19
    obj.layers[19] = True
    # disable all layers except 19
    for u in range(0,19):
      obj.layers[u] = False

  tested_name = obj.name[7:]

  # check if the string maches any layer ID and set layers based on that
  # only process things which start with |
  if tested_name[:1] == '|':
    print(tested_name)
    # as long as the name starts with |, iterate
    while tested_name[:1] == '|':
      # cut out the first character - |
      tested_name = tested_name[1:]
      # get the first characters from the new string (numeric ID)
      layer_ID = tested_name[:2]
      print(layer_ID)
      # enable layers based on the numeric ID
      for i in range(0,20):
        if layer_ID == layer_list[i]:
          obj.layers[i] = layer_ID == layer_list[i]
        
      # cut the last 2 characters from the start (numeric ID)
      tested_name = tested_name[2:]
      print(tested_name)
    obj.name = tested_name[1:]

def process_meshes(obj):
  if obj.type == 'MESH':
    data_name_start = obj.data.name[:9]
    if data_name_start == 'Transfer_':
      data_name = obj.data.name[9:]
      print(data_name)
      if bpy.data.meshes.get(data_name) is not None:
        obj.data = bpy.data.meshes[data_name]
      else:
        obj.data.name = data_name

def process_materials(obj):
  if obj.type == 'MESH' or obj.type == 'CURVE':
    if obj.data.materials:
      slotCount = len(obj.material_slots)
      slotNumber = 0
      print(obj.name, 'slotCount is',slotCount)

      for slotNumber in range(0, slotCount):
        
        # this can happen when there is only 1 slot but with no material (typically shadow plane)
        if obj.material_slots[slotNumber].material is not None:
          transfer_mat_name = obj.material_slots[slotNumber].material.name
          if transfer_mat_name[:9] == 'Transfer_':
            destination_mat_name = transfer_mat_name[9:]
            # if matching material is found, use that material
            if bpy.data.materials.get(destination_mat_name) is not None:
              destination_material = bpy.data.materials[destination_mat_name]
              obj.material_slots[slotNumber].material = destination_material
              print('Adding material to' ,obj.name, 'slot number', slotNumber)   
            # if there is no matching material, keep it unique and put the name back without Transfer_
            else:
              obj.material_slots[slotNumber].material.name = destination_mat_name
              print('Matching material' + destination_mat_name + ' not found. Removing Transfer_ from name and skipping.')
          
    else:
      print('Skipping' + obj.name + 'No material slots found.')




for obj in bpy.context.selected_objects:
  #process_layers(obj)
  process_meshes(obj)
  #process_materials(obj)
  
# bpy.context.scene.objects['MonkeyL0'].data = bpy.data.meshes['WTF']