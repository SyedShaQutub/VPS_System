# reload every import 
import sys, os
import importlib
import bpy
import metaData
importlib.reload(metaData)
import objectbasedAlpha
importlib.reload(objectbasedAlpha)
from objectbasedAlpha import objectbasedAlpha
# TODO: change this to relative path using os/pathlib
# NOTE: If you load Blender first then open a project then the CWD is where Blender is. If you script from the blender the CWD is the location of the blender program.

# TODO: When excecuted in blender the os.path gives out C:/ instead of abs path of scene_launch; for now hard code the abs path of this file.
# office WS C:/Users/Qutub/Documents/VPS/scene_content/VPS_project/scene_creation
# HP laptop C:/Users/squtub/Documents/Master_Thesis/Git/vps_engine/scene_creation

filepath = bpy.context.space_data.text.filepath
print(filepath)
labels_path = os.path.dirname(filepath)
labels_path = labels_path.replace('\\','/')
sys.path.append(labels_path)

def edit_ShaderEditorNodes():
    # adapts FBX model for cycle renderer
    mat = [mat.name for mat in bpy.data.materials]
    for _mat in mat:

        #delete the node Image Texture.001
        purge_nodeName = 'Image Texture.001'
        principled_bsdf = 'Principled BSDF'
        nodes = bpy.data.materials[_mat].node_tree.nodes
        links = bpy.data.materials[_mat].node_tree.links
        node_names = [node.name for node in nodes]
        if purge_nodeName in node_names and principled_bsdf in node_names:
            print(_mat)
            purge_node = nodes[purge_nodeName]
            nodes.remove(purge_node)
            links.new(nodes['Image Texture'].outputs['Alpha'], nodes['Principled BSDF'].inputs['Alpha'])
            
def gen_CompositorNodes():
    obj_names = [obj.name for obj in bpy.data.objects]
    labels = metaData.labels
    obj_pass_idx = [0] * len(obj_names)
    obj_labels_name = ['unlabeled'] * len(obj_names)
    obj_labels_color = [(0,0,0)] * len(obj_names)

    bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True

    for obj_ind, obj in enumerate(obj_names):
        for label in labels:
            if label[-1].lower() in obj.lower(): 
                bpy.data.objects[obj].pass_index = label[1]
                obj_pass_idx[obj_ind] = label[1]
                obj_labels_color[obj_ind] = list(label[7])
                obj_labels_name[obj_ind] = label[0]

    print(obj_labels_name)
    print(obj_pass_idx)

    labels_list = list(zip(obj_labels_name, obj_pass_idx, obj_labels_color))
    del obj_pass_idx, obj_labels_name, obj_labels_color

    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    links = tree.links
    # remove all nodes
    for currentNode in tree.nodes:
        tree.nodes.remove(currentNode)

    alphablocks = []
    renderer = tree.nodes.new('CompositorNodeRLayers') # add render node
    global_composite = tree.nodes.new('CompositorNodeComposite')
    global_composite.use_alpha = True
    inputLink_image = renderer.outputs[0]
    inputLink_obj_id = renderer.outputs[14]

    ## TEST to check the class
    # alphablocks.append(objectbasedAlpha(labels_list[0], inputLink_image, inputLink_obj_id, 0, tree))
    # inputLink_image = alphablocks[0].get_outputLink()

    for idx, label_list in enumerate(labels_list):
        alphablocks.append(objectbasedAlpha(label_list, inputLink_image, inputLink_obj_id, idx, tree))
        inputLink_image = alphablocks[idx].get_outputLink()

    #Global LinkS
    links.new(inputLink_image, global_composite.inputs[0] )

def gen_labels():

    gen_CompositorNodes()
    FILEPATH = launch_path + '/test.png'
    bpy.data.scenes['Scene'].render.filepath = FILEPATH
    bpy.ops.render.render(layer='RenderLayers', write_still=True)

def gen_labels_test(labels_path=None):

    gen_CompositorNodes()
    FILEPATH = labels_path + '/test.png'
    bpy.data.scenes['Scene'].render.filepath = FILEPATH
    bpy.ops.render.render(layer='RenderLayers', write_still=True)

if __name__ == "__main__":
     gen_labels_test()