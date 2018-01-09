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



for obj in bpy.context.scene.objects:
  process_layers(obj)
  process_meshes(obj)
  process_materials(obj)
  
# bpy.context.scene.objects['MonkeyL0'].data = bpy.data.meshes['WTF']